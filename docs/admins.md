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
  - **Bulk Select & Delete:** Use the checkboxes on each row (or the "Select All" checkbox in the header) to select multiple pings. A toolbar will appear at the bottom of the screen with an option to **Delete Selected**.

### Repeaters
Manage the repeaters database.

  - **Add/Edit:** Manually register repeaters or update their details (Name, Location, Power).
  - **Status Control:**
    - **Active:** The default state. The repeater is visible on the map, included in leaderboards, and actively associating with coverage pings.
    - **Disabled:** The repeater is hidden from the public map and leaderboards but remains in the database for historical purposes.
    - **Inactive:** The repeater hasn't sent an advert in the last 30 days and has been removed from from the map.
    - **Pending:** The repeater has been discovered but is awaiting approval. Pending repeaters are **not** visible on the map and do not associate with coverage data. This state is only used when the "New Repeaters Enter Pending State" setting is enabled for the region. Admins can approve a pending repeater by editing it and setting its status to **Active**. Pending repeaters that have existed for 3× the stale timer will be automatically approved if still actively being heard, or deleted if not.
    - **Excluded:** The repeater is flagged as a duplicate. It appears as a **Red** icon on the map. Coverage data is **not** associated with this repeater to prevent skewing statistics (with the exception of **DISCOVERY** type pings).

    !!! warning "Duplicate Repeater Persistence"
        **You cannot force a repeater with a colliding ID to remain Active.**
        
        If a repeater is flagged as **Excluded** due to an ID collision, manually setting it back to **Active** is futile. The moment MeshMapper receives a new advert or ping from that repeater, the collision detection logic will trigger again, and it will immediately revert to **Excluded**.  In addition, setting a repeaters status to **Disabled** does not bypass collision detection logic.
        
        This is a safety mechanism designed to protect the integrity of the map's data. To resolve this, one of the colliding repeaters must change its ID.  If a repeater that was once a duplicate is no longer physically on the mesh, deleting the repeater will ensure collision detection logic will not trigger for surviving repeaters.

  - **Ping Calc:** A tool to recalculate the total number of pings a repeater has handled.
  - **Notes:** Clicking the note icon will allow you to optionally add a note to the repeater.  On multiregion admin panels, if a repeater belongs to multiple single regions, notes will be combined and edits will be saved to the individual regions.
  - **Lock GPS Coordinates:** Enabling this setting will prevent new adverts from a repeater from updating its location.  This can be used in instances where the GPS coordinates set on the repeater are incorrect and need to be manually overridden.
  - **Bulk Select & Edit/Delete:** Use the checkboxes on each row (or the "Select All" checkbox in the header) to select multiple repeaters. A toolbar will appear at the bottom of the screen with options to **Edit Selected** or **Delete Selected**. Bulk edit allows you to change Status, Power, Lock GPS, and Notes for all selected repeaters at once — each field has an "Apply" checkbox so you only change the fields you intend to. Works across multi-region admin panels.

    !!! warning "Bulk Notes"
        Bulk editing the Notes field will **overwrite** existing notes for all selected repeaters.

    !!! warning "Data Inaccuracy Warning"

        Enabling "Lock GPS Coordinates" for a repeater that can or will physically move locations will result in inaccurate data.  Use with caution.

!!! info "Blank Name Adverts"
    If a repeater advert is received with a blank or missing name, MeshMapper will silently reject it — no record will be created or updated. This is a data quality safeguard. If a repeater is not appearing on the map despite being active on the mesh, verify that its name is set correctly on the device.

### Companions
Manage the "Phonebook" of known companions.

  - **Identity:** Map a Public ID (e.g., `12345678...`) to a human-readable Name.
  - **Blocking:** Set a companion's status to **Blocked** to prevent them from uploading data to the map.
  - **Notes:** Clicking the note icon will allow you to optionally add a note to the companion.  On multiregion admin panels, if a repeater belongs to multiple single regions, notes will be combined and edits will be saved to the individual regions.
  - **Bulk Select & Edit/Delete:** Same multi-select functionality as repeaters. Bulk edit allows you to change Status and Notes for all selected companions at once.

