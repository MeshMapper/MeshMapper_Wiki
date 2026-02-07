# Overriding Duplicate ID Detection

MeshMapper's default behavior is to aggressively quarantine repeaters and pings with colliding ID's to ensure map accuracy (see [Duplicate Repeater IDs](https://wiki.meshmapper.net/duplicaterepeaterid/)). However, some regions may prefer to visualize all repeaters and connections, even if the data attribution is technically ambiguous.

The **Disable Duplicate ID Detection Logic** setting allows regions to bypass these safety checks.

!!! danger "Data Integrity Warning"
    Enabling this setting compromises the accuracy of the map and data.
    
    Because the system cannot distinguish between two repeaters sharing the same ID (e.g., `A1`), coverage lines may be drawn to the wrong location, and "Max Range" statistics may be falsely inflated.

## How to Enable

1. Region administrators can log in to the **Admin Portal**.
2. Navigate to the **Settings** tab.
3. Check the box for **Disable Duplicate ID Detection Logic**.
4. Click **Save Settings**.

*Note: If your region is part of a Multi-Region Group, this setting must be enabled by a Master or Global Administrator.*

## Changes to System Behavior

When this mode is active, the system alters its logic in the following ways:

### 1. Map Visualization
*   **Icons:** Repeaters involved in a collision will no longer display the red **Excluded** icon. They will appear as standard Active repeaters (Orange/Grey/Green).
*   **Coverage Lines:** The map will draw connection lines from pings to *all* repeaters that match the ID, even if the ping data is ambiguous.
*   **Neighbor Lines:** Neighbor lines will be drawn for every repeater sharing a colliding ID.
*   **Public Warning:** A warning icon will appear on the public map interface (below the Help button) to inform visitors that the region has opted out of standard validation logic.

### 2. Data Ingestion
*   **Persistence:** The system will no longer automatically force existing repeaters into "Excluded" status when a collision is detected. If you manually set a duplicate repeater to **Active**, it will remain Active.
*   **New Collisions:** To ensure admins are still aware of issues, *newly discovered* repeaters that cause a collision will still default to "Excluded" initially. However, unlike the standard mode, you can manually change them to "Active" without the system reverting your change on the next ping.  Regardless of being "Excluded", the repeater will still function as being "Active".

### 3. Leaderboards
*   **Local Leaderboard:** Duplicate repeaters will be included in the regional "Best Repeaters" and "Max Range" tables.
*   **Global Leaderboard:** To protect the integrity of the global rankings, regions with this setting enabled are **excluded** from the Global Leaderboard. Your repeaters will not appear.

## Summary of Differences

| Feature | Standard Mode | Override Mode |
| :--- | :--- | :--- |
| **Duplicate Repeater Status** | Forced to "Excluded" (Red) | Can be manually set to "Active" |
| **Ambiguous Pings** | Ignored / Not drawn | Drawn to all matching candidates |
| **Neighbor Lines** | Drawn only for unique IDs | Drawn for all colliding IDs |
| **Max Range Stats** | Calculated only for verified unique IDs | Calculated for all IDs (may be inaccurate) |
| **Global Leaderboard** | Included | **Excluded** |