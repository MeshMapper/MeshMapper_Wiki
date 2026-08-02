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

  - **Add/Edit:** Manually register repeaters or update their details (Name, Location, Power, Hop Bytes).
  - **Status Control:**
    - **Active:** The default state. The repeater is visible on the map, included in leaderboards, and actively associating with coverage pings.
    - **Disabled:** The repeater is hidden from the public map and leaderboards but remains in the database for historical purposes.
    - **Inactive:** The repeater hasn't sent an advert within the region's **Repeater Inactive After** window (default 30 days) and has been removed from the map. This is non-destructive — the record is retained and returns to Active automatically the next time the repeater adverts and an observer relays it to MeshMapper. Wardrive pings alone will not bring it back. See [Repeater Lifecycle & Data Cleanup](#repeater-lifecycle-data-cleanup).
    - **Pending:** The repeater has been discovered but is awaiting approval. Pending repeaters are **not** visible on the map and do not associate with coverage data. This state is only used when the "New Repeaters Enter Pending State" setting is enabled for the region. Admins can approve a pending repeater by editing it and setting its status to **Active**. Once a pending repeater has existed for 3× the stale timer it is resolved automatically — approved if it has been heard within 1× the stale timer, deleted if it has not. See [Pending repeater resolution](#pending-repeater-resolution).
    - **Excluded:** The repeater is flagged as a duplicate. It appears as a **Red** icon on the map. Coverage data is **not** associated with this repeater to prevent skewing statistics (with the exception of **DISCOVERY** type pings).

    !!! warning "Duplicate Repeater Persistence"
        **You cannot force a repeater with a colliding ID to remain Active.**
        
        If a repeater is flagged as **Excluded** due to an ID collision, manually setting it back to **Active** is futile. The moment MeshMapper receives a new advert or ping from that repeater, the collision detection logic will trigger again, and it will immediately revert to **Excluded**.  In addition, setting a repeaters status to **Disabled** does not bypass collision detection logic.
        
        This is a safety mechanism designed to protect the integrity of the map's data. To resolve this, one of the colliding repeaters must change its ID.  If a repeater that was once a duplicate is no longer physically on the mesh, deleting the repeater will ensure collision detection logic will not trigger for surviving repeaters.

  - **Ping Calc:** A tool to recalculate the total number of pings a repeater has handled.
  - **Neighbours Cleanup:** Reset the neighbours list for any repeater in the region. Useful for clearing stale or incorrect neighbour associations.
  - **Notes:** Clicking the note icon will allow you to optionally add a note to the repeater.  On multiregion admin panels, if a repeater belongs to multiple single regions, notes will be combined and edits will be saved to the individual regions.
  - **Lock GPS Coordinates:** Enabling this setting will prevent new adverts from a repeater from updating its location.  This can be used in instances where the GPS coordinates set on the repeater are incorrect and need to be manually overridden.
  - **Bypass Auto Delete:** When enabled on a repeater, every automatic cleanup routine will skip it entirely. The repeater will not be marked inactive, will not be deleted as a stale duplicate, will not be removed as a stale pending repeater, and will not be removed by the [Repeater Retention / Auto-Delete](#repeater-retention-auto-delete-days) purge. This is useful for repeaters that are known to be offline for extended periods but should remain on the map (e.g. seasonal deployments, repeaters in remote locations with intermittent connectivity).
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
  - **Remove**: Administrators can remove stale or inactive observers from the list.  Note that if the observer starts sending packets again, it will automatically be re-added.

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

  1. **Username** *(required)*: Choose a username for the new administrator. If the administrator already has an account, a notice will appear and the form will switch to "Grant Access" mode — submitting will add your region to their existing access.
  2. **Contact Info** *(required)*: Enter the new administrator's contact information (e.g., Discord handle or email).
  3. **Region Assignment** *(required)*: Select which region the new administrator should have access to. On multiregion admin panels, you can assign the administrator to the multi-region group or to an individual sub-region.

For **new administrators**, an invite link will be generated. Copy the link and send it to the new administrator. Invite links expire after **7 days**. For **existing administrators**, a confirmation will display that access to the region has been granted — no invite link is needed.

Pending invites are displayed below the administrators table, showing the username, region, who sent the invite, and when it expires. Invites can be deleted before they are claimed.

#### Registration

New administrators claim their account by visiting the invite link sent to them. The link opens a confirmation page showing their username, assigned region, and who invited them. Clicking **Accept Invite & Create Account** generates their password.

!!! warning "Password"
    The password is shown **only once** during registration. The new administrator must copy it immediately. After logging in for the first time, they can change their password from the **User Settings** tab.

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

The Settings tab is organised into collapsible blocks. Everything that ages, hides, or deletes data lives together under **Repeaters & Data Integrity** — see [Repeater Lifecycle & Data Cleanup](#repeater-lifecycle-data-cleanup) below for the full walkthrough of those timers.

  - **Max Session Capacity**: Limit the number of simultaneous wardrivers to prevent mesh congestion.
  - **Disable All Flood Traffic**: Disables Active and Hybrid modes in the mobile app entirely — users in your region can only passively wardrive. When enabled, Max Session Capacity is forced to 0 and greyed out.
  - **Hide Companion Names**: Toggle privacy mode for the public map. Also disables the companion filter for map traffic — the public map's Filter → User field is shown disabled with an explanation.
  - **Hop Bytes**: Configure the region's repeater identification byte length — 1-byte (256 IDs), 2-byte (65K IDs), or 3-byte (16M IDs). When set to 2 or 3-byte, companion devices connecting to wardrive sessions are automatically configured to use the enforced hop byte length. In 1-byte regions, MeshMapper passively detects which repeaters support multi-byte by watching packets and only confirmed repeaters will show multi-byte IDs on the map. Collision detection, coverage mapping, and leaderboards all respect the configured hop byte length. Changing the byte mode automatically recalculates repeater collisions and updates affected repeaters to Active status. Requires MeshCore firmware v1.14.0+.
  - **Single Observer Mode**: Enable this if your region relies on a single MQTT ingestor to prevent repeaters from being flagged as "Stale" too quickly. A region in Single Observer Mode is skipped entirely by the nightly repeater cleanup — repeaters are never marked stale, never marked inactive, and never auto-deleted. (Ghost cleanup still runs, since it only touches the heard-only catalog.)
  - **Public Channels**: Define which channels are treated as public traffic.
  - **Regions/Scopes**: If your region uses MeshCore Regions/Scopes, define it here.  If not, leave the default scope of "*".
  - **Enforce Hybrid Mode**: Disables Active mode for wardrivers in your region.  If your regions mesh has an issue with dropped packets due to high mesh traffic or many wardrivers, consider enabling this option.  *(Mobile app functionality will be available with v1.1.0)*
  - **Consider Failed DISC as DROP**: When disabled, Discovery pings that do not receive a reply will not appear on the map.  When enabled, Discovery pings that do not will receive a reply will display as DROP (red) on the map.
  - **Minimum Active/Hybrid Mode Interval**: Optionally set the number of seconds between mesh pings for wardrivers in your region.  If your regions mesh has an issue with dropped packets due to high mesh traffic or many wardrivers, consider setting a higher minimum interval.  *(Mobile app functionality will be available with v1.1.0)*
  - **Region Message**: Optionally add a message here that will display to map visitors when they click the "Region Info" option.  Direct guests to your Discord server, website, etc.  Field is plain-text and will automatically convert URLs to clickable links.
  - **Social Media Links**: Optionally add any number of social media or website links that will display on the "Region Info" window on your regions map.
  - **MQTT Observers**: Configure the list of letsmesh observers to ingest from.
  - **Subscribe to all local observers**: This gives a region the option to either define which observers make up their mesh and exclude everything else (when off), or by toggling this on, listen for packets from any connected observer in the IATA. Turning this off and defining which observers to use could be helpful in cases where someone has fired up an observer and connected it with an IATA, but in reality its far away from the actual region and not contributing to the mesh.

### Repeater Lifecycle & Data Cleanup

Everything that ages, hides, or deletes data lives in the **Repeaters & Data Integrity** block of the Settings tab. A repeater goes quiet, gets flagged, gets hidden, and — only if you opt in — eventually gets deleted.

Cleanup runs once a night, so changes you save here take effect on the next run rather than immediately.

!!! warning "\"Heard\" means an advert, not a wardrive"
    These timers only reset when the repeater sends an **advert that reaches MeshMapper through an MQTT observer**.

    Wardriving past a repeater records its pings normally, but does **not** reset its clock — it will still go stale, go Inactive, and be deleted on schedule. A repeater that is transmitting fine but has no observer in range will age off the map anyway. If repeaters vanish unexpectedly, check the [Observers](#observers) tab first.

    Ghosts are the exception — they run on wardrive discovery. See [Ghost Retention](#ghost-retention-days).

#### The lifecycle at a glance

Defaults, for a repeater that stops adverting at **day 0**:

| Elapsed | What happens | Setting |
| --- | --- | --- |
| 24 hours | Flagged **stale** on the map. Still Active, still collects pings. | Stale Repeater Age |
| 72 hours | Deleted **only if another repeater still shares its ID**. A unique ID is untouched. | Stale Repeater Age × 3 |
| 30 days | Marked **Inactive** and hidden from the map. Reversible — returns to Active when it adverts again. | Repeater Inactive After |
| Never | Permanently deleted. **Off by default.** | Repeater Retention / Auto-Delete |

Ghosts and orphaned pings run on separate clocks: ghosts age out after 30 days, and orphaned pings are kept forever unless you enable Stale Ping Cleanup.

Pending repeaters aren't on this timeline at all — see [Pending repeater resolution](#pending-repeater-resolution).

#### Stale Repeater Age (Hours)

**Default: 24. Always on. Non-destructive.**

Hours without an advert before a repeater is flagged stale on the map. It stays Active and still collects pings — this is a visual warning only.

The value also sets the **3×** threshold (72 hours by default) used by the two routines below.

Lower it for a map that reacts quickly to outages; raise it if your repeaters advert infrequently and healthy ones keep getting flagged.

##### Duplicate collision cleanup

After 3× the stale age of silence, a repeater is deleted **only if another repeater still shares the leading bytes of its ID**. Silence alone never deletes anything here — a repeater with a unique ID simply carries on toward Inactive.

If exactly one other repeater shared that ID and the collision had forced it into **Excluded**, it is restored to **Active** with the clean ID. Collisions blocking a legitimate repeater fix themselves once the stale twin is gone.

[See Duplicate Repeater IDs](https://wiki.meshmapper.net/duplicaterepeaterid/).

##### Pending repeater resolution

Applies only when **New Repeaters Enter Pending State** is on. This clock starts when the repeater was first added, not when it went quiet.

Once a pending repeater is **3× the stale age** old, MeshMapper decides based on whether it adverted within **1×** the stale age:

  - **Adverted recently** → approved to Active.
  - **Hasn't** → deleted.

!!! example
    With Stale Repeater Age = 24h, pending repeaters are judged at 72 hours old:

      - Added Monday, still adverting Thursday → **approved**.
      - Added Monday, went silent Tuesday → **deleted**.
      - Added yesterday → not judged yet, whatever it's doing.

    The two numbers differ on purpose: 72h decides *when* it's judged, 24h decides *which way*.

A repeater with **Bypass Auto Delete** is never deleted here, but can still be auto-approved.

#### Repeater Inactive After (Days)

**Default: 30. Always on. Non-destructive.**

Days without an advert before a repeater is marked **Inactive** and hidden from the map.

Nothing is lost — the record, its notes, its history, and its leaderboard contributions all stay. It returns to Active by itself the next time an advert gets through.

Configurable per region (previously fixed at 30 days).

!!! example
    Raise it to **60** for a repeater whose adverts only occasionally reach an observer, giving it two months to land one. Lower it to **14** for a dense region that wants stale entries off the map quickly.

!!! warning "This won't help a repeater with no observer coverage"
    Raising the value only helps if adverts get through *sometimes*. If no observer can hear the repeater at all it ages out regardless, and its wardrive pings won't stop that. That's an observer gap, not a timer problem. (**Single Observer Mode** disables this ageing entirely.)

!!! tip "Per-repeater override"
    **Bypass Auto Delete** on a repeater (Repeaters tab) exempts it from every routine in this section. Use it for seasonal or knowingly-offline deployments you want to keep on the map.

#### Repeater Retention / Auto-Delete (Days)

**Default: blank (Disabled). Opt-in. DESTRUCTIVE.**

!!! danger "This permanently deletes repeaters"
    An Inactive repeater that hasn't adverted for this many days is **permanently deleted**. Recovery is only from a nightly backup. **Leave it blank to keep it off** — that's the default, and most regions should keep it there.

    A repeater with no observer in range looks identical to a dead one here. Enabling this in a region with patchy observer coverage will delete repeaters that are still transmitting.

It exists for regions accumulating dead records — test devices, replaced hardware — that want the database pruned without doing it by hand.

**The clock runs from the last advert**, not from the day the repeater went Inactive, so the two windows overlap.

!!! example
    Inactive After = **30**, Retention = **90**. A repeater last adverts January 1st:

      - **January 31st** — marked Inactive, hidden from the map. Record intact.
      - **April 1st** — permanently deleted.

    So it was recoverable for 60 days, not 90. Set both to 30 and it's marked Inactive and deleted on the same night.

**Minimum:** your **Repeater Inactive After** value, or 7 days, whichever is larger — a repeater can't be deleted before it's marked Inactive. The minimum shown next to the field updates as you type. **A smaller value is rejected outright and auto-delete stays off.** It is not rounded up.

Leaderboard points and Explorer credit survive; only the repeater record goes. Deletions are written to the audit log.

Nothing is deleted until the MeshMapper operator enables the purge fleet-wide — setting a value alone isn't enough.

#### Ghost Retention (Days)

**Default: 30. Always on.**

A **ghost** is a device that has only ever been heard passively — it answered a wardriver's discovery ping but never sent an advert. With no advert it has no name and no fixed location, so it never appears on the map. Ghosts are kept in a separate catalog as evidence that *something* with that ID is transmitting nearby.

This setting drops a ghost after this many days without being heard. Ghosts are also removed as soon as the same ID registers as a real repeater, regardless of the timer.

That catalog is what makes [Pending Repeater Links](#pending-repeater-links) work — a local ghost sharing a distant repeater's ID is the evidence that the pings belong to the local device. Set it too low and you lose that evidence.

!!! example
    An unregistered repeater `C4A8…` answers discovery 40 times but never adverts. It's logged as a ghost and used as evidence for any pending-link decision on that ID. If nobody hears it for 30 days the ghost is dropped. If its owner fixes it and it starts adverting, it becomes a real repeater and the ghost is removed on the next nightly run.

!!! info
    Ghost cleanup only touches the ghost catalog — it can never delete or modify a registered repeater.

#### Pending Link Distance (km)

**Default: 200. 0 disables. Affects new pings only.**

When a wardriver hears a repeater, their radio reports a short ID — often only one or two bytes. If that resolves to exactly one registered repeater, MeshMapper normally links the ping to it.

The problem: an **unregistered** local repeater can share a short ID with a registered one on the far side of the country, and every ping it generates gets credited to the distant repeater — drawing coverage lines hundreds of kilometres long.

So if the matching repeater is farther away than this many km, the link isn't drawn. The pings are held as a **Pending Repeater Link** in the Alerts tab for you to confirm or reject. They stay on the map, just not tied to a repeater.

!!! example
    At the default 200 km:

      - An Ottawa wardriver hears `C4`, which resolves to a repeater in Vancouver 3,500 km away → held for review.
      - Hears `9F`, resolving to a repeater 40 km away → linked automatically.
      - A genuine mountaintop link at 215 km → held once; confirm it and future pings link automatically.

!!! question "Why 200?"
    Real LoRa long-hauls reach about 220 km. Past that, a handheld hearing a repeater almost always means an unregistered local device with the same short ID. A false alert costs one click; a missed one puts a wrong line on the map permanently.

Lower it in a compact region to catch more collisions at the cost of more alerts; raise it if you genuinely have extreme long-haul links. **0** disables the check and always auto-links.

Changing it affects new pings only — existing data and existing alerts are untouched.

See [Pending Repeater Links](#pending-repeater-links) for how to resolve the alerts it generates.

#### Stale Ping Cleanup (Auto-Delete Orphaned Pings)

**Default: Disabled. Options: Disabled / 30 / 60 / 90 days. DESTRUCTIVE.**

Ages out **orphaned** pings — ones whose repeater has moved more than 100 m away or vanished entirely. These are the pings the map already shows as **"(Gone)"**. A ping only counts as orphaned when *every* repeater on it is gone; anything still resolving is kept.

##### The grace clock

**Choosing a window does not delete your existing backlog.** This is the part people misread.

The nightly job starts a clock the first night it sees a ping orphaned, and only deletes it once it has stayed orphaned for the full window. If the repeater comes back within 100 m, the clock clears and the ping is kept.

!!! example
    You pick **30 days** on June 1st, and you have pings orphaned since last year.

      - **June 1st** — they're flagged and the clock starts. Nothing is deleted.
      - **July 1st** — 30 days orphaned. *Now* they're deleted.

    A repeater returning on June 20th resets the clock and its pings are kept — unless it comes back more than 100 m from where it was.

Leaderboard points and Explorer credit are preserved; only the ping record is removed.

##### Backfill Purge Now…

The immediate alternative — it doesn't wait out the clock. It deletes every ping that is **already** orphaned **and** older than your saved window, plus any no-location (0,0) pings of any age. Anything orphaned more recently than the window is kept, so a briefly-offline repeater doesn't lose data.

  1. Save a window (30 / 60 / 90) first — the preview won't run without one.
  2. Click **Backfill Purge Now…** to open a read-only preview.
  3. Review what would go: totals, a breakdown by repeater with the reason each qualifies, and one by date. Multi-region groups also get a per-region breakdown.
  4. Confirm the exact ping count.

!!! example
    Window = 30 days, run on June 1st:

      - January ping, orphaned → **deleted**.
      - May 25th ping, orphaned → **kept** (inside the window; the repeater may only be briefly offline).
      - March ping at 0,0 → **deleted** (no-location pings go at any age).
      - January ping whose repeater is still live nearby → **kept** (not orphaned).

Use it to clear a backlog now instead of waiting for each ping to age out.

!!! info
    The nightly sweep won't run with a window under 30 days, which is why there's no shorter option. And like the repeater purge, real deletion is blocked until the MeshMapper operator enables it fleet-wide — until then both the nightly job and this button only *mark* pings, and the preview will tell you so.

With the **Ping Purge Cleanup Report** notification on, you'll get a Discord DM summarising what was removed (one combined message per group).

#### New Repeaters Enter Pending State

When enabled, newly discovered repeaters will enter a **Pending** state instead of **Active**. Pending repeaters are hidden from the map until an admin reviews and approves them, and are resolved automatically once they have been in the queue for 3× the stale timer — see [Pending repeater resolution](#pending-repeater-resolution) for exactly how that decision is made. In multiregion mode, this setting is configured per-region under Region-Specific Settings.

!!! warning "Data Inaccuracy Warning"
    New repeaters will not display on the map until approved. This can cause data inaccuracies. Use with caution.

#### Disable Duplicate ID Detection Logic

Allows the region to opt-out of MeshMapper's strict duplicate ID collision handling. When enabled, repeaters with colliding IDs will remain active, and pings will associate with all matching repeaters.

  - *Warning:* This compromises data accuracy. A warning badge will be displayed on the public map, and the region will be excluded from global leaderboards.
  - [Learn more about overriding duplicate detection](https://wiki.meshmapper.net/overrideduplicates/)

#### Multi-region groups

Some of these are set once for the whole group, others per region.

**Group-wide** (Multi-Region Settings → Group Defaults):

  - Stale Repeater Age
  - Pending Link Distance
  - Stale Ping Cleanup — including Backfill Purge, which runs across every member region

**Per region**, on each member's own settings:

  - Repeater Inactive After
  - Repeater Retention / Auto-Delete
  - Ghost Retention

Open a member region and the group-controlled fields are greyed out — the group's value wins, so change them from the group panel. Where a group hasn't set a value, the region's own applies; if neither has, the default does.

### Region Boundary

The **Region Boundary** section allows you to view and edit the geographic boundary of your region.

  - **Draw Polygon**: Use the **Polygon Tool** to draw or redraw the region boundary directly on the map.
  - **Import GeoJSON**: Click the **Import GeoJSON** button to paste GeoJSON data from an external source (e.g., [geojson.io](https://geojson.io)). Supported formats include `Polygon`, `MultiPolygon`, `Feature`, and `FeatureCollection`.
  - **Center Pin**: The center pin automatically moves to the center of the polygon when one is drawn or imported. You can also drag it manually. This determines where the region appears on the global map.
  - **Lat / Lon / Radius**: The latitude, longitude, and radius fields are used as a fallback if no polygon is defined. If a polygon is drawn, it takes precedence over the radius.
  - **Auto Generate Boundry**: Use this option to have AI attempt to draw your regions boundry for you.

## User Settings

The **User Settings** tab allows administrators to manage their own account.

  - **Change Key**: Update your admin login key.
  - **Contact Info**: Update your contact information (e.g., Discord handle, email). This is displayed to all users.
  - **API Access**: Generate or manage your Coverage API key. Each admin is allowed one key per region with a fixed rate limit of 100 requests per day. A description/reason is required when generating a key. Use **Regenerate** to replace an existing key (the old key stops working immediately). See [Coverage API](coverage-api.md) for usage details.

## Alerts & History

  - **Alerts**: Automatically detects configuration issues, including:
      - **Repeater Clock Alerts**: Repeaters whose embedded timestamp differs from the server time by more than 120 seconds. An incorrect clock can affect packet routing and deduplication.
      - **Duplicate Repeater IDs** (Collisions): Multiple repeaters sharing the same short public ID.
      - **Pending Repeaters**: Repeaters awaiting approval (when "New Repeaters Enter Pending State" is enabled).
      - **Pending Repeater Links**: Pings held for review because the repeater they resolve to is implausibly far away — see below.
      - **Suspicious Live Sessions**: Sessions containing pings whose implied speed between consecutive fixes exceeds the flyover threshold — typically a device that was flown, or otherwise moved faster than any ground vehicle. Each row shows who, session ID, start time, peak speed, and ping count. You can **delete** the session to scrub the pings, or **dismiss** it if the movement was legitimately fast (a train, for example). Dismissed sessions are kept in a collapsed list so the decision is reviewable.
  - **History**: An audit log of all administrative actions (who edited what and when), ensuring accountability.

### Pending Repeater Links

Generated by the [Pending Link Distance](#pending-link-distance-km) setting: a ping's repeater ID resolved to exactly one registered repeater, but it sits farther away than your configured distance.

The pings **stay on the map** — they're just not tied to a repeater until you decide. Nothing is deleted or hidden.

#### Reading the evidence

Each row gives you what you need to decide:

  - **The resolved repeater** — ID, name, region, and distance.
  - **What was actually heard on-air** — the short token the radio really reported. It's often shorter than the resolved ID, and that's the crux: the extra bytes came from MeshMapper's resolution, not from the radio.
  - **Nearby ghosts** — unregistered devices answering discovery in the area. **Strong matches** start with the exact token that was heard; if one exists, the pings almost certainly belong to it and the panel says so. **Weak matches** share only the first byte and are de-emphasised.
  - **The held pings** — date, session, heard token, coordinates, and a **🗺️ Map** link to that exact ping.

#### Your three choices

  - **Link to repeater** — you know that repeater genuinely reaches this area. The pings link to its current position, and future far pings for this ID link automatically.
  - **Leave unlinked** — the likely case. Pings stay on the map, marked as tied to no repeater. New far pings will alert again.
  - **Leave unlinked + suppress** — same, but future far pings are held quietly with no new alert. Use it once you've confirmed there's a local unregistered device.

With more than one row you also get **Suppress all**. Suppressed IDs sit in their own list with held-ping counts and can be restored individually or all at once.

!!! info "Suppression clears itself"
    MeshMapper watches the situation around each ID. If a local repeater with that ID registers, the distant one moves or is deleted, or a new ghost appears, suppression clears and you're alerted again. Same for a confirmed link.

!!! warning "When linking is refused"
    - **Unplaced repeater** — it has no usable position, so linking would bake the pings to a meaningless location. Place it on the map first.
    - **Newly ambiguous** — more than one repeater now matches that ID, so linking would be a guess. Review that ID's repeaters first.

Admins with the **Pending Repeater Link** notification on get a daily reminder. Each ID notifies once, resetting if its situation changes.

## Notifications

Link your Discord to MeshMapper to receive DM's from the MeshMapper bot.

  - **Alert on Duplicate Repeater ID**: Notifies you when a repeater has sent an advert, but its ID collides with another, putting both repeaters into Excluded status.  [See Duplicate Repeater ID](https://wiki.meshmapper.net/duplicaterepeaterid)
  - **Alert on Pending Repeater**: Once a day, receive a notification if your region has repeaters in **Pending** state that are awaiting review.  This notification is only relevant if "New Repeaters Enter Pending State" is enabled for the region.
  - **Allow Messages From Visitors**: When enabled, a map visitor can send a message to you directly from the "Region Info" page of your regions map.
  - **Alert on Offline Observer**: Once a day (around 0800 EST/EDT) MeshMapper will review all data received via your regions MQTT observers (pings, repeater adverts, companion adverts) for the past 7 days.  If a particular observer has sent data within that time, but not within the "Stale Repeater Age" time configured for your region, then this observer is potentially offline.  Receive an alert when this is the case.
  - **Suspicious Flight**: Alerts you when a live session contains pings implying a speed faster than any ground vehicle — usually a device that was flown. Corresponds to the **Suspicious Live Sessions** alert.
  - **Pending Repeater Link**: Once a day, a summary of repeater IDs whose pings are held for review because they resolved to an implausibly distant repeater. Each ID notifies once, and again only if its situation changes. See [Pending Repeater Links](#pending-repeater-links).
  - **Ping Purge Cleanup Report**: A summary of what [Stale Ping Cleanup](#stale-ping-cleanup-auto-delete-orphaned-pings) removed — ping count, plus a breakdown by date and repeater. Multiregion groups get one combined message. Only sent when something was actually deleted.

These events are also available as **webhook** subscriptions, configured separately in the Settings tab. See [Webhooks](https://wiki.meshmapper.net/webhooks/).

Webhooks can also be configured per-region to send these same notifications to any HTTPS endpoint (Slack, Home Assistant, custom automation, etc.). See [Webhooks](https://wiki.meshmapper.net/webhooks) for setup instructions.