### Sessions
A historical log of all wardriving sessions.

  - **Metadata:** View details about the device used (App Version, Hardware Model, etc.).
  - **Cleanup:** Options to delete just the pings from a session (keeping the record) or wipe the session entirely.

### Users
Manage user identities to group multiple contacts.

  - **Leaderboard Grouping:** Associate multiple contacts/companions under a single User identity. This ensures that all contributions from these devices are aggregated together on the leaderboards.  The name that will display on the leaderboards is that of the selected Main Companion.
  - **Future Functionality:** Currently, this feature is for administrative grouping only. However, plans are in place to expand this into a full Contributor Portal, allowing users to log in, view their personal statistics, and manage the data they have contributed to MeshMapper.  There are some fields (like Username) that exist for this purpose but are not yet implemented.

### Observers

Monitor the MQTT observers that are feeding data into your region.

#### Summary Cards

Four metric cards are displayed at the top of the tab:

  - **Total**: The total number of unique observers seen.
  - **Online**: Observers that have reported data within the stale threshold (configured in Settings).
  - **Stale**: Observers that have reported within the last 7 days but are beyond the stale threshold.
  - **Offline**: Observers with no activity in the last 7 days.

#### Table Columns

  - **Observer ID**: The unique identifier of the observer node.
  - **Region**: *(Multi-region groups only)* Which sub-region(s) the observer belongs to.
  - **Status**: The observer's current state — **Online** (green), **Stale** (orange), or **Offline** (red).
  - **Last Heard**: How long ago the observer last reported data.
  - **Pings**: The number of coverage pings submitted through this observer.
  - **Repeaters**: The number of repeater adverts heard by this observer.
  - **Companions**: The number of companion adverts observed.
  - **LetsMesh MQTT**: Indicates whether this observer has contributed data via the LetsMesh broker.
  - **MeshMapper MQTT**: Indicates whether this observer has contributed data via the MeshMapper in-house broker.

!!! info "MQTT Brokers"
    Only 1 broker per observer is required to submit data to MeshMapper.  Data received from both brokers will aggregate.

  - **Notifications**: A toggle to mute or unmute offline Discord notifications for this observer. Muting suppresses notifications only — data collection is unaffected.

!!! info "Observer Data Source"
    Observer data is aggregated from coverage, repeater, and companion records over the last 30 days. Observers will appear here automatically once they begin reporting data.

### Administrators

The **Administrators** tab displays all admin accounts that have been granted access to your region and allows you to invite new administrators.

  - **Name:** The username of the administrator account.
  - **Contact:** The contact information on file for the administrator (e.g., Discord handle, email).
  - **Region:** On multiregion admin panels, each administrator's entry will display which sub-regions they have been granted access to.
  - **Status:** Indicates whether the administrator has completed registration.
      - **Active:** The administrator has claimed their account and set a key.
      - **Pending Registration:** The administrator has been invited but has not yet claimed their account.

#### Adding a New Administrator

Region admins can invite new administrators directly from this tab by clicking **+ Add Administrator**.

  1. **Username** *(required)*: Choose a username for the new administrator. As you type, the system will check if the username already exists. If the administrator already has an account, a notice will appear and the form will switch to "Grant Access" mode — submitting will add your region to their existing access instead of creating a new account.
  2. **Contact Info** *(required)*: Enter the new administrator's contact information (e.g., Discord handle or email) so they can be reached if needed. If the username already exists, this field will auto-populate with their current contact info.
  3. **Region Assignment** *(required)*: Select which region the new administrator should have access to. On multiregion admin panels, you can assign the administrator to the multi-region group or to an individual sub-region.

For **new administrators**, a message will display with a registration link and the username. Share both with the new administrator. For **existing administrators**, a confirmation will display that access to the region has been granted — no registration link is needed.

#### Registration

