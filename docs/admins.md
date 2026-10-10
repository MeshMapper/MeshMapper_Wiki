# Admin Panel

The **MeshMapper Admin Panel** is where region administrators keep their region's data clean, change its settings, and check the health of its map.

## Access & Permissions

The Admin Panel is only for region administrators.

  - **Getting access:** If the region has an administrator, ask them for an invite. If it has none, ask a Moderator in the MeshMapper Discord. See [Finding Your Region's Administrators](administratorlist.md).
  - **Signing in:** Go to **admin.meshmapper.net** and sign in with your MeshMapper account (username or email, plus password), or click **Sign in with Discord**. It's the same account you use for the [portal](portal.md). If you've lost your password, use **Forgot password?**.

The sidebar lists the tabs in this order: **Overview**, **Coverage**, **Repeaters**, **CARpeaters**, **Companions**, **Sessions**, **Administrators**, **Tools**, **History**, **Alerts**, **Observers**, **Settings** and **User Settings**. It also has **Go to Map** and **Switch Region**.

## Overview

The first tab you see after signing in.

  - **Region Statistics:** Total Data Points, Bidirectional, TX Only, RX Only, Discovery, Dead, Dropped, Active Repeaters, Est. Coverage and Contributors. Click **Refresh** to update them.
  - **Active Sessions:** Who is wardriving in your region right now, with Status, Last Active and Pings (click **Calc** to count them).
  - **Capacity:** Shows **Active**, **Transmitting** (slots used out of slots available) and **Passive** sessions. Group panels show **Group TX slots**.
  - **Kick:** Ends a session that is stuck or holding a slot it doesn't need.

## Data Management

The next few tabs manage your region's data: pings, repeaters, CARpeaters, companions and sessions.

### Coverage

Every coverage point (ping) in your region.

  - **Search:** By Name, Time/Date, Lat/Lon, Block Code (paste a `P-` code from the map), Via (repeater), Heard Repeats or Offline Uploads. You can also filter by status.
  - **Row details:** An icon opens the ping on the map. Pings uploaded later from the app's offline mode show an **OFFLINE** badge. Tags show the radio preset and altitude when known.
  - **Delete:** Removes a single bad ping.
  - **Debug:** If the ping was sent with Debug Mode on, a **Debug** button shows the raw data from the device.
  - **Bulk delete:** Tick rows (or the header box to select all), then click **Delete Selected**.
  - **Export CSV:** Downloads the current results.

!!! info "Fixing ping details"
    Region admins can't edit a single ping. To fix details such as power or external antenna, use **Bulk Update Pings** in the [Tools tab](#maintenance-tools).

### Repeaters

Your region's repeater list.

If an unknown repeater shows up, first check whether an observer has heard an advert from it with a valid name. A repeater heard only through wardriving discovery is a **Ghost**: it has no name or fixed location. You can add or correct its record here. Don't give a guessed location to a device that moves.

On a group map, a repeater can come from any member region. Check the Region column before editing it. When a repeater moves, its next advert updates its position unless **Lock GPS Coordinates** is on. Old pings don't move with it.

#### Statuses

  - **Active:** Shown on the map and leaderboards, and linked to coverage pings.
  - **Disabled:** Hidden from the map and leaderboards, but kept in the list.
  - **Inactive:** No advert has reached MeshMapper within **Repeater Inactive After** (default 30 days), so it's hidden from the map. The record is kept, and it goes back to Active on its own at its next advert through an observer. Wardrive pings alone won't bring it back. See [Repeater Lifecycle & Cleanup](#repeater-lifecycle-cleanup).
  - **Ambiguous:** Its ID matches another repeater's, so MeshMapper can't tell which one a ping went through. It shows as a **red** icon on the map, and coverage isn't credited to it (except **Discovery** pings, which carry the full key). See [the collision rules](duplicaterepeaterid.md#the-rules).
  - **Pending** (shown as a pill): Found, but waiting for approval. Only used when **New Repeaters Enter Pending State** is on. Pending repeaters aren't on the map and don't collect coverage. Approve one by editing it and setting its status to **Active**, or use **Review Pending Repeaters** in the Alerts tab. Pending repeaters that nobody reviews are sorted out automatically; see [Pending repeater resolution](#pending-repeater-resolution).

!!! warning "You can't force an Ambiguous repeater to Active"
    MeshMapper checks for ID collisions again at every advert, so setting an Ambiguous repeater to **Active** won't stick. To fix it, one of the repeaters has to change its ID. See [Duplicate Repeater IDs](duplicaterepeaterid.md).

    A **Disabled** or **Inactive** repeater is left out of this check. If one side of a collision is gone for good, set it to Disabled and its partner goes back to Active at its next advert.

#### Adding and editing

  - **Add Repeater:** Name, Advert Bytes (1, 2 or 3), Public ID, ID, Lat, Lon, Power, Status and Bypass Auto Delete.
  - **Edit:** Name, location, power, status, Hardware, Antenna, Height above ground (m), Power source and Site note (shown publicly), plus:
    - **Lock GPS Coordinates:** New adverts won't change its location. Use it when the GPS set on the repeater is wrong.
    - **Bypass Auto Delete:** Every automatic cleanup skips this repeater. It won't be marked Inactive, won't be removed as a stale Pending repeater, and won't be removed by [Repeater Retention / Auto-Delete](#repeater-retention-auto-delete-days). Good for seasonal or remote repeaters you want kept on the map.
    - **Administrators:** People who logged in to the repeater as admin from the app. Add one by public key or exact companion name.
    - **Radio presets:** Presets the repeater was heard on. Add one as `freq,bw,sf`. Removing one only hides it until the repeater is heard on that preset again.

!!! warning "Lock GPS Coordinates"
    Locking the location of a repeater that moves will put its coverage in the wrong place.

#### Finding and managing repeaters

  - **Filters:** Location (All, No Location (0,0), Out of Boundary) and claim (All, Claimed, Unclaimed). The table shows each repeater's **Bytes** and whether it's in or out of your boundary.
  - **Select Offline (n):** Selects every offline repeater at once.
  - **Mark as CARpeater:** Tags a repeater as riding in a car. See [CARpeaters](#carpeaters).
  - **Ping counts:** Click **Calc** on a row, or **Load All Ping Counts**.
  - **Notes:** Click the note icon to add a note. On a group panel, notes for a repeater that's in several regions are shown together and saved to each region.
  - **Export CSV:** Downloads the list.
  - **Bulk Edit:** Tick rows, then change Status, Power, Lock GPS and Notes for all of them at once. Each field has an **Apply** checkbox, so only ticked fields change. Bulk editing Notes **overwrites** existing notes. You can also delete the selected repeaters.
  - **Neighbours:** To clear a repeater's neighbour list, use **Reset Neighbours** in the [Tools tab](#maintenance-tools).

!!! warning "Deleting doesn't fix a duplicate ID"
    A deleted repeater comes back at its next advert. Deleting won't fix an ID collision while the repeater is still on the air.

!!! info "Blank name adverts"
    Adverts with a blank name are rejected, so nothing is added or updated. If a working repeater isn't showing up, check that its name is set.

### CARpeaters

A CARpeater is a repeater riding in a wardriver's car. Pings heard through it would make coverage look far bigger than it is, so apps in your region drop packets heard through a CARpeater.

  - **Add CARpeater:** Enter the repeater's public key. You can also use **Mark as CARpeater** on the Repeaters tab.
  - **Columns:** Public Key, Resolves To, Shares Prefix With, Reporters, First Reported, Last Reported and Auths.
  - **Delete:** Removes the tag.

Tags that haven't been reported for **CARpeater Retention (Days)** (default 90) are removed. See [CARpeater Retention](#carpeater-retention-days).

### Companions

Your region's list of known companions.

  - **Add Companion:** Add a companion by public ID and give it a name. The **Type** column shows what kind of device it is.
  - **Status:** **Active**, **Inactive** or **Blocked**. A Blocked companion can't upload data to the map.
  - **Notes:** Click the note icon to add a note. On a group panel, notes for a companion that's in several regions are shown together and saved to each region.
  - **Bulk Edit:** Tick rows, then change Status and Notes for all of them at once.
  - **Delete:** The delete window has **Also delete its N coverage points in this region**, ticked by default. The deletion is logged so it can be undone.

### Sessions

Every wardriving session in your region.

  - **Columns:** Who, Session ID, Mode (Standard or Offline), Status, Started, Active Time, Ping Count and Actions.
  - **Metadata:** Shows details of the device used, such as app version and hardware model.
  - **🗑️ Pings Only:** Deletes the session's pings but keeps the session.
  - **×:** Deletes the session and its pings.

### Users

The Users tab has been retired. Wardrivers now link their own companions to their MeshMapper account in the [portal](portal.md), which becomes their leaderboard identity.

## Administrators

Everyone with admin access to your region. Each listed admin shows as **Active**, with their contact info. On a group panel, you also see which member regions each admin has.

**Pending Invites** lists invites that haven't been accepted yet: Invitee, Region, Invited By and Expires. Use **Resend** to send one again, or **×** to revoke it.

### Adding a New Administrator

  1. Click **Invite Admin**.
  2. In **Invite an administrator**, enter their **Email** and pick a **Region Assignment**.
  3. Click **Send invite**.

MeshMapper emails an invite tied to that address. It expires after 7 days. If the email fails, the panel shows a link you can pass on yourself.

### Accepting an Invite

Open the invite with the matching email or Discord account. Sign in to your MeshMapper account, or create one, then accept the invite. Sign in to the admin panel with that same account.

Forgot your password? Use **Forgot password?** on the sign-in page or the [portal](portal.md). If you use Discord to sign in, click **Sign in with Discord**. The bot doesn't send new passwords.

## Maintenance Tools

The **Tools** tab changes many pings at once. **Use with care.** Every tool has **Analyze & Preview**, so you see what will change before you confirm.

  - **Replace Repeater:** Moves an old repeater's pings to another repeater, within a From/To date range. Useful when a repeater gets a new ID or new hardware. **Find removed repeaters** helps you pick one that's no longer in the list. Ping positions aren't moved, so run **Reassociate Repeater** afterwards.
  - **Bulk Delete / Scrub Pings:** Deletes pings from one companion or all companions, in a date range or **All time**. Pick a repeater to remove just that repeater from the pings instead of deleting them.
  - **Bulk Update Pings:** Changes details on many pings. **Companion** is required and **Session ID** is optional. You can set a **New Companion** (rename), **New Power** and **New Ext. Ant**. There's no date filter.
    *Example:* set every ping from companion "Tom_Mobile" in session `20241221-0005` to External Antenna = YES.
  - **Reassociate Repeater:** Re-links pings to a repeater that was missing when they came in, or that had the wrong GPS. Pings already within about 100 m of the right spot are skipped, and so are pings where the repeater ID is ambiguous.
  - **Reset Neighbours:** Clears the neighbour list of one repeater, or of **All Repeaters (Full Reset)**.

!!! warning "Check the location first"
    Reassociating pings to a repeater in the wrong place puts coverage in the wrong place. Make sure the repeater's GPS is right before running it.

## History

**Admin Activity History** is a log of every admin action in your region: Time, User, IP, Action and Details.

## Alerts

**Alerts & Warnings** lists things that need a look. If there's nothing, it shows **All clear!**

  - **Repeater Clock Alerts:** Repeaters whose clock is more than 120 seconds off, among those that adverted in the last 7 days. A wrong clock can affect routing. Tick **Only show in-boundary repeaters** to hide the rest.
  - **Ambiguous Public IDs Detected:** Repeaters that share an ID, listed by **Collision Group**. **MB Capable** tags show which ones can use multi-byte IDs. See [Duplicate Repeater IDs](duplicaterepeaterid.md).
  - **Pending Repeaters:** Repeaters waiting for approval. Click **Review Pending Repeaters**.
  - **Suspicious Live Sessions:** Sessions with pings moving faster than any ground vehicle, usually a device on a plane. Each row shows who, session ID, start time, top speed and ping count, with a **🗺️ Map** link. **Delete** the session to remove its pings, or **Dismiss** it if the speed was real (a train, for example). Dismissed sessions are kept in a list and can be brought back with **Restore**.
  - **Pending Repeater Links:** Pings held because their repeater is too far away. See below.

### Pending Repeater Links

Created by the [Pending Link Distance](#pending-link-distance-km) setting: a ping's repeater ID matched exactly one registered repeater, but it's farther away than your set distance.

The pings **stay on the map**. They're just not linked to a repeater until you decide. Nothing is deleted or hidden.

#### Reading the evidence

Each row gives you what you need to decide:

  - **The matched repeater:** ID, name, region and distance.
  - **What was actually heard on air:** The short ID the radio really reported. It's often shorter than the matched ID, and that's the key point: the extra bytes came from MeshMapper's lookup, not from the radio.
  - **Nearby ghosts:** Unregistered devices answering discovery in the area. **Strong matches** start with the exact ID that was heard; if there is one, the pings almost certainly belong to it and the panel says so. **Weak matches** share only the first byte and are shown faded.
  - **The held pings:** Date, session, heard ID, coordinates, and a **🗺️ Map** link to each ping.

#### Your three choices

  - **Link to repeater:** You know that repeater really reaches this area. The pings link to its current position, and future far pings for this ID link automatically.
  - **Leave unlinked:** The likely case. The pings stay on the map, linked to no repeater. New far pings will alert again.
  - **Leave unlinked + suppress:** The same, but future far pings are held quietly without a new alert. Use it once you've confirmed there's a local unregistered device.

With more than one row you also get **Suppress all**. Suppressed IDs sit in their own list with held-ping counts and can be restored one at a time or all at once.

!!! info "Suppression clears itself"
    MeshMapper keeps watching each ID. If a local repeater with that ID registers, the distant one moves or is deleted, or a new ghost appears, suppression clears and you're alerted again. The same goes for a confirmed link.

!!! warning "When linking is refused"
    - **Unplaced repeater:** It has no usable position, so linking would put the pings in a meaningless place. Place it on the map first.
    - **Newly ambiguous:** More than one repeater now matches that ID, so linking would be a guess. Check that ID's repeaters first.

Admins with the **Pending Repeater Link** notification on get a daily reminder. Each ID notifies once, and again only if its situation changes.

## Observers

The MQTT observers feeding data into your region.

!!! info "Connecting an observer"
    Connect your observers to the [MeshMapper MQTT broker](mqtt-main.md). MeshMapper also collects from LetsMesh, but that isn't MeshMapper infrastructure.

**Summary cards** at the top:

  - **Total:** Every observer seen.
  - **Online:** Heard within your region's **Stale Repeater Age**.
  - **Stale:** Heard within the last 7 days, but not within Stale Repeater Age.
  - **Offline:** Not heard in the last 7 days.

**Table columns:**

  - **Observer:** Its name and ID.
  - **Region:** *(Groups only)* Which member region(s) it belongs to.
  - **Status:** Online, Stale or Offline, with how long ago it was last heard.
  - **Pings**, **Repeaters**, **Companions:** How many coverage pings, repeater adverts and companion adverts came through it.
  - **Brokers:** One badge per broker. A badge is coloured when that broker heard the observer in the last 7 days, with the last-heard time below it.
  - **Notifications:** Mutes or unmutes offline alerts for this observer. Muting only stops alerts; data still comes in.
  - **Action:** **Remove** takes an old observer off the list. If it starts sending again, it comes back on its own.

## System Settings

The **Settings** tab is split into blocks: **Public Display**, **Repeaters, Neighbours & Scopes**, **Wardriving**, **MQTT Brokers & Observers**, **Data Sources**, **Notifications** and **Region Boundary**. Click **Save All Settings** when you're done.

### Public Display

  - **Region Message:** Shown to map visitors when they open **Region Info**. Use it to point people to your Discord server or website. Plain text up to 500 characters; links become clickable. Not shown on regions that are part of a group.
  - **Social Media Links:** Any number of social media or website links, shown in **Region Info**.

### Repeaters, Neighbours & Scopes

  - **Stale Repeater Age**, **Repeater Inactive After (Days)**, **Repeater Retention / Auto-Delete (Days)**, **Ghost Retention (Days)** and **CARpeater Retention (Days)**: see [Repeater Lifecycle & Cleanup](#repeater-lifecycle-cleanup).
  - **Pending Link Distance (km)** and **Stale Ping Cleanup**: see [Coverage Ping Settings](#coverage-ping-settings).
  - **Neighbour links:** How long a neighbour link stays after it was last seen: **Inferred, days** (default 7), **Reported, days** (30) and **Uploaded, days** (0). **0** means never delete it on age. Links between repeaters farther apart than **Max link distance, km** (default 250) are dropped.
  - **Scopes to Monitor:** Extra scope names to look for in the traffic MeshMapper hears, one per row, saved in lowercase. Your Wardriving Scope and scopes your repeaters report are included automatically, so most regions can leave this empty.
  - **Mesh Scopes retention:** How long each kind of scope sighting is kept: **Seen forwarding**, **Reported by observers** and **Uploaded from the app**, in days (default 60; **0** means never delete).
  - **New Repeaters Enter Pending State** and **Disable Duplicate ID Detection Logic**: see below.

#### Repeater Lifecycle & Cleanup

These settings decide when a quiet repeater is flagged, hidden and (only if you turn it on) deleted. Cleanup runs once a night, so changes take effect at the next run.

!!! warning "\"Heard\" means an advert, not a wardrive"
    These timers only reset when the repeater sends an **advert that reaches MeshMapper through an MQTT observer**.

    Wardriving past a repeater records pings as normal, but does **not** reset its clock. A repeater that works fine but has no observer in range will still age off the map.

    Ghosts are the exception: they run on wardrive discovery. See [Ghost Retention](#ghost-retention-days).

With the default settings, this is what happens to a repeater that stops adverting on **day 0**:

| Elapsed | What happens | Setting |
| --- | --- | --- |
| 24 hours | Flagged **stale** on the map. Still Active, still collects pings. | Stale Repeater Age |
| 30 days | Marked **Inactive** and hidden from the map. Comes back when it adverts again. | Repeater Inactive After |
| Never | Permanently deleted. **Off by default.** | Repeater Retention / Auto-Delete |

Ghosts have their own clock and age out after 30 days. Pending repeaters follow their own rules; see [Pending repeater resolution](#pending-repeater-resolution).

!!! tip "Keep one repeater no matter what"
    **Bypass Auto Delete** on a repeater (Repeaters tab) exempts it from every rule in this section.

#### Stale Repeater Age (Hours)

**Default: 24. Always on. Doesn't delete anything.**

Hours without an advert before a repeater is flagged stale on the map. It stays Active and still collects pings; this is only a visual warning. It's also how long a repeater's radio preset tag holds, and how long an observer counts as Online.

It also sets the **3×** point (72 hours by default) used by [pending repeater resolution](#pending-repeater-resolution).

Lower it for a map that reacts quickly to outages. Raise it if your repeaters advert rarely and healthy ones keep getting flagged.

##### Pending repeater resolution

Only applies when **New Repeaters Enter Pending State** is on. This clock starts when the repeater was first added, not when it went quiet.

Once a pending repeater is **3× the stale age** old, MeshMapper decides based on whether it adverted within **1×** the stale age:

  - **Adverted recently:** approved to Active.
  - **Didn't:** deleted.

!!! example
    With Stale Repeater Age = 24h, pending repeaters are judged at 72 hours old:

      - Added Monday, still adverting Thursday: **approved**.
      - Added Monday, went silent Tuesday: **deleted**.
      - Added yesterday: not judged yet.

    The two numbers differ on purpose: 72h decides *when* it's judged, 24h decides *which way*.

A repeater with **Bypass Auto Delete** is never deleted here, but can still be approved automatically.

#### Repeater Inactive After (Days)

**Default: 30. Always on. Doesn't delete anything.**

Days without an advert before an **Active** or **Ambiguous** repeater is marked **Inactive** and hidden from the map.

Nothing is lost: the record, notes, history and leaderboard points all stay. It goes back to Active on its own at its next advert.

This is also what clears an old collision. Once an Ambiguous repeater goes Inactive, it's left out of the ID check, and its partner goes back to Active at its next advert. See [Duplicate Repeater IDs](duplicaterepeaterid.md).

!!! example
    Raise it to **60** for a repeater whose adverts only sometimes reach an observer. Lower it to **14** in a busy region that wants old entries off the map quickly.

!!! warning "This won't help a repeater no observer can hear"
    A higher value only helps if adverts get through *sometimes*. If no observer hears the repeater at all, it ages out anyway, and its wardrive pings won't stop that. The fix is an observer, not a timer. (**Single Observer Mode** turns this ageing off.)

#### Repeater Retention / Auto-Delete (Days)

**Default: blank (off). DELETES DATA.**

!!! danger "This permanently deletes repeaters"
    An Inactive repeater that hasn't adverted for this many days is **permanently deleted**. There is no undo. **Leave it blank to keep it off.**

    A repeater no observer can hear looks the same as a dead one. Turning this on in a region with patchy observer coverage will delete repeaters that are still working.

Some regions collect dead records (test devices, replaced hardware) and want them pruned without doing it by hand.

**The clock runs from the last advert**, not from when the repeater went Inactive.

!!! example
    Inactive After = **30**, Retention = **90**. A repeater last adverts January 1st:

      - **January 31st:** marked Inactive and hidden. Record kept.
      - **April 1st:** permanently deleted.

    So it sat Inactive for 60 days, not 90. Set both to 30 and it's marked Inactive and deleted on the same night.

**Minimum:** your **Repeater Inactive After** value or 7 days, whichever is larger. A smaller value is rejected and auto-delete stays off.

Leaderboard points and Explorer credit are kept; only the repeater record goes. Deletions are written to the History log.

Nothing is deleted until MeshMapper enables the purge for everyone. Setting a value alone isn't enough.

#### Ghost Retention (Days)

**Default: 30. Always on.**

A **ghost** is a device that has only been heard answering a wardriver's discovery ping and has never sent an advert. With no advert it has no name and no fixed location, so it never shows on the map. Ghosts are kept in a separate list as evidence that *something* with that ID is transmitting nearby.

A ghost is dropped after this many days without being heard. Once MeshMapper gets an advert from it, it becomes a normal repeater straight away and the rules above apply.

The ghost list is what makes [Pending Repeater Links](#pending-repeater-links) work: a local ghost sharing a distant repeater's ID shows the pings belong to the local device. Set it too low and you lose that evidence.

!!! info
    Ghost cleanup only touches the ghost list. It never changes or deletes a registered repeater.

#### CARpeater Retention (Days)

**Default: 90.** A [CARpeater](#carpeaters) tag that hasn't been reported for this many days is removed.

#### New Repeaters Enter Pending State

When on, newly found repeaters start as **Pending** instead of **Active**. They stay off the map until an admin approves them, or until they're sorted out automatically (see [Pending repeater resolution](#pending-repeater-resolution)).

!!! warning "Pending repeaters don't collect coverage"
    Pings aren't linked to a repeater while it's Pending, and approving it later doesn't fill them in. Use **Reassociate Repeater** in the Tools tab if you need them linked.

#### Disable Duplicate ID Detection Logic

Turns off MeshMapper's duplicate ID handling. Colliding repeaters stay Active, and pings link to every matching repeater.

  - *Warning:* This hurts data accuracy. The public map shows a warning badge, and the region is left out of global leaderboards.
  - [Learn more about overriding duplicate detection](overrideduplicates.md)

#### Coverage Ping Settings

These decide how coverage pings are linked to repeaters and when orphaned pings are removed.

##### Pending Link Distance (km)

**Default: 200. 0 turns it off. Only affects new pings.**

A ping that matches a repeater farther away than this isn't linked automatically. It's held as a **Pending Repeater Link** in the Alerts tab for you to decide. The pings stay on the map, just not linked to a repeater.

This catches an unregistered local repeater that shares a short ID with a registered one far away, which would otherwise draw coverage lines across the country.

!!! question "Why 200?"
    LoRa links this long are unlikely. A handheld hearing a repeater that far away almost always means an unregistered local device with the same short ID.

Lower it in a small region to catch more collisions (and get more alerts). Raise it if you really have very long links. **0** always links automatically.

See [Pending Repeater Links](#pending-repeater-links) for how to handle the alerts.

##### Stale Ping Cleanup (Auto-Delete Orphaned Pings)

**Default: Disabled. Options: Disabled / 30 / 60 / 90 days. DELETES DATA.**

Removes **orphaned** pings: pings whose repeater has moved more than 100 m or is gone. The map already shows these as **"(Gone)"**. A ping only counts as orphaned when *every* repeater on it is gone. Don't use this just to hide a repeater from the map.

**Picking a window doesn't delete your existing backlog.** The nightly job starts a clock the first night it sees a ping orphaned, and only deletes it once it has stayed orphaned for the full window. If the repeater comes back within 100 m, the clock clears and the ping is kept.

!!! example
    You pick **30 days** on June 1st, and you have pings orphaned since last year.

      - **June 1st:** they're flagged and the clock starts. Nothing is deleted.
      - **July 1st:** 30 days orphaned. *Now* they're deleted.

    If a repeater comes back on June 20th (within 100 m), its pings are kept.

Leaderboard points and Explorer credit are kept; only the ping record is removed.

**Backfill Purge Now…** clears the backlog right away instead of waiting. It deletes every ping that is **already** orphaned **and** older than your saved window, plus any no-location (0,0) pings of any age.

  1. Save a window (30, 60 or 90) first. The preview won't run without one.
  2. Click **Backfill Purge Now…** to open a preview. Nothing is deleted yet.
  3. Check what would go: totals, what share of the region's pings that is, and breakdowns by repeater and by date (and by region for groups). The preview confirms leaderboard and Explorer credit are kept.
  4. Confirm the exact ping count.

!!! example
    Window = 30 days, run on June 1st:

      - January ping, orphaned: **deleted**.
      - May 25th ping, orphaned: **kept** (inside the window; the repeater may only be briefly offline).
      - March ping at 0,0: **deleted** (no-location pings go at any age).
      - January ping whose repeater is still nearby: **kept** (not orphaned).

!!! info
    There's no window under 30 days. And like the repeater purge, nothing is actually deleted until MeshMapper enables it for everyone; until then pings are only marked, and the preview tells you so.

With the **Ping Purge Cleanup Report** notification on, you get a Discord DM summarising what was removed (one message per group).

### Wardriving

#### Radio Channels

Wardriving rules are set per radio channel, one row each. The **\*** row covers every radio that doesn't have its own row. Click **Add preset** to add a row for a channel; a new row starts with Flood Off and Slots 0.

| Column | What it does |
| --- | --- |
| **Slots** | How many people can transmit on that channel at once. **0** makes it listen-only. |
| **Flood** | **Off** turns off Active and Hybrid modes, so wardrivers can only listen. Forces Slots to 0. |
| **Path B** | App Path Bytes: **Device**, **2** or **3**. Tells the app what path width to set. It doesn't change repeaters. See [Multi-Byte Repeaters](multibyte.md). |
| **Hybrid** | Forces Hybrid mode (turns off Active mode). Try it if your mesh drops packets from heavy traffic. |
| **DISC drop** | When on, Discovery pings that get no reply show as DROP (red). When off, they don't show. |
| **Interval** | Shortest time between pings: 15s, 30s or 60s (default 60s). |
| **Smart** | Locks the app's Smart Pinging on, so pings are held in squares that already have a recent result. |
| **Window** | How recent a result must be for Smart Pinging: 1, 3, 7, 14 or 30 days (default 14). |
| **Scopes** | Scope discovery: after each discovery, the app asks each repeater it found which scopes it carries. Adds a little extra traffic. Off by default. |
| **Re-check** | How many days a repeater's scope answer counts as fresh before it's asked again (minimum 7, default 14). |

#### Other wardriving settings

  - **Public Channels:** Channels the app listens on for passive coverage. **#public** is always included; add any other # channels you know of.
  - **Wardriving Scope:** The scope the app puts on every Active and Hybrid ping. Repeaters not set up for it drop those pings. If you don't use scopes, leave it at **\***.
  - **Disable Detailed Statistics (Hide Detail):** *(Groups only)* Hides the Repeater Coverage, Neighbours, Scopes and Backbone layers on the map.

### MQTT Brokers & Observers

Called **Group MQTT Brokers** on a group panel.

  - **Observers:** The observers your region takes data from. Paste each observer's full 64-character Public ID.
  - **Subscribe to all local observers:** When on, your region uses packets from any observer connected in its area. When off, only the observers you list are used. Turn it off if a far-away observer is being counted as part of your mesh.
  - **Add Broker:** Adds your own MQTT broker: Display Name, Username, Password, Badge Icon, Badge Color, Hosts and Enabled. Each broker can be tested, edited, paused or deleted. **Last data ingested** shows how fresh its data is, and the **Connection log** helps with problems. A broker must run meshcore-mqtt-broker in WebSocket mode with SSL (`wss://`) and have a role 2 subscriber account.

Most regions don't need their own broker. Point observers at the [MeshMapper MQTT broker](mqtt-main.md).

### Data Sources

  - **Single Observer Mode (Prevent Stale Repeaters):** Turn this on if your region has only one observer. The nightly cleanup then skips your region's repeaters completely: they're never marked stale, never marked Inactive and never deleted. Ghost cleanup still runs.

### Notifications (Webhooks)

Sends alerts to a **webhook** (Slack, Home Assistant, your own automation, and so on).

  - **Webhook URL:** The HTTPS address to send to. Click **Send Test** to check it.
  - **Events to send:** Ambiguous Repeater ID, Pending Repeater, Offline Observer, Visitor Message, Suspicious Flight and Pending Repeater Link.

The webhook turns itself off after 3 permanent failures. See [Webhooks](webhooks.md).

### Region Boundary

Where your region is and what counts as inside it. See [Defining a Region's Boundary](region_boundaries.md) for a step-by-step guide.

  - **Center of Region:** A pin you can drag.
  - **Country:** The two-letter country code.
  - **Region Radius:** Worked out from the boundary. You can't edit it.
  - **Auto Boundary:** Loads real borders from OpenStreetMap (or geoBoundaries). Drag the pin, pick **State/Prov**, **County** or **Local**, click the areas you want, then click **Use selected**.
  - **Draw Boundary** (under Advanced Mapping): Draw or edit the boundary by hand.
  - **Import GeoJSON:** Paste a `Polygon`, `MultiPolygon`, `Feature` or `FeatureCollection`. Only use custom GeoJSON in special cases.
  - **Export GeoJSON:** Downloads the current boundary. Do this before a big change.

### Multi-region groups

A group panel splits settings between the group and its member regions.

**Group Defaults** (apply to every member region):

  - Stale Repeater Age
  - Pending Link Distance
  - Neighbour links
  - Scopes to Monitor
  - Mesh Scopes retention
  - Stale Ping Cleanup, including Backfill Purge across every member region
  - Disable Detailed Statistics
  - Disable Duplicate ID Detection Logic

The group panel also has **Wardriving → Radio Channels** (Slots are totals for the whole group), **Public Display** and **Group MQTT Brokers**.

**Per region**, in each member region's card on the group panel:

  - New Repeaters Enter Pending State
  - Public Channels
  - Wardriving Scope
  - Single Observer Mode
  - MQTT Observers and Subscribe to all local observers
  - Webhook settings
  - Region Boundary

On a member region's own panel you'll see *"This region is part of a multiregion group. Some settings cannot be edited here."* **Repeater Inactive After**, **Repeater Retention**, **Ghost Retention** and **CARpeater Retention** are read-only in a group; ask MeshMapper staff to change them.

## User Settings

### My Account

Your MeshMapper account: the same login for the [portal](portal.md) and every admin panel.

  - **Username** and **Email** (shows whether it's verified).
  - **Change password**, or **Set password** if you don't have one yet. If you sign in with Discord, you can **Remove password**.
  - **Link Discord** / **Unlink Discord**.
  - **Contact info:** Shown to other admins in the Administrators tab and to visitors in the map's **Region Info**.

### Notifications

Discord DMs from the MeshMapper bot, with one set of boxes per region. You need Discord linked to your account.

  - **Ambiguous Repeater ID:** A repeater's ID collides with another's, making them Ambiguous. See [Duplicate Repeater IDs](duplicaterepeaterid.md).
  - **Pending Repeater:** A daily reminder when your region has repeaters waiting for approval. Only useful when **New Repeaters Enter Pending State** is on.
  - **Messages From Visitors:** Lets map visitors message you from your region's **Region Info**.
  - **Offline Observer:** Once a day, MeshMapper checks each observer that sent data in the last 7 days. If it hasn't sent anything within your **Stale Repeater Age**, you get an alert.
  - **Suspicious Flight:** A live session has pings moving faster than any ground vehicle. Matches **Suspicious Live Sessions** in the Alerts tab.
  - **Pending Repeater Link:** A daily summary of repeater IDs whose pings are held for review. Each ID notifies once, and again only if its situation changes. See [Pending Repeater Links](#pending-repeater-links).
  - **Ping Purge Cleanup Report:** What [Stale Ping Cleanup](#stale-ping-cleanup-auto-delete-orphaned-pings) removed, broken down by date and repeater. Groups get one combined message. Only sent when something was deleted. DM only; there's no webhook for it.

The other events can also go to a webhook; see [Notifications in Settings](#notifications-webhooks).

### API Access

Create an integration key for the [Coverage API](coverage-api.md) and the other [read APIs](api-keys.md). Each admin gets one key per region, limited to 100 Coverage requests a day (usage shows as "n / 100"). A description is required. **Regenerate integration key** replaces your key; the old one stops working straight away.
