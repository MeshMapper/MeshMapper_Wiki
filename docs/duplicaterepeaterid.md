!!! success "Multi-Byte Hops Are Here!"
    MeshCore firmware now supports multi-byte repeater hop identification (up to 3 bytes), and MeshMapper fully supports it. Regions running firmware with 2 or 3 byte hops will see far fewer (or zero) collisions. This requires repeaters and companions running **firmware version 1.14.0 or newer**.

    For regions still running 1-byte hops, duplicate repeater IDs can be managed using the below methods, or by driving in **Hybrid** mode where **Discovery** packets are used.  **Discovery**, or **DISC**, packets associate with repeaters using their full Public ID.  [Read more about this here.](#workarounds)

# Duplicate Repeater IDs

As a regions mesh network grows, the likelihood of two repeaters sharing the same short identifier increases. MeshMapper has a robust system for detecting, handling, and resolving these "collisions" to ensure data integrity.

MeshMapper does not filter out repeaters outside of a regions defined boundry, as that would not be an accurate representation of real-world RF conditions.

!!! tip "Override Available"
    Regions now have the ability to override MeshMapper's default duplicate ID detection logic if they prefer to visualize all data regardless of ambiguity.

    [Learn how to override duplicate detection](https://wiki.meshmapper.net/overrideduplicates/)

## Hop Bytes: 1, 2, or 3

MeshCore repeaters are identified in packets by appending a portion of their Public ID as a "hop" to each message they relay. The number of bytes used for this identifier is called **Hop Bytes**, and is configurable per-region in MeshMapper.

| Hop Bytes | Hex Characters | Unique IDs | Example |
| --- | --- | --- | --- |
| **1** | 2 | ~254 | `A1` |
| **2** | 4 | ~65,536 | `A1B2` |
| **3** | 6 | ~16,777,216 | `A1B2C3` |

Region administrators can configure the Hop Bytes setting in the admin panel under **Settings**. This should match the firmware configuration of the repeaters in the region.

!!! info "Per-Repeater Detection"
    MeshMapper tracks hop bytes on a per-repeater basis. If a repeater sends in a ping using a longer ID than previously seen, MeshMapper automatically updates that repeater's hop bytes value. This means a region transitioning from 1-byte to 2-byte hops will see repeaters update as they are heard.

### The 1-Byte Limitation

In **1-byte mode**, repeaters are identified using the first two characters of their Public ID (e.g., `A1`, `4F`, `09`). Since this is only two hexadecimal digits long, there are only **254 possible combinations** (01 to FE...00 and FF are reserved in the MeshCore firmware). As the number of repeaters in a region increases, it becomes statistically inevitable that two completely different devices will end up with the same Short ID.

When this happens, it is called a **Collision**.

With **2-byte** or **3-byte** hops, the number of available unique IDs increases dramatically, making collisions extremely unlikely in all but the largest deployments.

## How MeshMapper Handles Collisions

MeshMapper prioritizes data accuracy. If two repeaters share the same short ID prefix (at the configured hop byte length), and a message repeat is heard by or is received via that prefix, the system has no way of knowing *which* physical repeater was actually involved. To prevent potentially inaccurate data from being represented on the map, MeshMapper enters a "Quarantine" mode for the affected devices.

### Smart Collision Detection

MeshMapper uses **per-repeater hop bytes** to determine whether two repeaters are truly in collision:

- Two repeaters are only considered colliding if they are **indistinguishable** at the longer of their two hop byte lengths.
- For example, repeater `AB` (1-byte) and repeater `AB12` (2-byte) are **not** in collision, because at 2 bytes (`AB` vs `AB12`), they are distinguishable.
- However, repeater `AB` (1-byte) and repeater `AB` (1-byte) with different full Public IDs **are** in collision, because at 1 byte they cannot be told apart.

This means regions transitioning from 1-byte to 2-byte firmware will see collisions automatically resolve as repeaters begin reporting longer IDs.

### 1. Detection & Quarantine
When a new repeater appears on the network with an ID that is indistinguishable from an existing device (at their respective hop byte lengths):

  - **Both** repeaters (the existing one and the new one) are immediately flagged as **Excluded**.
  - The system assigns the new repeater a temporary internal ID (e.g., `X1`) to differentiate it in the database and map, but it remains linked to the collision.
  - Both repeaters are excluded from regional or global leaderboards and statistics (like maximum distance reached)

### 2. Map Appearance

  - **Red Icons**: Both repeaters will appear on the map with **Red** icons (instead of the standard Pink, Orange or Grey).
  - **Popups**: Clicking on the repeater will show its status as "Duplicate" and will list the repeaters that are in collision with it.
  - **Pings**: Clicking a grid square on the map that has a repeater involved in an active collision will draw red dashed lines to each repeater in the collision group (and list distance), allowing the viewer to make their own assumption on which repeater was actually involved.
  - **Leaderboards**: Both repeaters are immediately removed from all Leaderboards (Best Repeaters, Max Range, etc.) both on the local region and globally to prevent skewed statistics.

### 3. Impact on Collected Data

  - **Ambiguity**: If a ping is ingested containing a repeater that has a collision (e.g., via `A1`), MeshMapper cannot attribute that hop to a specific location with certainty.
  - **Data Integrity**: This data is forever flagged as being ambiguous, and will never associate with a repeater (even after the collision is resolved).

## Workarounds

### Upgrade to Multi-Byte Hops
The most effective solution is to upgrade your region's repeaters to firmware that supports **2-byte or 3-byte hops**. Once upgraded, update the **Hop Bytes** setting in your region's admin panel to match. As repeaters are heard with longer IDs, MeshMapper will automatically update their hop byte tracking and resolve false collisions.

### Hybrid Wardriving Mode
Wardrivers can choose to collect data in **Hybrid** mode, which utilizes **Discovery**, or **DISC**, packets.  You can think of these packets as broadcasting "Hello, who's out there?", and any repeater within hearing distance (and with compatible firmware) will respond with their full Public ID.  As we're not relying on only the short hop ID to make the association to the repeater, associations can be made even if the short ID of that particular repeater is in collision with another.

!!! tip "Enforce Hybrid Mode"
    If a region is large and contains many duplicate ID's, region administrators can choose to "Enforce Hybrid Mode" for their region.  This will prevent any **Active** wardriving from occuring in the region by automatically enabling Hybrid mode for wardrivers.  The option is available in the regional admin panel.

## Resolution

Collisions are typically resolved in one of two ways:

### Automatic Cleanup
Often, a collision occurs because an old, offline repeater is still in the database when a new one comes online.

  - MeshMapper runs a cleanup routine every day.
  - If one of the colliding repeaters has not been heard from in **3× the region's configured Stale Repeater Age** (e.g., 72 hours at the default 24-hour setting), it is considered gone and is automatically deleted.
  - **The Survivor**: Once the duplicate ID is removed, the remaining active repeater is automatically restored to **Active** status. Its icon will turn back to normal, it will reappear on Leaderboards, and new incoming pings will properly associate themselves with this repeater again.

### Manual Resolution
If both repeaters are active and legitimate (a true collision between two live devices):

  - Region administrators receive an alert regarding the collision.  If able, it is suggested that the administrator resolve the issue by asking the owner of the new repeater to generate a new ID.
  - If the administrator knows the the collision has been cleared, they may manually reinstate the remaining repeater and delete the old. If the collision has not been cleared, both repeaters will enter excluded state again on next advert. 

!!! warning "Note"
    As long as two (or more) repeaters are indistinguishable at their hop byte length, regardless of current status, pings will not get associated to a repeater with that ID, unless those pings are of **DISC** type (which associate using the full Public ID of the repeater).

!!! info "TRACE vs DISC for Collisions"
    Unlike **DISC** packets which use the full Public ID to uniquely associate with a repeater, **TRACE** packets only carry the short repeater hop ID. This means TRACE data is subject to the same prefix-based collision detection as standard BIDIR/TX/DEAD pings. In regions with active duplicate IDs, TRACE data for those repeaters will be quarantined just like other ping types.

## Summary Table

| State | Indicator | Meaning |
| --- | --- | --- |
| **Active** | Green / Grey Icon | Normal operation. Unique ID. |
| **New** | Orange Icon | Recently discovered (less than 14 days old). |
| **Excluded** | **Red Icon** | **Duplicate ID Detected.** Data from this repeater is currently untrusted. |

## Multi-Byte Hop Support

MeshCore now supports multi-byte repeater hop identification, available in **firmware version 1.14.0 and newer** for both repeaters and companions. MeshMapper fully supports **1-byte**, **2-byte**, and **3-byte** hop modes across all features including collision detection, coverage mapping, leaderboards, etc.

| Hop Bytes | Max Unique IDs | Suitable For |
| --- | --- | --- |
| **1 byte** | ~254 | Small regions with few repeaters |
| **2 bytes** | ~65,536 | Most regions |
| **3 bytes** | ~16,777,216 | Very large deployments |