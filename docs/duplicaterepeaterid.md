# Duplicate Repeater IDs

As a regions mesh network grows, the likelihood of two repeaters sharing the same short identifier increases. MeshMapper has a robust system for detecting, handling, and resolving these "collisions" to ensure data integrity.

## The "2-Char" Limitation

MeshCore repeaters are identified by a **Short ID** consisting of the first two characters of its Public ID (e.g., `A1`, `4F`, `09`).  As a message travels across different repeaters in a mesh to its destination, these repeaters append their 2 character ID to the message as a "hop".  MeshMapper operates using these 2 character ID's to associate coverage information with which repeaters were involved in that ping.

Since this Short ID is only two hexadecimal digits long, there are only **254 possible combinations** (01 to FE...00 and FF are reserved in the MeshCore firmware). As the number of repeaters in a region increases, it becomes statistically inevitable that two completely different devices will end up generating with the same Short ID.

When this happens, it is called a **Collision**.

## How MeshMapper Handles Collisions

MeshMapper prioritizes data accuracy. If two repeaters share the ID `A1`, and a message repeat is heard by or is received via `A1`, the system has no way of knowing *which* physical repeater was actually involved. To prevent potentially inaccurate data from being represented on the map, MeshMapper enters a "Quarantine" mode for the affected devices.

### 1. Detection & Quarantine
When a new repeater appears on the network with a Short ID that is already in use by a different device:
  - **Both** repeaters (the existing one and the new one) are immediately flagged as **Excluded**.
  - The system assigns the new repeater a temporary internal ID (e.g., `X1`) to differentiate it in the database and map, but it remains linked to the collision.
  - Both repeaters are excluded from regional or global leaderboards and statistics (like maximum distance reached)
### 2. Map Appearance
  - **Red Icons**: Both repeaters will appear on the map with **Red** icons (instead of the standard Orange or Grey).
  - **Popups**: Clicking on the repeater may show its status as "Excluded" or "Duplicate" and will list the repeaters that are in collision.
  - **Pings**: Clicking a grid square on the map that has a repeater involved in an active collision will draw red dashed lines to each repeater in the collision group (and list distance in KM).
  - **Leaderboards**: Both repeaters are immediately removed from all Leaderboards (Best Repeaters, Max Range, etc.) both on the local region and globally to prevent skewed statistics.

### 3. Impact on Collected Data
  - **Ambiguity**: If a ping is ingested containing a repeater that has a collision (e.g., via `A1`), MeshMapper cannot attribute that hop to a specific location with certainty.
  - **Data Integrity**: This data is forever flagged as being ambiguous, and will never associate with a repeater (even after the collision is resolved).

## Resolution

Collisions are typically resolved in one of two ways:

### Automatic Cleanup (Stale Data)
Often, a collision occurs because an old, offline repeater is still in the database when a new one comes online.
  - MeshMapper runs a cleanup routine (typically every few days).
  - If one of the colliding repeaters has not been heard from in **3 days**, it is considered "Stale" and is automatically deleted.
  - **The Survivor**: Once the stale duplicate is removed, the remaining active repeater is automatically restored to **Active** status. Its icon will turn back to normal, it will reappear on Leaderboards, and new incoming pings will properly associate themselves with this repeater again.

### Manual Resolution
If both repeaters are active and legitimate (a true collision between two live devices):
  - Region administrators receive an alert regarding the collision.  If able, it is suggested that the administrator resolve the issue by asking the owner of the new repeater to generate a new ID.
  - If the administrator knows the the collision has been cleared, they may manually reinstate the remaining repeater

## Summary Table

| State | Indicator | Meaning |
| --- | --- | --- |
| **Active** | Green / Grey Icon | Normal operation. Unique ID. |
| **New** | Orange Icon | Recently discovered (less than 14 days old). |
| **Excluded** | **Red Icon** | **Duplicate ID Detected.** Data from this repeater is currently untrusted. |

## Permanent Solution
*MeshCore does not have to use 2-character IDs*.  This is a limitation that can be, albeit with a lot of work and coordination from the MeshCore developers, resolved by implementing 4-character (or more) IDs.

Please post your concerns on the discussion here:
https://github.com/meshcore-dev/MeshCore/issues/1083

With 4-character HEX IDs, a region can have up to **65,536** different repeaters without ID collisions.