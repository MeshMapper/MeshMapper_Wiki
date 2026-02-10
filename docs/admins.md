# Admin Portal

The **MeshMapper Admin Portal** is a restricted area designed for region maintainers to manage data integrity, configure system settings, and monitor the health of a regions map.

## Access & Permissions

Access to the Admin Portal is strictly controlled. It is not available to general users.

  - **How to get access:** Reach out to one of the [MeshMapper administrators](https://wiki.meshmapper.net/administratorlist/) to get credentials.

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
    - **Active:** The default state. The repeater is visible on the map, included in leaderboards, and actively associating with coverage pings.
    - **Disabled:** The repeater is hidden from the public map and leaderboards but remains in the database for historical purposes.
    - **Inactive:** The repeater hasn't sent an advert in the last 30 days and has been removed from from the map.
    - **Excluded:** The repeater is flagged as a duplicate. It appears as a **Red** icon on the map. Coverage data is **not** associated with this repeater to prevent skewing statistics (with the exception of **DISCOVERY** type pings).

    !!! warning "Duplicate Repeater Persistence"
        **You cannot force a repeater with a colliding ID to remain Active.**
        
        If a repeater is flagged as **Excluded** due to an ID collision, manually setting it back to **Active** is futile. The moment MeshMapper receives a new advert or ping from that repeater, the collision detection logic will trigger again, and it will immediately revert to **Excluded**.  In addition, setting a repeaters status to **Disabled** does not bypass collision detection logic.
        
        This is a safety mechanism designed to protect the integrity of the map's data. To resolve this, one of the colliding repeaters must change its ID.  If a repeater that was once a duplicate is no longer physically on the mesh, deleting the repeater will ensure collision detection logic will not trigger for surviving repeaters.

  - **Ping Calc:** A tool to recalculate the total number of pings a repeater has handled.

### Contacts
Manage the "Phonebook" of known nodes.

  - **Identity:** Map a Public ID (e.g., `12345678...`) to a human-readable Name.
  - **Blocking:** Set a contact's status to **Blocked** to prevent them from uploading data to the map.

### Sessions
A historical log of all wardriving sessions.

  - **Metadata:** View details about the device used (App Version, Hardware Model, etc.).
  - **Cleanup:** Options to delete just the pings from a session (keeping the record) or wipe the session entirely.

### Users
Manage user identities to group multiple contacts.

  - **Leaderboard Grouping:** Associate multiple contacts/companions under a single User identity. This ensures that all contributions from these devices are aggregated together on the leaderboards.  The name that will display on the leaderboards is that of the selected Main Contact.
  - **Future Functionality:** Currently, this feature is for administrative grouping only. However, plans are in place to expand this into a full Contributor Portal, allowing users to log in, view their personal statistics, and manage the data they have contributed to MeshMapper.  There are some fields (like Username) that exist for this purpose but are not yet implemented.

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
  - **Disable Duplicate ID Detection Logic**: Allows the region to opt-out of MeshMapper's strict duplicate ID collision handling. When enabled, repeaters with colliding IDs will remain active, and pings will associate with all matching repeaters.
    - *Warning:* This compromises data accuracy. A warning badge will be displayed on the public map, and the region will be excluded from global leaderboards.
    - [Learn more about overriding duplicate detection](https://wiki.meshmapper.net/overrideduplicates/)
  
## Alerts & History

  - **Alerts**: Automatically detects configuration issues, such as **Duplicate Repeater IDs** (Collisions).
  - **History**: An audit log of all administrative actions (who edited what and when), ensuring accountability.