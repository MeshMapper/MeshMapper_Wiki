# Duplicate Repeater IDs

Packets identify each repeater they pass through by a short **hop ID**: the first 1, 2 or 3 bytes of its Public ID. As a region grows, two repeaters can end up with the same hop ID. This is a **collision**, and MeshMapper can't always tell which of the two a packet went through.

This page explains how MeshMapper decides, what you'll see, and how to fix it.

!!! tip "The best fix is multi-byte"
    With 1-byte IDs there are only 254 to go around, so collisions are common. With 2 or 3 bytes they become rare. See [Multi-Byte Repeaters](multibyte.md) to upgrade.

## The Rules

MeshMapper follows two rules, on the server and on the map.

### Rule A: When a Repeater Is Ambiguous

A repeater is marked **Ambiguous** if it **can't be told apart from another repeater at its own width**:

  - A 1-byte repeater is judged on its first byte.
  - A multi-byte repeater is judged at the width it advertises (at least 2 bytes).

This is judged separately for each repeater, so a collision doesn't always flag both:

| Repeaters | Result |
| --- | --- |
| `AB` (1-byte) and `AB` (1-byte) | **Both Ambiguous.** They can't be told apart. |
| `AB` (1-byte) and `AB12` (2-byte) | **Only `AB` is Ambiguous.** A 1-byte `AB` hop could be either, but `AB12` is unique at its own width. |
| `AB12` (2-byte) and `AB9F` (2-byte) | **Neither.** They're different at 2 bytes. |

### Rule B: When a Ping's Hop Is Credited

A hop in a ping's path is credited to a repeater only if **exactly one** repeater's ID starts with that hop, at the hop's own width.

  - **One match**: credited to that repeater.
  - **More than one**: ambiguous. The ping still counts for coverage, but isn't linked to any repeater.
  - **No match**: unknown. The ping still counts, unlinked.

### Other Rules

  - **Discovery (DISC) pings** carry the repeater's full Public ID, so they're always credited to the right repeater, even during a collision. **TRACE** pings only carry the short hop ID, so Rule B applies to them.
  - **Corrupted adverts**: a garbled advert that makes a near-copy of a repeater's ID is recognised as the same repeater and doesn't make it Ambiguous.
  - **Far-away matches**: if the only match is unusually far from the ping, it's held for a region admin to review instead of being linked.
  - **Groups**: in a [multiregion group](multiregions.md), collisions are checked across every region in the group.
  - **Outside the boundary**: repeaters outside a region's boundary are still counted (tagged **Out of Region**), because RF doesn't stop at the border.

## What You'll See

  - **On the map**: the repeater's chip has a **red** edge (**Ambiguous** in the Legend).
  - **In its details**: an **Ambiguous** status and a red **AMBIGUOUS ID DETECTED** box listing its **Collision Group**.
  - **On a ping**: when you select a single ping with an ambiguous hop, red dashed **Duplicate** lines go to each possible repeater with their distance, so you can judge which was likely involved.
  - **On leaderboards**: Ambiguous repeaters stay listed, marked with a red **\*** ("Ambiguous ID"). Pings where their hop was ambiguous don't count towards them.
  - **For admins**: an **Ambiguous Public IDs Detected** box in the admin panel, plus an optional Discord DM and region webhook (both called **Ambiguous Repeater ID**).

## What Happens to the Data

A ping whose hop was ambiguous is stored as unlinked, and **stays unlinked**, even after the collision is resolved. MeshMapper won't guess later.

When a new repeater creates a collision, MeshMapper also checks recent pings that were linked to the old repeater before the collision existed. Any that could now belong to either repeater are unlinked.

## Avoiding Collisions

### Upgrade to Multi-Byte

The most effective fix. Once repeaters advertise 2 or 3 bytes, most collisions clear up on their own. See [Multi-Byte Repeaters](multibyte.md).

### Wardrive in Hybrid Mode

**Hybrid** mode sends **Discovery (DISC)** requests: "who's out there?" Any repeater in range (firmware 1.10+) replies with its full Public ID, so the ping is credited correctly even when its short ID collides.

!!! tip "Enforce Hybrid"
    Region admins can require Hybrid mode for a radio preset with the **Hybrid** column under **Settings → Wardriving → Radio Channels** in the admin panel. Wardrivers on that preset can't use Active mode.

## Resolving a Collision

### Automatic Cleanup

Often a collision is an old, offline repeater still on record when a new one comes online. That fixes itself:

  - Every day, a repeater that hasn't been heard for the region's **Repeater Inactive After (Days)** (default 30, under **Settings → Repeaters, Neighbours & Scopes**) is marked **Inactive** and drops off the map.
  - Inactive repeaters don't count in collisions, so the remaining repeater returns to normal on the next advert in that ID range.
  - If the silent repeater comes back on air, it's reactivated, and if the ID still collides, it's Ambiguous again.

Inactive repeaters aren't deleted unless the region has set a retention period for removing them.

!!! tip "Bypass Auto Delete"
    For a repeater that goes offline for long periods (seasonal, remote), admins can tick **Bypass Auto Delete** in its edit window. Automatic cleanup then skips it. It also keeps its partner Ambiguous while it's away.

### Manual Resolution

If both repeaters are live and genuine:

  - The best fix is to ask one owner to **generate a new ID** for their repeater, or to upgrade both to multi-byte.
  - If one repeater is gone for good, a region admin can set its **Status** to **Inactive** or **Disabled** in the admin panel. The other returns to normal on the next advert.
  - Setting an Ambiguous repeater back to **Active** doesn't stick. It's re-checked on the next advert.

!!! warning "Deleting doesn't help"
    A deleted repeater adds itself back on its next advert. Change its status instead.

## Turning Detection Off

A region can turn this off with **Disable Duplicate ID Detection Logic**, and show every possible repeater instead. See [Override Duplicate IDs](overrideduplicates.md).

## Repeater States

For every repeater state and colour (Active, New, Stale, Ambiguous, Backbone), see [Repeater States](visuals.md#repeater-states).
