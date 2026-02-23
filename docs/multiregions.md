# Multiregion Groups

A Multiregion Group allows multiple individual regions/IATA's to be combined into a single, seamless map interface, and allows MeshMapper to properly represent data based on real-world conditions.

## How it Works

When regions are grouped:

1.  **Unified Map**: The individual maps and leaderboards for each region are effectively merged.
2.  **Shared Logic**: The system treats the group as a single entity for data processing.
    *   **Duplicate Detection**: Scans for duplicate repeater IDs across *all* regions in the group. If region `AAA` has a repeater `AA` and region `BBB` has a repeater `AA`, those repeaters will correctly enter collision with one another.
    *   **Leaderboards**: Statistics are aggregated. A user's contribution counts towards the group leaderboard, and repeaters are ranked against all others in the group.
3.  **Centralized Administration**: Administrators can gain access to a **Grouped Admin Panel**, allowing them to monitor and manage all sub-regions simultaneously.  Individual regions within the group can still be administered individually.
4.  **Wardriving Handoff**: Wardrivers leaving one individual region and entering another will have their session automatically transferred and companion authorized without interruption.

## When to use a Multiregion Group

Multiregion groups are designed for specific scenarios where one regions mesh traffic can be heard by another.

### ✅ When to use multiregion groups
*   When repeaters in one region can be heard by observers in a neighboring region.
*   When wardriving in one region may have pings heard/repeated by repeaters in a neighboring region.

### ❌ When NOT to use it
*   When repeater adverts or wardriving traffic in one region would not be heard by repeaters or observers in another.  Combining two regions that cannot physically share mesh traffic can result in repeaters unnecessarily entering a collision/duplicate state.

## Why?

The primary reason to create multiregion groups is **data accuracy**.  Use this example below:
![Image](https://meshmapper.net/img/upload_20260223_072127_2dd1a584.png)
In this example, you have a car wardriving around the border of region `AAA`.  Nearby is region `BBB`.

The wardrivers companion sends out a ping.  Region `AAA`'s repeater `AA` is too far away to hear the ping.  Region `BBB`'s repeater `AA` is close enough and rebroadcasts that ping.  The wardrivers companion hears this repeat.  The ping propagates through the mesh network is is picked up by an observer in region `AAA`.  MeshMapper's backend processes both data points and determines successful bidirectional communication...

*   ❌ **When the regions ARE NOT grouped**: ...but incorrectly associates it with region `AAA`'s repeater `AA` (it is the only `AA` it knows of).  A link from that grid square to the incorrect repeater is made.
*   ✅  **When the regions ARE grouped**: ...however, it is aware of two repeaters sharing the ID of `AA`.  Associations ARE NOT made to either repeater as the data is ambiguous.  The map will draw suggestion lines from that grid square to both repeaters and provide signal strength information, which may allow the viewer to make a reasonable assumption on their own as to which repeater was actually involved.

## Administration

Managing a multiregion group is similar to managing a single region, with added capabilities.

### Grouped Admin Panel
Administrators can view data for the entire group or filter by specific sub-regions.
*   **Global Actions**: Tools like "Replace Repeater" or "Bulk Update" can apply to the entire group.
*   **Notes**: Adding a note to a repeater or companion (e.g., "Tom owns this repeater") makes that note visible to all admins in the group, regardless of which specific region the repeater belongs to.

## Requesting a Multiregion Group

As each region in a multiregion group still maintains its own backend databases, regions can be added or removed from multiregion groups easily.  Please reach out to a [Global Administrator](https://wiki.meshmapper.net/administratorlist/) to start the process.