# Data Upload

MeshMapper allows for the upload of legacy coverage data via CSV upload. This feature is designed to import data collected from other systems.

!!! warning "Administrator Only"
    Due to the complexity of maintaining data integrity, only a MeshMapper Master or Global Administratorcan upload legacy data.  [Please reach out to start this process](https://wiki.meshmapper.net/administratorlist/).

## CSV Requirements

The uploaded file must be in **CSV** format and contain, at a minimum, the following columns:

*   **Latitude**
*   **Longitude**
*   **Time** - Unix timestamp
*   **Status** - See definitions below

A **Coverage Radius** can also be set, which can expand each coverage point beyond the default 300x300 meters.

You may also include any number of additional columns (e.g., `Repeater`, `RSSI`, `SNR`), which will be stored and available for display.

### Status Definitions

The `status` column should contain an integer representing the coverage type, consistent with MeshMapper's standard ping types:

| Value | Type | Color | Description |
| :--- | :--- | :--- | :--- |
| **0** | **DROP** | **Red** | **Drop** - Failed ping. No repeats heard and did not make it into the wider mesh. |
| **1** | **BIDIR** | **Green** | **Bidirectional** - Confirmed two-way coverage. |
| **2** | **TX** | **Orange** | **Transmit** - Message sent and received into the mesh, but no repeat was heard. |
| **3** | **DEAD** | **Grey** | **Dead** - Repeater heard the ping, but it did not make it into the wider mesh. |
| **5** | **RX** | **Purple** | **Receive** - Heard traffic while in RX mode. |
| **6** | **DISC** | **Cyan** | **Discovery** - Discovery packet sent and reply heard. |

## Visualization & Limitations

Legacy data appears on its own layer on the map.

Unlike standard MeshMapper data, legacy uploads have the following limitations:

*   **No Connection Lines**: Lines connecting the ping to a repeater are not drawn.
*   **No Max Distance Logic**: Statistics for maximum range are not calculated.

### Why?

MeshMapper uses a unique method for storing and processing data that relies on advanced duplicate repeater detection and associating each data point to a specific repeater instance (beyond just the ID). Legacy data often lacks the metadata required to perform these associations accurately.

To prevent skewing the "Best Repeater" leaderboards or creating false associations with duplicate IDs, legacy data is treated as a standalone visual layer.