New administrators claim their account by visiting [register.meshmapper.net](https://register.meshmapper.net) and entering the username provided to them. If the account exists and has not yet been registered, a **temporary key** will be generated and displayed.

!!! warning "Temporary Key"
    The temporary key is shown **only once** during registration. The new administrator must copy it immediately. After logging in for the first time, they should change their key from the **User Settings** tab.

## Maintenance Tools

The **Tools** tab contains powerful utilities for bulk operations. **Use with caution.**

  - **Replace Repeater**:
    - Useful when a repeater changes its ID or is replaced by new hardware.
    - Scans the entire database and updates all historical pings to point to the new ID.
  
  - **Bulk Delete Pings**:
    - Remove all data for a specific companion or session within a specific time range.

  - **Bulk Update**:
    - Mass-edit attributes for a set of pings.
    - *Example:* Change all pings from companion "Tom_Mobile" on "Dec 25th" to have "External Antenna = YES".

  - **Reassociate Repeater**:
    - Reassociate pings to a repeater that was missing from the map at the time of ingestion, or whose GPS coordinates were incorrect.
    - Select a repeater and click "Analyze & Preview" to see how many pings would be affected. The tool detects ID collisions automatically — if the repeater's short ID collides with another active repeater, only DISC pings (matched by full public key) will be processed.
    - Pings that already have the correct coordinates (within ~100m) are skipped.

    !!! warning "Use With Caution"
        Reassociating pings to the wrong repeater location will result in misrepresented data. Always verify the repeater's GPS coordinates are correct before running this tool.

## System Settings

Configure how the map behaves for your region.

  - **Max Session Capacity**: Limit the number of simultaneous wardrivers to prevent mesh congestion.
  - **Hide Companion Names**: Toggle privacy mode for the public map.
  - **Stale Repeater Age**: Set how many hours without an advert before a repeater is considered stale and visually flagged on the map (default: 24 hours). This threshold also drives the automatic duplicate cleanup routine — a colliding repeater that has not been heard in **3× this value** is eligible for automatic deletion. For example, with a 12-hour stale age, stale duplicates are removed after 36 hours of silence. [See Duplicate Repeater IDs](https://wiki.meshmapper.net/duplicaterepeaterid/)
  - **New Repeaters Enter Pending State**: When enabled, newly discovered repeaters will enter a **Pending** state instead of **Active**. Pending repeaters are hidden from the map until an admin reviews and approves them. After 3× the stale timer, pending repeaters are automatically approved if still actively being heard, or deleted if not. In multiregion mode, this setting is configured per-region under Region-Specific Settings.

    !!! warning "Data Inaccuracy Warning"
        New repeaters will not display on the map until approved. This can cause data inaccuracies. Use with caution.

  - **Hop Bytes**: Configure the region's repeater identification byte length — 1-byte (256 IDs), 2-byte (65K IDs), or 3-byte (16M IDs). When set to 2 or 3-byte, companion devices connecting to wardrive sessions are automatically configured to use the enforced hop byte length. In 1-byte regions, MeshMapper passively detects which repeaters support multi-byte by watching packets and only confirmed repeaters will show multi-byte IDs on the map. Collision detection, coverage mapping, and leaderboards all respect the configured hop byte length. Requires MeshCore firmware v1.14.0+.
  - **Single Observer Mode**: Enable this if your region relies on a single MQTT ingestor to prevent repeaters from being flagged as "Stale" too quickly. This option prevents the repeater from displaying as stale and ultimately getting disabled at 30 days without an advert.
  - **Public Channels**: Define which channels are treated as public traffic.
  - **Regions/Scopes**: If your region uses MeshCore Regions/Scopes, define it here.  If not, leave the default scope of "*".
  - **Enforce Hybrid Mode**: Disables Active mode for wardrivers in your region.  If your regions mesh has an issue with dropped packets due to high mesh traffic or many wardrivers, consider enabling this option.  *(Mobile app functionality will be available with v1.1.0)*
  - **Consider Failed DISC as DROP**: When disabled, Discovery pings that do not receive a reply will not appear on the map.  When enabled, Discovery pings that do not will receive a reply will display as DROP (red) on the map.
  - **Minimum Active/Hybrid Mode Interval**: Optionally set the number of seconds between mesh pings for wardrivers in your region.  If your regions mesh has an issue with dropped packets due to high mesh traffic or many wardrivers, consider setting a higher minimum interval.  *(Mobile app functionality will be available with v1.1.0)*
  - **Region Message**: Optionally add a message here that will display to map visitors when they click the "Region Info" option.  Direct guests to your Discord server, website, etc.  Field is plain-text and will automatically convert URLs to clickable links.
  - **Social Media Links**: Optionally add any number of social media or website links that will display on the "Region Info" window on your regions map.
  - **MQTT Observers**: Configure the list of letsmesh observers to ingest from.
  - **Subscribe to all local observers**: This gives a region the option to either define which observers make up their mesh and exclude everything else (when off), or by toggling this on, listen for packets from any connected observer in the IATA. Turning this off and defining which observers to use could be helpful in cases where someone has fired up an observer and connected it with an IATA, but in reality its far away from the actual region and not contributing to the mesh.
  - **Disable Duplicate ID Detection Logic**: Allows the region to opt-out of MeshMapper's strict duplicate ID collision handling. When enabled, repeaters with colliding IDs will remain active, and pings will associate with all matching repeaters.
    - *Warning:* This compromises data accuracy. A warning badge will be displayed on the public map, and the region will be excluded from global leaderboards.
    - [Learn more about overriding duplicate detection](https://wiki.meshmapper.net/overrideduplicates/)

### Region Boundary

The **Region Boundary** section allows you to view and edit the geographic boundary of your region.

  - **Draw Polygon**: Use the **Polygon Tool** to draw or redraw the region boundary directly on the map.
  - **Import GeoJSON**: Click the **Import GeoJSON** button to paste GeoJSON data from an external source (e.g., [geojson.io](https://geojson.io)). Supported formats include `Polygon`, `MultiPolygon`, `Feature`, and `FeatureCollection`.
  - **Center Pin**: The center pin automatically moves to the center of the polygon when one is drawn or imported. You can also drag it manually. This determines where the region appears on the global map.
  - **Lat / Lon / Radius**: The latitude, longitude, and radius fields are used as a fallback if no polygon is defined. If a polygon is drawn, it takes precedence over the radius.

## User Settings

The **User Settings** tab allows administrators to manage their own account.

  - **Change Key**: Update your admin login key.
  - **Contact Info**: Update your contact information (e.g., Discord handle, email). This is displayed to all users.

## Alerts & History

  - **Alerts**: Automatically detects configuration issues, such as **Duplicate Repeater IDs** (Collisions) and **Pending Repeaters** awaiting approval.
  - **History**: An audit log of all administrative actions (who edited what and when), ensuring accountability.

## Notifications

Link your Discord to MeshMapper to receive DM's from the MeshMapper bot.

  - **Alert on Duplicate Repeater ID**: Notifies you when a repeater has sent an advert, but its ID collides with another, putting both repeaters into Excluded status.  [See Duplicate Repeater ID](https://wiki.meshmapper.net/duplicaterepeaterid)
  - **Alert on Pending Repeater**: Once a day, receive a notification if your region has repeaters in **Pending** state that are awaiting review.  This notification is only relevant if "New Repeaters Enter Pending State" is enabled for the region.
  - **Allow Messages From Visitors**: When enabled, a map visitor can send a message to you directly from the "Region Info" page of your regions map.
  - **Alert on Offline Observer**: Once a day (around 0800 EST/EDT) MeshMapper will review all data received via your regions MQTT observers (pings, repeater adverts, companion adverts) for the past 7 days.  If a particular observer has sent data within that time, but not within the "Stale Repeater Age" time configured for your region, then this observer is potentially offline.  Receive an alert when this is the case.