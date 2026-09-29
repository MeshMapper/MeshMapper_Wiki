# Multi-Byte Repeaters

Every packet in a MeshCore mesh carries a record of the repeaters it passed through (its **path**). Each repeater adds the first 1, 2 or 3 bytes of its Public ID to the path. Each of those entries is a **hop**.

MeshMapper supports 1-, 2- and 3-byte hops across the wardriving app and the map.

---

## The 1-Byte Problem

In 1-byte mode, a repeater is identified by just the first two hex characters of its Public ID (e.g. `A1`, `4F`, `09`). That's only **254** usable IDs (`00` and `FF` are reserved), so growing regions end up with two repeaters sharing an ID.

When that happens, MeshMapper can't tell which repeater a packet went through. The affected repeater is marked **Ambiguous** (red on the map). Pings still count for coverage, but they aren't linked to it.

With 2 or 3 bytes there are tens of thousands or millions of IDs, so collisions become rare.

!!! tip "How MeshMapper decides"
    A repeater is judged at its own width, and a hop is only credited when exactly one repeater matches it. See [The Rules](duplicaterepeaterid.md#the-rules) on the Duplicate Repeater IDs page.

## Upgrading to Multi-Byte

You don't need to upgrade every device at once. Multi-byte repeaters still relay packets from repeaters and companions on 1-byte firmware.

### Step 1: Update the Repeater

Flash the repeater with **MeshCore firmware v1.14.1 or newer**, then set its hop width from the repeater's command line.

For 2-byte:

```
set path.hash.mode 1
```

For 3-byte:

```
set path.hash.mode 2
```

Reboot the repeater, then **send a flood advert**. MeshMapper reads the width from the repeater's flood advert and updates it automatically.

### Step 2: Set the Width for Wardrivers

Once most of your repeaters are upgraded, set **App Path Bytes** in the region admin panel under **Settings → Wardriving → Radio Channels** (the **Path B** column, one per radio preset). Options are **Device** (leave it to the wardriver's radio), **2** or **3**.

This tells the wardriving app what hop width to set on wardrivers' companion radios. It doesn't change repeaters; they get their width from their own adverts. For grouped regions, the group admin sets it.

### How MeshMapper Tracks Each Repeater

MeshMapper tracks every repeater separately, so a region can run a mix of 1-, 2- and 3-byte repeaters.

  - **Advertised width**: taken from the repeater's latest **flood advert**. If it later adverts at 1 byte again, this goes back down.
  - **Multibyte capable**: set the first time MeshMapper sees the repeater with a 2- or 3-byte hop, in its own advert, a wardriving ping, or any flood packet an observer hears. Once set, it stays set.

For example, repeater `A1B2C3D4E5F6` was known as `A1`. The first time it's heard as `A1B2`, it's marked multibyte capable and judged at 2 bytes from then on.

### Collisions Clear Up Automatically

As repeaters upgrade, old collisions resolve on their own:

  - `AB` (1-byte) and `AB` (1-byte) **collide**: they can't be told apart.
  - `AB12` (2-byte) and `AB9F` (2-byte) **don't**: the longer IDs tell them apart.

When a repeater in a collision next adverts, MeshMapper re-checks it and returns it to normal if it can now be told apart.

## Tracking Your Region's Upgrade

  - **Repeater List** (**Region** menu): the **Non-Multibyte Capable** and **Multibyte Capable** tabs show which repeaters still need upgrading.
  - **ID width** filter (**Filter Map Data**): show only repeaters and pings using 1-, 2- or 3-byte IDs. See [Filters](layers.md#filters).
  - **Multibyte Upgrade Board** on the global leaderboard: ranks regions by how far their upgrade has got.

### Repeater ID Grid

Open **Region → Repeater IDs** to see **Repeater ID Usage**: a grid of every first-byte prefix (`00` to `FF`).

| Colour | Status | Meaning |
| --- | --- | --- |
| **Green** | Available | No repeater uses this first byte. |
| **Blue** | Deployed | In use, and every repeater here can be told apart. |
| **Red** | Conflict | At least one repeater here can't be told apart from another: two 1-byte repeaters sharing it, or multi-byte repeaters sharing their full 2 or 3 bytes. |
| **Dark grey** | Reserved | `00` and `FF`, reserved by MeshCore. |

Click a cell to see the repeaters using that prefix, with their Public ID, width, hardware and any conflict. Use the **search** box or the tag filters (**MB**, **Ambiguous**, **2-Byte**, **3-Byte**, **No Location**, **Out of Region**, **Ghost**, **Observer**, **CARpeater**) to narrow it down.

Private (🚫) repeaters are listed as **Hidden** and still count towards usage and conflicts.

## In the Wardriving App

  - If the region sets **App Path Bytes**, the app sets that width on your companion radio and tells you when it changes.
  - If the region leaves it to the device, you can choose the width yourself in the app's wardriving settings.
  - Companion firmware older than 1.14 can only use 1 byte; the app will recommend a firmware update.
