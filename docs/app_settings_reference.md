# Settings Reference

Complete reference for every setting in MeshMapper. The Settings tab is a list of folders, and each folder opens its own page. The headings below follow the app: one section per folder, then the groups you see inside it.

!!! warning
    Some settings are locked while auto-ping is running. A yellow banner appears at the top of Settings and on each folder page when this is the case. Stop auto-ping to change locked settings.

---

## General

*Appearance, sounds, background location*

### Appearance

#### Theme

- Toggle between **Dark mode** (default) and **Light mode**
- Dark mode recommended for wardriving at night to reduce glare

#### Units

- **Metric** (km, m, default) or **Imperial** (mi, ft)
- Affects distance displays throughout the app: zone distances, ping distances, GPS simulator speed

### Sounds

#### Sound Notifications

- Plays sounds on ping events. Sounds follow your phone's **media volume**.
- When enabled, three individual sounds can be toggled:
    - **Ping Sent**: Sound when a TX ping or discovery is sent
    - **Response Received**: Sound when a repeater echo or RX is received
    - **Disconnect Alert**: Triple beep when pinging stops unexpectedly (e.g., BLE drop mid-session)
- Coexists with other audio (transient focus with ducking on Android, ambient on iOS)
- Useful when wardriving with phone mounted out of view

### Location (Mobile only)

#### Background Location

- Prompts for "Always" location permission for continuous GPS tracking when the app is backgrounded
- **Android**: Background operation uses a foreground service. Enabling this grants "Always" location permission for improved GPS consistency.
- **iOS**: Required for reliable background wardriving. Without it, iOS may throttle or stop GPS updates when the app is not in the foreground.
- The app cannot take a permission away again, so switching this off opens the system settings for you to change it there

### Live Activity (iOS only)

#### Repeater Names on Live Activity

- Chooses how the Top Heard list is drawn on the Live Activity (Lock Screen and Dynamic Island), CarPlay and Apple Watch
- **On** (default): named rows, one repeater per line
- **Off**: a compact grid that fits more repeaters

### Exit (Android only)

#### Close App After Disconnect

- App automatically exits after disconnecting from your radio
- Disabled by default

#### Close App

- Immediately exits the app
- Confirmation dialog. Warns if connected.

---

## Map

*Map tiles, coverage overlay, markers*

### Map Tiles

#### Offline Maps (Mobile only)

Download map areas to your device for wardriving without a data connection. Opens the **Offline Maps** screen:

- **Download Area**: Pick a map style (Liberty, Dark, or Light; Satellite is not downloadable), a zoom range, and an area on the map. An estimated tile count is shown before downloading.
- **Storage**: Shows downloaded areas and the ambient cache (tiles auto-cached while panning), with a configurable storage limit and options to clear or delete.

#### Use Downloaded Tiles Only

- When enabled, the map uses **only** your downloaded areas, with no network tile requests at all
- Useful for guaranteed offline operation or saving mobile data

### Coverage Overlay

#### Coverage Overlay Opacity

- Slider (30% to 100%, default 70%) controlling how strongly the community coverage overlay is drawn over the base map

#### Grid Mode

