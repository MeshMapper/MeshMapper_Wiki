# Data Upload

MeshMapper allows for the upload of legacy coverage data via CSV upload. This feature is designed to import data collected from other systems.

!!! warning "Administrator Only"
    Due to the complexity of maintaining data integrity, only a MeshMapper Master or Global Administrator can upload legacy data.  [Please reach out to start this process](administratorlist.md).

Uploads are done in the Master Admin panel, on the **Legacy Upload** tab, using the **Legacy Data Upload** card: pick the region, choose the CSV file, map the columns, and use **+ Add Field** for any extra columns.

Each upload goes to one region and **replaces all existing legacy data** for that region. Group maps show their members' legacy data combined.

## CSV Requirements

The uploaded file must be in **CSV** format and contain, at a minimum, the following columns:

*   **Latitude**
*   **Longitude**
*   **Time** - Unix timestamp in seconds or milliseconds, or a standard date string.
*   **Status** - See definitions below

The header names are mapped on the upload form (defaults `lat`, `lon`, `status`, `date`).

You may also include additional columns (e.g. `Repeater`, `RSSI`, `SNR`); each needs a display name. They are stored in the region's legacy database but are not currently shown on the map.

Separately from the CSV, a per-region **Grid Expansion** setting (radius in squares, 0–20, default 1) sets how far each legacy point spreads in Detailed grid mode: 0 = one ~100 m square, 1 = 3×3 (~300 m), 6 = 13×13 (~1.2 km). In Simplified mode each point fills a single 300 m square.

### Status Definitions

The `status` column should contain an integer representing the coverage type, consistent with MeshMapper's standard ping types:

| Value | Type | Colour | Description |
| :--- | :--- | :--- | :--- |
| **0** | **DROP** | **Red** | **Drop** - Failed ping. No repeats heard and did not make it into the wider mesh. |
| **1** | **BIDIR** | **Green** | **Bidirectional** - Confirmed two-way coverage. |
| **2** | **TX** | **Orange** | **Transmit** - Message sent and received into the mesh, but no repeat was heard. |
| **3** | **DEAD** | **Grey** | **Dead** - Repeater heard the ping, but it did not make it into the wider mesh. |
| **5** | **RX** | **Purple** | **Receive** - Heard traffic while in RX mode. |
| **6** | **DISC** | **Cyan** | **Discovery** - Discovery packet sent and reply heard. |
| **7** | **TRACE** | **Cyan** | **Trace** - Targeted trace request sent and reply heard from a specific repeater. Shown the same as DISC. |

Any other status value is drawn red.

## Visualization & Limitations

Legacy data appears on its own map layer, called **Legacy Data**. Legacy squares are never drawn where regular coverage exists.

The **Manage Legacy Databases** card on the same tab lists each region's legacy data, with a **Delete** button.

Unlike standard MeshMapper data, legacy uploads have the following limitations:

*   **No Connection Lines**: Lines connecting the ping to a repeater are not drawn.
*   **No Max Distance Logic**: Statistics for maximum range are not calculated.

### Why?

MeshMapper uses a unique method for storing and processing data that relies on advanced duplicate repeater detection and associating each data point to a specific repeater instance (beyond just the ID). Legacy data often lacks the metadata required to perform these associations accurately.

To prevent skewing the "Best Repeater" leaderboards or creating false associations with duplicate IDs, legacy data is treated as a standalone visual layer.