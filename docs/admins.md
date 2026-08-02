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
    - **Inactive:** The repeater hasn't sent an advert within the region's **Repeater Inactive After** window (default 30 days) and has been removed from the map. This is non-destructive — the record is retained and returns to Active automatically the next time the repeater is heard. See [Repeater Lifecycle & Data Cleanup](#repeater-lifecycle-data-cleanup).
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

All of MeshMapper's ageing and cleanup controls are grouped together in the **Repeaters & Data Integrity** block of the Settings tab. They form a single pipeline: a repeater goes quiet, gets flagged, gets hidden, and — only if you opt in — eventually gets deleted. Each stage has its own timer, and each timer is independent of the others.

The nightly cleanup job runs once per day across the whole fleet. Nothing here happens instantly when you save a setting; changes take effect on the next nightly run.

#### The lifecycle at a glance

Using the defaults, for a repeater that stops adverting at **day 0**:

| Elapsed | What happens | Controlled by |
| --- | --- | --- |
| 24 hours | Flagged **stale** on the map. Still Active, still associates pings. | Stale Repeater Age (24h) |
| 72 hours (3×) | **Only if another repeater still shares its ID:** deleted as the stale half of a collision. A repeater with a unique ID is unaffected. | Stale Repeater Age × 3 |
| 30 days | Marked **Inactive** and removed from the map. Non-destructive — the record stays in the database and returns to Active the moment it is heard again. | Repeater Inactive After (30 days) |
| Never (default) | Permanently deleted. **Off unless you set a retention value.** | Repeater Retention / Auto-Delete (blank) |

Pending repeaters are **not** on this timeline — their clock starts when the record was created, not when the repeater went quiet. See [Pending repeater resolution](#pending-repeater-resolution) below.

Separately, and on their own clocks:

| Data type | Default | Controlled by |
| --- | --- | --- |
| Heard-only "ghost" devices | Aged out after 30 days unheard | Ghost Retention |
| Orphaned coverage pings | Kept forever | Stale Ping Cleanup (Disabled) |

#### Stale Repeater Age (Hours)

**Default: 24. Always on. Non-destructive.**

How many hours a repeater can go without sending an advert before it is considered stale and visually flagged on the map. A stale repeater is still Active — it still appears on the map and still associates with coverage pings.

This value also drives two separate cleanup routines, both keyed to **3× the stale age** (72 hours by default). They are described individually below, because they answer different questions and run on different clocks.

!!! example "Worked example"
    Stale Repeater Age = **12** hours. A repeater that last adverted 13 hours ago is flagged stale on the map, and the two 3× routines below now use a 36-hour threshold instead of 72.

    Lowering this value makes your map more responsive to outages but flags healthy repeaters more often in a quiet mesh. Raising it is the right call for regions with long advert intervals.

##### Duplicate collision cleanup

When a repeater has been silent for **3× the stale age**, MeshMapper checks whether any *other* repeater still shares the leading bytes of its ID.

  - **Nothing else shares its ID** — nothing happens. Silence alone never deletes a repeater here; it just continues down the timeline toward Inactive.
  - **Something else does share its ID** — the silent one is deleted that night. The reasoning is that between two devices claiming the same ID, the one that has gone quiet is the one you can afford to lose, and keeping it around only prolongs the collision.

**The survivor is repaired.** If exactly one other repeater shared that ID and it had been forced into **Excluded** status by the collision, it is restored to **Active** and given the clean ID back. So a collision that was blocking a legitimate repeater resolves itself once the stale twin is cleaned up — no admin action needed.

[See Duplicate Repeater IDs](https://wiki.meshmapper.net/duplicaterepeaterid/) for the full collision model.

##### Pending repeater resolution

This only applies when **New Repeaters Enter Pending State** is enabled, and it runs on a different clock from everything else on this page.

The question here is not "how long has this repeater been silent?" but **"has this repeater been sitting in the approval queue long enough for us to judge it?"** That clock starts when the record was created.

Once a pending repeater has existed for **3× the stale age**, MeshMapper resolves it by asking whether it is *currently* alive — a **1×** stale-age check, not 3×:

  - **Heard within the last 1× stale age** (24h by default) → automatically **approved** to Active.
  - **Not heard within the last 1× stale age** → **deleted**.

!!! example "Worked example"
    Stale Repeater Age = **24** hours, so pending records are judged once they are **72 hours** old.

      - A repeater first seen on Monday, still adverting on Thursday → 72h old and heard within 24h → **approved**, appears on the map.
      - A repeater first seen on Monday that adverted twice and never again → 72h old, last heard 3 days ago → **deleted**.
      - A repeater first seen yesterday → only 24h old, not yet judged either way. It waits in the queue regardless of how active it is.

    Note the asymmetry: the two thresholds are different numbers. 72 hours decides *when* the repeater is judged; 24 hours decides *which way*.

!!! tip
    A repeater exempted with **Bypass Auto Delete** is never deleted by this routine — but it can still be auto-approved.

#### Repeater Inactive After (Days)

**Default: 30. Always on. Non-destructive.**

How many days a repeater can go without an advert before it is marked **Inactive** (status 3) and removed from the map.

This is fully reversible and loses nothing. The repeater row, its notes, its history, and its leaderboard contributions all stay in the database. The next time an advert arrives, ingestion flips it straight back to Active and it reappears on the map.

Previously this was hardcoded to 30 days; it is now configurable per region.

!!! example "Worked example"
    A region with a slow, low-traffic mesh sets **Repeater Inactive After = 60**. A cottage-country repeater that only gets heard when someone drives past every few weeks now stays on the map for two months of silence instead of one.

    A dense urban region wanting a tighter map sets it to **14** — anything not heard in two weeks drops off, and reappears automatically if it comes back.

!!! tip "Per-repeater override"
    Enabling **Bypass Auto Delete** on an individual repeater (Repeaters tab) exempts it from *every* automatic routine described in this section — it will never be marked inactive, never deleted as a stale duplicate, never deleted as a stale pending repeater, and never deleted by the retention purge. Use it for seasonal or intentionally-offline deployments you want to keep pinned on the map.

#### Repeater Retention / Auto-Delete (Days)

**Default: blank (Disabled). Opt-in. DESTRUCTIVE.**

!!! danger "This permanently deletes repeaters"
    When set, a repeater that is **Inactive** and has not been heard for this many days is permanently deleted from your region's repeater database. Recovery is only possible from a nightly backup. **Leave the field blank to keep it disabled** — that is the default, and most regions should keep it that way.

This is the only setting in the panel that removes registered repeaters. It exists for regions that accumulate large numbers of dead records — test devices, one-off hardware, repeaters that were replaced rather than moved — and want the database to stay clean without manual pruning.

**How the clock is measured.** The deletion window is counted from the repeater's **last heard advert**, not from the day it flipped to Inactive. The two stages overlap on one timeline rather than running back to back.

!!! example "Worked example"
    Repeater Inactive After = **30**, Repeater Retention = **90**.

    A repeater last adverts on **January 1st**.

      - **January 31st** — 30 days silent. Marked Inactive, removed from the map. Record intact.
      - **April 1st** — 90 days silent. Permanently deleted.

    So it sat Inactive and recoverable for **60 days** (90 − 30) before deletion, not 90.

    Set Retention = **30** with Inactive After = **30** instead, and the two coincide: the repeater is marked inactive and deleted on the same nightly run.

**Minimum value.** The field enforces a live minimum — whichever is larger of your **Repeater Inactive After** value and a hard floor of **7 days**. The minimum shown next to the label updates as you type in the Inactive After field. A value below the minimum is rejected and the setting stays disabled, because a repeater cannot be deleted before it has been marked inactive.

!!! example "Rejected values"
    With Repeater Inactive After = **30**:

      - Retention = **90** → accepted.
      - Retention = **30** → accepted (equal to the minimum).
      - Retention = **20** → rejected, setting reverts to Disabled.
      - Retention = **blank** → Disabled (the default).

**What survives deletion.** Leaderboard points and Explorer credit earned against that repeater are preserved — they are moved to the **retired-points ledger** rather than lost, so no contributor's score drops because a repeater was cleaned up. The repeater row itself, however, is gone.

**A second safety gate.** Even with a value set, nothing is deleted until the MeshMapper operator separately enables the fleet-wide purge flag on the server. Setting a retention value alone will not delete anything.

Deletions are written to the audit log (repeater ID, last heard timestamp, and the retention window applied), so you can see exactly what was removed and when.

#### Ghost Retention (Days)

**Default: 30. Always on.**

A **ghost** is a device MeshMapper has heard passively — it answered a wardriver's discovery ping — but which has never sent an advert. Because it never adverted, it carries no name and no fixed location, so it can never appear on the map as a repeater. Ghosts are tracked in a separate heard-only catalog, purely as evidence that *something* with that ID is transmitting in the area.

This setting ages ghosts out of that catalog after the given number of days without being heard.

Ghosts are also removed immediately — regardless of this timer — the moment the same ID becomes a **registered repeater** in your region. Once a device starts adverting, it is a real repeater and no longer needs a ghost entry, so the ghost record is dropped on the next nightly run.

!!! info "Ghost cleanup never touches your repeaters"
    This routine only prunes the heard-only catalog. It can never delete, hide, or modify a registered repeater. It also runs for regions in Single Observer Mode and for regions with no registered repeaters at all.

**Why ghosts matter.** The ghost catalog is the evidence base for the **Pending Repeater Links** feature below. When a wardriver reports a repeater ID that resolves to a device hundreds of kilometres away, the presence of a local ghost sharing that ID is what tells you the pings almost certainly belong to an unregistered local device instead. Setting Ghost Retention too low weakens that evidence; setting it very high keeps stale ghosts around cluttering the analysis.

!!! example "Worked example"
    A wardriver drives past an unregistered repeater whose ID starts `C4A8`. It answers discovery 40 times but never adverts.

      - It is recorded as a ghost `C4A8…`, and is used as evidence in any pending-link decision involving that ID.
      - With Ghost Retention = **30**, if nobody hears it again for 30 days the ghost entry is dropped.
      - If its owner instead configures it properly and it starts adverting, it registers as a real repeater — and the ghost entry is deleted on the next nightly run, no waiting.

#### Pending Link Distance (km)

**Default: 200. Set to 0 to disable. Affects future ingestion only.**

This is the guard against the "ghost repeater steals a distant repeater's pings" problem.

When a wardriver hears a repeater, their radio reports a short ID token — often only one or two bytes. MeshMapper resolves that token against the registered repeater database. If the token resolves to exactly **one** registered repeater, MeshMapper would normally draw a link from the ping to that repeater's location.

The failure case: an **unregistered** local repeater happens to share the same short ID as a registered repeater on the other side of the country. Without this check, every ping heard from the local device gets attributed to the distant one, drawing false coverage lines hundreds of kilometres long.

**What this setting does:** if the single matching repeater sits farther than this many kilometres from the ping, the link is **not** drawn automatically. Instead the pings are held as a **Pending Repeater Link** in the Alerts tab for you to confirm or reject. The pings still appear on the map — they are simply not tied to a repeater until you decide.

!!! example "Worked example"
    Pending Link Distance = **200** (default).

      - A wardriver in Ottawa hears repeater token `C4`. It resolves uniquely to a repeater registered in Vancouver, **3,500 km away**. That is far past 200 km, so the pings are held for review and an alert appears.
      - The same wardriver hears token `9F`, resolving to a repeater 40 km away on a nearby ridge. Well under 200 km — linked automatically, no alert.
      - A mountaintop repeater genuinely reaching **215 km** would be held for review. You would use **Link to repeater** once, and future pings for that ID auto-link from then on.

!!! question "Why 200 km?"
    Genuine LoRa long-haul links (mountaintop to mountaintop) run up to roughly 220 km. Beyond that, a handheld radio in a car hearing a repeater almost always means the data actually belongs to an unregistered local device with a colliding short ID. The trade-off is deliberately asymmetric: a false alert costs you one click, while a missed one draws a permanently wrong line on the map.

**Tuning it.** Lower the value in a geographically dense region where you know nothing legitimately reaches far — you will catch more collisions, at the cost of more alerts. Raise it if your region genuinely has extreme long-haul links and you are tired of confirming them. Set it to **0** to disable the check entirely and always auto-link.

Changing this value affects **future ingestion only**. Existing pings and existing pending links are unaffected.

See [Pending Repeater Links](#pending-repeater-links) under Alerts for how to actually resolve the alerts this generates.

#### Stale Ping Cleanup (Auto-Delete Orphaned Pings)

**Default: Disabled. Options: Disabled / 30 / 60 / 90 days. DESTRUCTIVE.**

This ages out **orphaned** coverage pings. A ping is orphaned when the repeater it was attributed to has either **moved more than 100 m away** or **vanished from the database entirely** — exactly the pings the map already renders as **"(Gone)"**.

A ping only counts as orphaned when *every* repeater association on it is gone. If any part of it still resolves to a live repeater at the right location, the ping is kept. The detector is deliberately conservative: any doubt keeps the row.

##### The grace clock — the most important thing to understand

**Choosing a window does not delete everything that is already that old.** This is the single most common misreading of this setting.

Instead, the nightly job **starts a clock**. The first night it sees a ping orphaned, it stamps that ping with a timestamp. It only deletes the ping once it has stayed **continuously orphaned** for the full window. If the repeater comes back within 100 m at any point, the clock is cleared and the ping is kept.

!!! example "Worked example — the grace clock"
    You set Stale Ping Cleanup = **30 days** today, on **June 1st**. Your region has pings orphaned since **last year**.

      - **June 1st (tonight)** — the nightly job flags those pings as orphaned and stamps the clock. **Nothing is deleted.**
      - **June 2nd–30th** — the job re-checks them each night. Still orphaned, clock keeps running.
      - **July 1st** — 30 days continuously orphaned. *Now* they are deleted.

    So a ping orphaned for a year is still not deleted until 30 days after you turn the setting on. This is intentional: it gives a repeater that is only temporarily offline, or one that was accidentally deleted, a full window to come back before any data is lost.

!!! example "Worked example — the clock resetting"
    A repeater goes offline on **March 1st** and is deleted from the database on **March 5th**. Its pings become orphaned and the clock starts that night.

      - **March 20th** — the owner brings the repeater back and re-registers it at the same location. The pings resolve again, the clock is cleared, and nothing is deleted.
      - Had it come back at a location **500 m away** instead, the pings would stay orphaned (>100 m) and the clock would keep running.

##### What is preserved

**Leaderboard points and Explorer credit are not lost.** Every deleted ping is written to the **retired-points ledger** before removal, inside the same transaction as the delete. Contributors keep their points, their grid-square "first" claims, and their portal statistics. Only the ping row itself is removed.

##### Backfill Purge Now…

The dropdown above ages pings out gradually. **Backfill Purge Now…** is the immediate one-time alternative — it does not wait out the clock.

When you run it, it deletes every ping that is **already** orphaned **and** whose ping date is older than your saved retention window, plus any **no-location (0,0)** pings of any age. Recent orphaned coverage — anything inside the window — is deliberately kept, so a repeater that is only temporarily offline does not lose its data.

The flow is:

  1. Save a retention window (30 / 60 / 90) first. The preview will refuse to run without one.
  2. Click **Backfill Purge Now…**. A read-only preview modal opens.
  3. Review exactly what would be deleted — totals, a breakdown **by repeater** (with the reason each qualifies, e.g. *moved >100 m*), and a breakdown **by date** with ages. On a multi-region group you also get a per-region breakdown.
  4. Confirm. You must explicitly click through a confirmation showing the exact ping count.

!!! example "Worked example — Backfill Purge"
    Retention window = **30 days**. You run Backfill Purge on **June 1st**.

      - A ping from **January**, orphaned → **deleted** (already orphaned, older than 30 days).
      - A ping from **May 25th**, orphaned → **kept** (only a week old, inside the window — the repeater may just be temporarily offline).
      - A ping from **March** at coordinates **0,0** → **deleted** (no-location pings go regardless of age).
      - A ping from **January** whose repeater is still live and within 100 m → **kept** (not orphaned at all).

    Use this to clear an existing backlog today rather than waiting for the nightly job to age each ping out individually.

!!! warning "Minimum window for automatic sweeps"
    The nightly automatic sweep refuses to run with an effective window under **30 days**, which is why the dropdown offers no shorter option.

!!! info "Fleet rollout gate"
    Like the repeater purge, real deletion is blocked fleet-wide until the MeshMapper operator enables it on the server. Until then, both the nightly job and the Backfill Purge button only *mark* pings — the preview still shows you accurately what will be removed once it is switched on, and the modal will tell you if you are in that state.

If you have the **Ping Purge Cleanup Report** notification enabled, you will receive a Discord DM summarising what was removed. On a multi-region group this arrives as one combined message with a per-region breakdown.

#### New Repeaters Enter Pending State

When enabled, newly discovered repeaters will enter a **Pending** state instead of **Active**. Pending repeaters are hidden from the map until an admin reviews and approves them, and are resolved automatically once they have been in the queue for 3× the stale timer — see [Pending repeater resolution](#pending-repeater-resolution) for exactly how that decision is made. In multiregion mode, this setting is configured per-region under Region-Specific Settings.

!!! warning "Data Inaccuracy Warning"
    New repeaters will not display on the map until approved. This can cause data inaccuracies. Use with caution.

#### Disable Duplicate ID Detection Logic

Allows the region to opt-out of MeshMapper's strict duplicate ID collision handling. When enabled, repeaters with colliding IDs will remain active, and pings will associate with all matching repeaters.

  - *Warning:* This compromises data accuracy. A warning badge will be displayed on the public map, and the region will be excluded from global leaderboards.
  - [Learn more about overriding duplicate detection](https://wiki.meshmapper.net/overrideduplicates/)

#### Multi-region groups

On a multiregion admin panel, these settings behave differently depending on where you set them.

**Set at the group level** (Multi-Region Settings → Group Defaults) and applied to every member region:

  - Stale Repeater Age
  - Pending Link Distance
  - Stale Ping Cleanup (including Backfill Purge, which runs across every member region)

**Set per-region**, on each member region's own settings:

  - Repeater Inactive After
  - Repeater Retention / Auto-Delete
  - Ghost Retention

When you open a **member region** of a group, the group-controlled fields are shown greyed out and read-only — the group's value wins. Change them from the group panel instead.

!!! info "How the value is resolved"
    For each setting, MeshMapper checks the containing group's configuration first. If the group specifies a value, that value is used. If not, the region's own value is used. If neither sets one, the built-in default applies.

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

This alert is generated by the [Pending Link Distance](#pending-link-distance-km) setting. It appears when a wardriver's ping reports a repeater ID token that resolves to exactly one registered repeater, but that repeater sits farther away than your configured distance.

The pings involved **stay on the map** — they are simply not tied to any repeater until you make a decision. Nothing is deleted, and nothing is hidden.

#### Reading the evidence

Each alert row is built to let you decide without leaving the page:

  - **The resolved repeater** — its ID, name, region, and how far away it is.
  - **What was actually heard on-air** — the short token the wardriver's radio genuinely reported, which is often shorter than the resolved ID. This is the crux: the extra bytes came from MeshMapper's resolution, not from the radio.
  - **Nearby ghosts** — unregistered devices that have answered discovery in this area, sorted into two tiers:
      - **Strong matches**, whose key starts with the exact token that was heard. If one of these exists, the pings almost certainly belong to it rather than to the distant registered repeater. The panel will recommend leaving them unlinked.
      - **Weak matches**, which share only the first byte. These are shown de-emphasised, because a wider heard token is what genuinely rules them out.
  - **The held pings themselves** — expandable, showing date, session, the heard token, coordinates, and a **🗺️ Map** link that opens the public map at that exact ping.

#### Your three choices

  - **Link to repeater** — you personally know that repeater genuinely reaches this area (a rare long-haul). The pings are linked using the repeater's current coordinates, the decision is recorded permanently, and future far pings for this ID auto-link.
  - **Leave unlinked** — the likely case. The pings stay on the map, permanently marked as not tied to any repeater. New far pings for this ID will alert again.
  - **Leave unlinked + suppress** — the same, but future far pings for this ID are quietly held without generating a new alert. Use this when you have confirmed there is a local unregistered device and you do not want repeat notifications.

With more than one pending row, a **Suppress all** button appears. Suppressed IDs are listed in their own collapsible section with held-ping counts, and can be individually **Restored** or restored in bulk.

!!! info "Suppression clears itself"
    Suppression is not permanent. MeshMapper tracks the *situation* around each ID. The moment anything about it changes — a local repeater with that ID registers, the distant repeater moves or is deleted, or a new unregistered ghost appears in the area — the suppression is automatically cleared and you are alerted again. The same applies to a confirmed link.

!!! warning "Two cases where linking is refused"
    - **Unplaced repeater** — the repeater has no usable position (unplaced, or 0,0). It must be placed on the map before its links can be confirmed. This prevents pings being baked to a meaningless location.
    - **Newly ambiguous** — more than one registered repeater now matches that ID, meaning the situation changed since the pings were held. Linking would be a guess between devices, so you are asked to review the ID's repeaters first.

If a region has pending links awaiting review, a daily reminder is sent to admins who have the **Pending Repeater Link** notification enabled. Each ID notifies once; the latch resets if its situation changes.

## Notifications

Link your Discord to MeshMapper to receive DM's from the MeshMapper bot.

  - **Alert on Duplicate Repeater ID**: Notifies you when a repeater has sent an advert, but its ID collides with another, putting both repeaters into Excluded status.  [See Duplicate Repeater ID](https://wiki.meshmapper.net/duplicaterepeaterid)
  - **Alert on Pending Repeater**: Once a day, receive a notification if your region has repeaters in **Pending** state that are awaiting review.  This notification is only relevant if "New Repeaters Enter Pending State" is enabled for the region.
  - **Allow Messages From Visitors**: When enabled, a map visitor can send a message to you directly from the "Region Info" page of your regions map.
  - **Alert on Offline Observer**: Once a day (around 0800 EST/EDT) MeshMapper will review all data received via your regions MQTT observers (pings, repeater adverts, companion adverts) for the past 7 days.  If a particular observer has sent data within that time, but not within the "Stale Repeater Age" time configured for your region, then this observer is potentially offline.  Receive an alert when this is the case.
  - **Suspicious Flight**: Receive an alert when a live session contains pings whose implied speed between consecutive fixes exceeds the flyover threshold — a device that was likely flown rather than driven. Corresponds to the **Suspicious Live Sessions** alert.
  - **Pending Repeater Link**: Once a day, receive a summary of repeater IDs with pings held for review because they resolved to an implausibly distant repeater. Each ID notifies once; the latch resets automatically if the situation around that ID changes. See [Pending Repeater Links](#pending-repeater-links).
  - **Ping Purge Cleanup Report**: Receive a DM summarising what the [Stale Ping Cleanup](#stale-ping-cleanup-auto-delete-orphaned-pings) removed — the ping count, and a breakdown by date and repeater. On a multiregion group this arrives as a single combined message with a per-region breakdown. Only sent when something was actually deleted.

These events are also available as **webhook** subscriptions, configured separately in the Settings tab. See [Webhooks](https://wiki.meshmapper.net/webhooks/).

Webhooks can also be configured per-region to send these same notifications to any HTTPS endpoint (Slack, Home Assistant, custom automation, etc.). See [Webhooks](https://wiki.meshmapper.net/webhooks) for setup instructions.