- **Simplified** (default): 300m coverage cells, merged cells, grouped repeaters. Loads faster.
- **Detailed**: 100m coverage cells with finer detail and non-grouped repeaters.
- Matches the Grid Mode option on the web map
- Also sets the square size [Smart Pinging](#smart-pinging) uses, so what is deferred matches what is painted

#### Color Vision

- Choose a colour palette optimised for your vision type: Default, Protanopia (red-blind), Deuteranopia (green-blind), Tritanopia (blue-blind), or Achromatopsia (monochrome)
- Applies to the coverage overlay and map colours, matching the web map's accessibility palettes

### Markers

#### Map Marker Style

- Choose the visual style used for ping markers on the map: **Dot** (default), **Outlined Dot**, **Pin**, or **Diamond**

#### GPS Marker

- Choose the marker that represents your position: **Arrow** (default), **Car**, **Bike**, **Boat**, **Walk**, **Dog**, or **Chomper** (which faces your direction of travel)

#### Top Repeaters on Map

- Shows the **Top Heard** overlay on the map with the best 3 repeaters by SNR from your most recent ping
- Disabled by default

---

## Wardriving

*Auto-ping, privacy, CARpeater filter, modes, radio*

### Privacy

#### Anonymous Mode

- Renames your companion device to **"Anonymous"** on the mesh (requires a clean disconnect to reset your node name)
- Changing while connected triggers a brief reconnection
- Confirmation dialog when enabling or disabling while connected
- Cannot change while auto-ping is running

#### Broadcast My Coordinates

- **Disabled by default.** By default, your TX pings do **not** contain your GPS position on the air. They carry a short anonymous token instead, and your coordinates travel only to the MeshMapper server over the internet. Anyone listening on the wardriving channel sees the token, not your location.
- Enabling this appends your real GPS coordinates to the on-air ping message, visible to anyone with the community channel key.
- Leave this off unless you specifically want your live position visible on the mesh (e.g., so local mesh users can follow your drive in real time).

### Auto-Ping

#### Auto-Ping Interval

How frequently pings are sent in Active, Hybrid, and Trace modes:

- **15 seconds**: Fast (more coverage, causes more mesh load)
- **30 seconds**: Normal (balanced coverage and mesh load, default)
- **60 seconds**: Slow (less coverage, little mesh load)
- Cannot be changed during auto-ping
- Regional admin may enforce a minimum interval. Faster choices are greyed out and marked "Set by Regional Admin".

!!! note
    Does not affect Passive Mode (fixed 30-second discovery interval). In Hybrid Mode, the effective interval between channel messages is doubled since discovery requests alternate with TX.

#### Min Ping Distance

Minimum distance you must move before the next auto-ping. Prevents spamming from a stationary position.

- Enter any value in meters (free-text input)
- **Default**: 25m
- **Minimum**: 25m (enforced by the app)

!!! note
    Does not apply to manual pings. Cannot be changed during auto-ping.

#### Smart Pinging

Defers auto pings in squares that already have recent coverage, so your airtime goes where it adds something new. See [Smart Pinging](app_wardriving_modes.md#smart-pinging) for how it behaves on the road.

- **Enabled by default**
- Tap the **(i)** beside the switch for a short explanation inside the app
- **Defer pings in squares covered within**: the window, in days, that makes a square count as covered. Enter any whole number from **1 to 365**. Default **14 days**. Shown only while the switch is on.
- Applies to Hybrid, Passive and Active modes. Never affects manual pings, Trace Mode or passive RX listening.
- Deferred squares still earn leaderboard points (1.5 each) once MeshMapper verifies them
- May be enforced by regional admin (shown in amber). When enforced, the switch is locked on and the window is the region's.
- Cannot be changed during auto-ping

#### Auto-Stop After Idle

- Automatically stops auto-ping after **30 minutes without GPS movement**
- Prevents unnecessary transmissions and saves battery
- Enabled by default
- Cannot be changed during auto-ping

### CARpeater

A "CARpeater" is a repeater mounted in your vehicle or carried with you. Without filtering, every ping would show it as "heard" with an extremely strong signal and the coverage map would fill with false data. Three layers deal with this: your own CARpeater's key, the region's shared list, and the RSSI failsafe.

#### CARpeater Filter

Strips your own CARpeater from results. Switching it on for the first time opens the **My CARpeater** dialog, and a **My CARpeater** row stays under the switch while it is on.

- Enter the full **public key** of your CARpeater (64 hex characters), or tap **Choose from repeater list** to pick it from the repeaters the app already knows. The key is checked before it can be saved.
- **Pass-through**: an echo or RX packet that came through your CARpeater is stripped of that hop and the repeater behind it is credited instead. A packet that only reached your CARpeater is dropped, and so is a discovery response from it.
- Your key is shared with MeshMapper so that every wardriver in the region filters your CARpeater too (see Regional CARpeaters below)
- Cannot be changed during auto-ping

!!! note "Upgrading from an older version"
    Earlier versions accepted a short hex ID prefix. That prefix is no longer used. If you had one set, the app asks for the full key after your next connect, with a button to this page. "Not now" asks again after the next connect; "I don't use a CARpeater" stops asking.

#### Regional CARpeaters

- Shows how many CARpeaters have been shared for your region, with a list (name and key) when there are any. Your own is marked "Mine".
- These are always filtered and cannot be turned off: someone else's CARpeater is in someone else's car, so neither it nor the repeater behind it may be credited
- The list is refreshed from MeshMapper on every connect. Offline Mode keeps the last copy.

#### Disable RSSI Filter

By default, the app drops any packet with RSSI equal to or stronger (closer to 0) than -30 dBm because a signal that strong almost certainly came from a co-located repeater and is not meaningful coverage data. Only disable this if you are certain no co-located repeater is within range. If disabled while a CARpeater is present, your device will report false coverage data to the MeshMapper community map, degrading accuracy for everyone.

- Default: Drops packets with RSSI of -30 dBm or stronger (carpeater threshold)
- Enabling allows **all signal strengths** through
- Confirmation dialog warns about community map impact before enabling
- Cannot be changed during auto-ping

### Modes

#### Flood Traffic

- Shows or hides the **Active Mode**, **Hybrid Mode**, and manual **Send Ping** controls (everything that sends flood channel messages)
- **Off by default.** On a fresh install only Passive and Trace modes appear on the Map tab. Turn this on to wardrive with channel messages.
- May be locked off by your regional admin if the region has disabled flood wardriving traffic (shown with a blue note)
- Cannot be changed during auto-ping

#### Hybrid Mode

- Alternates between TX channel messages and discovery requests each interval
- Produces richer data with **50% fewer channel messages** (less mesh flooding)
- Enabled by default across all regions. Tap the **(i)** beside the switch for how the interval timing works.
- May be locked by regional admin (shown in amber when enforced)
- Cannot be changed during auto-ping

#### Discovery Drop

- Counts discovery requests with **no response** as "failed pings" reported to the API
- Helps identify dead zones for network planning
- Requires repeater firmware **1.10+** to respond to discovery requests
- Disabled by default
- May be enforced by regional admin (shown in amber when set)
- Confirmation dialog before enabling
- Cannot be changed during auto-ping

### Radio

#### TX Bytes

Repeater ID size in TX/RX path hops:

- **1 byte**: 256 unique IDs, standard for most networks
- **2 bytes**: about 65K unique IDs, reduces collisions
- **3 bytes**: about 16M unique IDs, maximum resolution

!!! warning
    Requires both your companion device and repeaters to be on firmware **1.14+**. Only change this if you understand what you're doing, or if your regional admin has enforced a value. RX always auto-detects the sender's byte size regardless of your TX setting.

**States:**

- "Set by Regional Admin" (amber) when region enforces a value
- "Firmware 1.14+ required" (amber) if firmware is too old
- "Connect to radio to configure" (amber) when disconnected
- Cannot be changed during auto-ping

!!! note
    Applied to your radio during connection, restored on clean disconnect.

#### Trace Bytes

Repeater ID size for trace path requests:

- **1 byte**, **2 bytes**, or **4 bytes**

This is separate from TX Bytes because traces use a different encoding in the MeshCore protocol (bitshift encoding vs simple counter). The size options don't match 1:1:

| TX/RX (simple counter) | Trace (bitshift encoding) |
|---|---|
| Mode 0: 1 byte | Mode 0: 1 byte |
| Mode 1: 2 bytes | Mode 1: 2 bytes |
| Mode 2: 3 bytes | Mode 2: 4 bytes |

!!! warning
    3-byte traces are not supported by the MeshCore protocol. When your region uses 3-byte TX paths, set Trace Bytes to 4.

!!! warning
    Requires companion firmware **1.14+**. Only change this if you understand what you're doing.

**States:**

- "Firmware 1.14+ required" (amber) if firmware is too old
- "Connect to radio to configure" (amber) when disconnected
- Cannot be changed during auto-ping

#### Delete Channel on Disconnect

- **Enabled** (default): Removes the #wardriving channel from your radio on disconnect. Keeps the radio clean.
- **Disabled**: Channel remains. Slightly faster reconnection since it doesn't need to be recreated.

---

## Data

*Queued pings, map markers, offline sessions*

### Current Session

#### Queued Pings

Shows how many items are waiting to be uploaded, with two actions beside the count:

- **Force upload**: Immediately upload all queued items
- **Clear queue**: Permanently delete all queued pings. Confirmation dialog included.

#### Clear Map Markers

- Removes all TX, RX, discovery, and trace markers from the map display
- Does not affect uploaded data or the upload queue

### Offline Sessions

Sessions recorded in Offline Mode. Each session shows:

- Filename (date-based)
- Ping count and date
- Device name

**Actions per session:**

- **Download**: Save the raw JSON to your device (via the system share sheet on mobile). Always available.
- **Upload**: Send to MeshMapper servers. Shown until the session has been uploaded.
- **Delete**: Remove from local storage

After an upload the session shows an "Uploaded" line with where its pings were placed. Tap it for the **Upload Summary**: the number of pings credited to each region, and any that were dropped for being more than 50 km outside every region.

---

## MeshMapper Account (Mobile only)

*Sign in to link your radios*

Signs you in to your [My MeshMapper](portal.md) account and links your radios to it, so their wardriving counts toward your account. Linking is best-effort and never affects a connection.

### Account

- **Sign in to MyMeshMapper**: Opens the portal sign-in page in your system browser. Finish signing in there and return to the app; the app never sees your password.
- Once signed in, the row shows your display name and username
- **Sign Out**: Signs the app out. Your linked devices stay on the server.
- The **refresh** button in the top bar re-reads your account. It is rate limited, and the app says how long to wait if you refresh too often.

### Overview

Shown once you are signed in, when the server provides it: your **Points**, **Grid squares** and number of **Companions**, plus your award badges (tap one for its description). The totals are the same ones the portal's Overview tab shows, summed across all your linked radios.

### Devices

- **This Device**: The connected radio. **Link now** has the radio sign a one-time challenge to prove it is yours; **Unlink** removes it. Needs a connected radio and is locked during auto-ping.
- Below it, every companion linked to your account, with its name, key and points
- **Re-enable Link Prompts**: Appears after you have declined a link prompt, or a radio was recorded as unable to sign. Clears those records so the app asks again.

!!! note
    After you connect a radio that is not yet linked, the app offers to link it. It asks at most once per radio per app session, and never while auto-ping is running.

---

## API Endpoints

*MeshMapper and custom endpoints*

### MeshMapper

#### MeshMapper API

- Always active. This is where your wardriving data goes.

### Custom Endpoint

#### Custom API Endpoint

Forward your wardrive data to a third-party HTTPS endpoint **in addition to** MeshMapper:

- A **Third-Party Data Sharing** notice must be accepted the first time it is enabled
- **Endpoint URL** and **API Key** fields (HTTPS is required; the key is sent as an `X-API-Key` header)
- **Include Contact Key**: Optionally share your device's public key prefix with the endpoint (on by default, can be disabled)
- **Import from Clipboard**: Paste a `meshmapper://custom-api?...` configuration link from an endpoint operator to auto-fill both fields
- Best-effort and fire-and-forget. A broken custom endpoint never affects your MeshMapper uploads.
- Everything MeshMapper receives is forwarded, including [Smart Pinging](app_wardriving_modes.md#smart-pinging) deferrals

See the [Third Party API guide](app_third_party_api.md) for the full payload contract (aimed at endpoint developers).

---

## Apple Watch (iOS only)

*Inspect pairing and delivery state*

This folder appears once an Apple Watch has been paired with your phone, and stays after an unpair, because that is when it is most useful. It opens the **Watch Connectivity** page for diagnosing a watch app that is not updating:

- **Sync gate**: whether the phone is currently allowed to send to the watch, and why not
- **Last successful send**, **Last availability change** and **Last send outcome**
- **Refresh** re-reads the state

---

## About & Support

*Version, feedback, debug logs*

### About

- **MeshMapper**: App name and tagline
- **Version**: Tap to copy the version to the clipboard. Seven quick taps unlock the [Developer Tools](#developer-tools) folder.

### Links

- **GitHub**: View issues and source code
- **Discord**: Join the community chat
- **Community**: Built with contributions from the Greater Ottawa Mesh Radio Enthusiasts community
- **Buy us a coffee**: Support MeshMapper development (not shown on iOS)

### Support

#### Submit Feedback

- Opens the bug report dialog to report bugs or request features
- Can attach debug log files if logging is enabled (select which files to include)

#### Debug Logs (Mobile only)

- Writes detailed debug logs to files on your device
- Orange "LOGGING" badge when active
- Timestamped entries, auto-rotate (max 10 files, max 4.5 MB per file)
- Always disabled on app start (must re-enable each session)

**When logs exist:**

- **Log file list**: Date, size, active status
- **View**: In-app log viewer
- **Share**: System share sheet
- **Upload**: Send to the MeshMapper team for analysis
- **Delete All**: Remove all stored log files

---

## Developer Tools

*GPS simulator*

Hidden until unlocked by tapping the version seven times on About & Support.

### Developer Mode

- Switch it off to hide the Developer Tools folder again

### GPS Simulator

Replaces the phone's GPS with a simulated position, for testing without leaving the desk. An orange "SIMULATED" badge shows while it is on.

- **Simulation Speed** and **Simulation Altitude** sliders
- **Movement Pattern**: Straight Line, Circle, or Random Walk
- **Load Route File**: Follow a KML or GPX route instead of a pattern. Shows the route name and point count once loaded, with a button to clear it.
- **Reset Position**: Back to the start of the route, or to downtown Ottawa when no route is loaded
