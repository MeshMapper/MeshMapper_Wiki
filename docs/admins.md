# Admin Portal

The **MeshMapper Admin Portal** is a restricted area designed for region maintainers to manage data integrity, configure system settings, and monitor the health of a regions map.

## Access & Permissions

Access to the Admin Portal is strictly controlled. It is not available to general users.

  - **How to get access:** You must reach out to **MrAldersOn** or **CSP-Tom** on Discord to request an account for your region.

## Dashboard & Active Sessions

Upon logging in, the dashboard presents a live view of **Active Sessions**.

  - **Real-time Monitoring:** See who is currently wardriving in your region.
  - **Capacity Management:** Displays the current slot usage (e.g., 2/5 slots).
  - **Kick User:** Admins can forcibly end a session if a user is stuck or consuming a slot unnecessarily.

## Data Management

The portal is divided into several tabs for managing different data types.

### Coverage
This tab allows granular control over individual data points (pings).

  - **Search:** Find pings by User, Time, or Repeater ID.
  - **Edit:** Correct erroneous data (e.g., if a user forgot to flag "External Antenna" or entered the wrong power level).
  - **Delete:** Remove individual bad data points.
  - **Debug:** If "Debug Mode" was enabled during the drive, a **Debug** button appears, allowing admins to inspect the raw JSON payload received from the device.

### Repeaters
Manage the infrastructure database.

  - **Add/Edit:** Manually register repeaters or update their details (Name, Location, Power).
  - **Status Control:**
    - **Active:** Normal operation.
    - **Disabled:** Hidden from map but kept in DB.
    - **Excluded:** Flagged as a duplicate or bad node. Data from this node is ignored.
  - **Ping Calc:** A tool to recalculate the total number of pings a repeater has handled.

### Contacts
Manage the "Phonebook" of known nodes.

  - **Identity:** Map a Public ID (e.g., `12345678...`) to a human-readable Name.
  - **Blocking:** Set a contact's status to **Blocked** to prevent them from uploading data to the map.

### Sessions
A historical log of all wardriving sessions.

  - **Metadata:** View details about the device used (App Version, Hardware Model, etc.).
  - **Cleanup:** Options to delete just the pings from a session (keeping the record) or wipe the session entirely.

## Maintenance Tools

The **Tools** tab contains powerful utilities for bulk operations. **Use with caution.**

  - **Replace Repeater**:
    - Useful when a repeater changes its ID or is replaced by new hardware.
    - Scans the entire database and updates all historical pings to point to the new ID.
  
  - **Bulk Delete Pings**:
    - Remove all data for a specific user or session within a specific time range.

  - **Bulk Update**:
    - Mass-edit attributes for a set of pings.
    - *Example:* Change all pings from user "Tom" on "Dec 25th" to have "External Antenna = YES".

## System Settings

Configure how the map behaves for your region.

  - **Max Session Capacity**: Limit the number of simultaneous wardrivers to prevent mesh congestion.
  - **Hide Contact Names**: Toggle privacy mode for the public map.
  - **Single Observer Mode**: Enable this if your region relies on a single MQTT ingestor to prevent repeaters from being flagged as "Stale" too quickly. This option prevents the repeater from displaying as stale and ultimately getting disabled at 30 days without an advert.
  - **Public Channels**: Define which channels are treated as public traffic.
  - **MQTT Observers**: Configure the list of letsmesh observers to ingest from.
  - **Subscribe to all local observers**: This gives a region the option to either define which observers make up their mesh and exclude everything else (when off), or by toggling this on, listen for packets from any connected observer in the IATA. Turning this off and defining which observers to use could be helpful in cases where someone has fired up an observer and connected it with an IATA, but in reality its far away from the actual region and not contributing to the mesh.
  
## Alerts & History

  - **Alerts**: Automatically detects configuration issues, such as **Duplicate Repeater IDs** (Collisions).
  - **History**: An audit log of all administrative actions (who edited what and when), ensuring accountability.