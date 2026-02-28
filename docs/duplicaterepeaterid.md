!!! success "Change is comining!"
    With multi-byte repeater path functionality being actively developed by the MeshCore team, the below information will, thankfully, soon become irrelevant.

    Until such a time, duplicate repeater ID's can be managed using the below methods, or by driving in Passive or Hybrid modes where **Discovery** packets are used.  **Discovery**, or **DISC**, packets associate with repeaters using their full Public ID.

# Duplicate Repeater IDs

As a regions mesh network grows, the likelihood of two repeaters sharing the same short identifier increases. MeshMapper has a robust system for detecting, handling, and resolving these "collisions" to ensure data integrity.

MeshMapper does not filter out repeaters outside of a regions defined boundry, as that would not be an accurate representation of real-world RF conditions.

!!! tip "Override Available"
    Regions now have the ability to override MeshMapper's default duplicate ID detection logic if they prefer to visualize all data regardless of ambiguity.
    
    [Learn how to override duplicate detection](https://wiki.meshmapper.net/overrideduplicates/)

## The 1-byte Limitation

MeshCore repeaters are identified in packets using 1-byte consisting of the first two characters of its Public ID (e.g., `A1`, `4F`, `09`).  As a message travels across different repeaters in a mesh to its destination, these repeaters append their 2 character ID to the message as a "hop".  MeshMapper operates using these 2 character ID's to associate coverage information with which repeaters were involved in that ping.

Since this is only two hexadecimal digits long, there are only **254 possible combinations** (01 to FE...00 and FF are reserved in the MeshCore firmware). As the number of repeaters in a region increases, it becomes statistically inevitable that two completely different devices will end up generating with the same Short ID.

When this happens, it is called a **Collision**.

## How MeshMapper Handles Collisions

MeshMapper prioritizes data accuracy. If two repeaters share the ID `A1`, and a message repeat is heard by or is received via `A1`, the system has no way of knowing *which* physical repeater was actually involved. To prevent potentially inaccurate data from being represented on the map, MeshMapper enters a "Quarantine" mode for the affected devices.

### 1. Detection & Quarantine
When a new repeater appears on the network with an ID that is already in use by a different device:

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
Wardrivers can choose to collect data in **Passive** or **Hybrid** modes, which utilize **Discovery**, or **DISC**, packets.  You can think of these packets as broadcasting "Hello, who's out there?", and any repeater within hearing distance (and with compatible firmware) will respond with their full Public ID.  As we're not relying on only 2 hex characters to make the association to the repeater, associations can be made even if the first 2 characters of that particular repeater is in collision with another.

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
    As long as two (or more) repeaters with the same first 2 characters of the public ID exist in a region, regardless of current status, pings will not get accociated to a repeater with that ID, unless those pings are of **DISC** type (which associate using the full Public ID of the repeater)

## Summary Table

| State | Indicator | Meaning |
| --- | --- | --- |
| **Active** | Green / Grey Icon | Normal operation. Unique ID. |
| **New** | Orange Icon | Recently discovered (less than 14 days old). |
| **Excluded** | **Red Icon** | **Duplicate ID Detected.** Data from this repeater is currently untrusted. |

## Permanent Solution
*MeshCore does not have to use 1-byte to identify repeaters in hops*.  This is a limitation that can be, albeit with a lot of work and coordination from the MeshCore developers, resolved by representing repeaters using 2-bytes or more.

Please post your concerns on the discussion here:

<https://github.com/meshcore-dev/MeshCore/issues/1083>
and
<https://github.com/meshcore-dev/MeshCore/discussions/1613>

With 2-byte IDs, a region can have up to **65,536** different repeaters without ID collisions.