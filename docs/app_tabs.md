# Using the App

MeshMapper has five tabs accessible from the bottom navigation bar:

- **Map** - Primary wardriving interface
- **Log** - Ping and error history
- **History** - Past session playback and noise floor graphs
- **Connect** - Device connection management (Bluetooth, TCP, USB)
- **Settings** - App configuration

---

## Map Tab

The Map tab is your primary wardriving interface. It shows a full-screen map with your GPS position, ping markers, and an overlay control panel.

### The App Bar (Portrait Mode)

In portrait orientation, the top bar shows:

- **"MeshMapper"** with your connected device name below it (or "Disconnected")
- **Noise floor indicator** (right): Current noise floor in dBm with colour coding
  - Below -100 dBm: great (green)
  - -100 to -90 dBm: okay (orange)
  - Above -90 dBm: noisy (red)
- **Battery indicator** (right): Radio battery percentage
  - 50%+ (green)
  - 20-50% (orange)
  - Below 20% (red)

### The Status Bar

Below the app bar is the status bar with tappable stat chips:

- **Zone chip** (left): Your current zone code. Tap for details. The popup changes based on your state: zone name and TX slots available (green), zone at TX capacity with Passive Mode suggestion (red), distance to nearest zone (orange), or "Connect to a device to start wardriving" (grey, when in zone but not connected).
- **TX** (green): Channel messages you have sent. These are flood messages that propagate across the mesh (or are regionally scoped if your zone admin has set a scope).
- **RX** (purple): Mesh packets passively received.
- **DISC** (cyan): Discovery requests sent.
- **TRC** (blue diamond): Successful trace responses.
- **Upload**: Pings successfully uploaded to the server.

Each stat chip animates with a bounce effect when its count increments, making it easy to notice activity. Tap any chip to see a description of what it tracks.

### The Map

The map shows your current position and wardriving data.

#### GPS Info Overlay (Top Left)

- **GPS accuracy**: Colour-coded readout in meters (or feet if imperial is enabled)
  - 10m or better (green)
  - 10-30m (orange)
  - Worse than 30m (red)
  - "No GPS" if there is no fix (black)
- **Distance from last ping**: How far you have moved since your last ping. Helps you see at a glance whether you have met the minimum distance requirement for auto-ping modes.

#### Map Controls

Expand the map controls panel to access:

- **Map Style**: Cycle between Liberty (standard), Dark, Light, and Satellite map styles
- **Coverage Overlay**: Toggle the MeshMapper community coverage overlay on the map. Shows coverage data reported by all wardrivers in your zone. Only available when in an onboarded region/zone.
- **Repeaters**: Show or hide repeater markers
- **Region Boundary**: Show or hide your region's boundary line and label
- **Auto-Follow**: Centers the map on your GPS position as you move
- **Always North**: Keeps north at the top. When disabled, the map can rotate with your heading.
- **Rotation Lock**: Disables rotation gestures entirely
- **Legend**: Opens a legend showing what the map markers and colours mean

#### Markers

Ping markers appear on the map as you wardrive. Tap any marker to view its details.

**Your session markers:**

These show what **your device** observed locally over BLE. The app only knows what it saw directly, not what happened on the backend. For example, a green TX marker means a repeater echoed your message back to *you*, but the app has no way of knowing whether that message also made it through the mesh to a backend MQTT observer. Similarly, a red TX marker means no repeater echoed back, but the message may still have been received by the backend through a different path (which would show as an orange TX on the coverage overlay).

- **TX (success)** (green): You sent a channel message (flood) and at least one repeater echoed it back directly
- **TX (multi-hop only)** (purple): Your channel message was echoed back, but only via multi-hop paths (no direct single-hop repeat). Echoes are grouped under the parent TX ping and shown as "Direct Repeats" and "Multi-hop Repeats" in the details.
- **TX (fail)** (red): You sent a channel message but no repeater was heard
- **RX** (purple): You passively received a message from the mesh
- **DISC (success)** (cyan): You sent a discovery request and a repeater responded
- **DISC (fail)** (grey/red): You sent a discovery request but no repeater responded. Shown as red if your region has "Count DISC as failed" enabled, meaning the backend will track a failed discovery as no coverage at that location.
- **TRC (success)** (blue diamond): A trace reached the target repeater
- **TRC (fail)** (grey): A trace got no response

**Coverage overlay markers** (when coverage overlay is enabled):

These show the **backend's view** of coverage, combining data from all wardrivers and MQTT observers across the entire mesh. The backend has information your device does not, such as whether a message was received by an MQTT observer on the other side of the mesh. This is why the overlay uses different categories than your session markers.

- **BIDIR** (green): Heard repeats from the mesh AND successfully routed through to a backend observer
- **DISC** (cyan): A wardriver sent a discovery packet and heard a reply
- **TX** (orange): Successfully routed through to a backend observer, but no repeats heard back by the wardriver
- **RX** (purple): Heard mesh traffic but did not transmit
- **DEAD** (brown): A repeater heard it, but no other radio received the repeat
- **DROP** (red): No repeats heard AND did not reach a backend observer. Also includes failed discovery requests if the region has "Count DISC as failed" enabled, meaning the backend tracks a failed discovery as no coverage at that location.

The overlay renders from the same vector coverage tiles as the web map, using your selected **Grid Mode** (Simplified 300m or Detailed 100m — see Settings > Map Management) and Color Vision palette. After a successful upload, your own newly-mapped cells refresh in place within about 10 seconds — you can watch your coverage appear as you drive.

**Tap to inspect:**

- **Tap a coverage cell** to open a summary of its pings, with dashed connection lines fanning out to every repeater that heard that spot (each line labelled with distance).
- **Tap a repeater** to see its details plus all the coverage cells it has been heard from, colour-coded by status, while the rest of the map dims so its footprint stands out.

If "Top Repeaters on Map" is enabled in Settings, a **Top Heard** overlay appears on the map.

**Top 3 slots**: Shows the best 3 repeaters by SNR from your most recent ping, fully replacing on each new ping. If a ping gets no responses, the previous results stay visible. Each row has a coloured dot indicating the ping type:

- TX ping (green) - Active/Hybrid channel message
- Discovery ping (cyan) - Passive/Hybrid query
- Trace ping (blue diamond) - Trace mode, specific repeater

**RX slot**: A 4th row shows the strongest passively overheard repeater (purple) within a rolling window that matches your auto-ping interval (15s, 30s, or 60s).

Each row also shows the repeater's hex ID and SNR value, colour-coded: green (good, above 5), orange (okay, -1 to 5), red (poor, below -1).

The overlay clears when you stop auto-ping, switch modes, disconnect, or clear pings/logs.

Example:

```
Top Heard
🟢 A1B2  8.5
🟢 C3D4  3.2
🟣 E5F6  1.0
🔵 7A8B -2.0
```

### The Control Panel

The control panel floats at the bottom of the map and contains everything you need to wardrive:

- **External Antenna Selector**: A "Yes / No" toggle that you must set before sending any pings. See [Getting Started](app_getting_started.md) for when to select Yes vs No.
- **Send Ping**: Sends a single channel message to #wardriving that floods the entire mesh (or is scoped to your region), then listens 5 seconds for repeater echoes. Disabled if you haven't set your antenna preference, don't have GPS, or aren't in a zone.
- **Hybrid / Active Mode**: Starts automated wardriving at your configured interval. Hybrid Mode (default) alternates between channel messages and discovery requests. See [Wardriving Modes](app_wardriving_modes.md) for details.
- **Passive Mode**: Discovery-only mode (no channel messages, no mesh flooding). Sends discovery requests every 30 seconds and passively monitors mesh traffic.
- **Trace Mode**: Target a specific repeater by its hex ID and send trace path requests at your configured interval.
- **Help**: Opens a bottom sheet explaining what each button does.

You can minimize the control panel to a compact bar showing just the essential buttons, or hide it entirely (a floating "Controls" button appears to bring it back).

### Landscape Mode

In landscape orientation, the app removes the traditional app bar and replaces it with a compact floating status bar at the top of the map. The control panel becomes a floating side panel on the left. Map controls appear on the right side of the map. This gives you maximum map visibility for wardriving in a car mount.

---

## Log Tab

The Log tab shows a detailed record of all your wardriving activity, organized into two sub-tabs: **All Pings** and **Errors**.

### All Pings

A unified chronological view of every TX, RX, DISC, and Trace event. At the top:

- **Search bar**: Filter entries by repeater name or hex ID. Searching by name finds all repeaters whose name contains the query. Searching by hex ID matches IDs that start with the query.
- **Filter bar**: Four toggleable segments (TX, RX, DISC, TRC) each with a count badge. Tap to show/hide that type. At least one must remain active.

Each entry is a card showing:

- **Type badge**: Colour-coded label (green TX, purple RX, cyan DISC, cyan diamond TRC). TX entries are channel messages that flooded the mesh (or were regionally scoped).
- **Timestamp**: When the event occurred
- **Location**: GPS coordinates at the time of the event
- **Repeater table**:
  - TX: Table of repeaters that echoed your message, with Node ID, SNR, and RSSI
  - RX: Single repeater row
  - DISC: Table with RX SNR, RX RSSI, and TX SNR
  - Trace: Target repeater and signal quality

**Tapping a card** navigates to the Map tab and centers on that event's GPS coordinates.

**Tapping a repeater ID** in any table opens a popup showing matching repeaters from the mesh database. Each match shows the repeater's name, a coloured hex ID badge, distance from your current GPS position (sorted closest first), and an Active/Stale status badge. For discovery pings, the popup uses exact 4-byte public key matching for precise identification. For TX/RX pings (which only have 1-byte path IDs), it uses prefix matching, so multiple repeaters may appear if they share the same first byte.

### Errors

The Errors sub-tab shows warnings and errors that occurred during your session:

- **Info** (blue): Informational messages
- **Warning** (orange): Warning conditions that may need attention
- **Error** (red): Errors that likely affected functionality

A badge appears on the Log tab icon when there are unread errors.

### Log Actions

The overflow menu (⋮) in the top right offers:

- **Copy CSV**: Copies the current tab's data to your clipboard in CSV format. If you have a search filter active, only filtered entries are exported.
- **Clear all logs**: Removes all TX, RX, DISC, Trace, and error log entries.

---

## History Tab

The History tab (titled **Session History**) lists your past wardriving sessions. Each session card offers two views:

- **View on Map**: Replays the session's pings as markers on the map, zoomed to fit the session's area. Tap any marker for the same detail sheets as during live wardriving.
- **Noise Floor**: Opens the interactive noise floor graph for that session (see below).

### Noise Floor History

Alongside session playback, MeshMapper records the ambient radio noise measured during each session.

### What is Noise Floor?

The noise floor is the baseline level of radio signal present in the environment when nobody is transmitting. Measured in dBm (decibels relative to milliwatt), a lower number means a quieter, cleaner radio environment:

- **-120 to -100 dBm**: Excellent, very quiet (green)
- **-100 to -90 dBm**: Moderate noise (orange)
- **Above -90 dBm**: High noise, may interfere with mesh communication (red)

MeshMapper polls your radio's noise floor every 5 seconds while connected and in auto-ping mode.

### Session List

Each session card shows:

- **Mode icon**: Upload arrow for Active/Hybrid, Ear for Passive
- **Mode name and date**: When the session started
- **Duration**: How long the session lasted
- **Sample count**: How many noise floor readings were taken
- **Event count**: How many ping events occurred during the session

The currently active session appears at the top with a green **"LIVE"** badge.

### Full-Screen Graph

Tap a session to open the full-screen interactive graph:

- **Noise floor line**: Colour-coded by level (green/orange/red) over time
- **Event markers**: Coloured dots marking when ping events occurred:
  - TX channel message (green) - heard by a repeater (success)
  - TX channel message (red) - not heard
  - Passive RX received (purple)
  - Discovery got a response (cyan)
  - Discovery with no response (grey) - or failed discovery if "Count DISC as failed" is enabled at the region level
  - Trace got a response (blue diamond)
  - Trace with no response (grey)

**Interactions**:

- **Pinch to zoom** on a specific time range (minimum 10-second visible window)
- **Drag to pan** across the timeline
- **Tap a marker** to open a detail sheet with event type, timestamp, interpolated noise floor, and repeater table
- **Reset zoom** (top right) returns to full session view

Live sessions update every 2 seconds. If the session ends while you are viewing it, the "LIVE" badge disappears and the graph becomes a static historical view.

### Clearing Sessions

Use the trash icon in the top right to delete all saved sessions. The current active session is not affected.

---

## Connect Tab

The Connect tab manages your device connection. Its appearance changes based on your connection state.

### Connection Methods

A selector at the top lets you choose how to connect to your MeshCore device:

- **BLE** (Bluetooth Low Energy) — available on all platforms. The standard way to connect.
- **TCP** — available on Android and iOS. Connect to a network-attached MeshCore device by host and port (default port 5000), e.g. via a WiFi companion or a ser2net bridge. Saved connections are remembered.
- **USB** — available on Android (USB OTG cable) and in the web app (Chrome/Edge via Web Serial). Connect your radio directly with a cable.

### Zone Status Bar

Shown across all connection states when GPS is available:

- **Left**: City name of your current zone and IATA code. If you are outside a zone, shows distance to the nearest one.
- **Right**: Open TX slots (e.g. "3/5 Open"), colour-coded: green (plenty available), orange (2 or fewer left), red (none available)

### Disconnected

- "Go Offline" / "Go Online" button to toggle offline mode
- "Scan for Devices" button to start a BLE scan. Once scanning, a list of discovered devices appears with signal strength.
- Your last connected device shown for quick reconnection

### Connecting

- Progress indicator showing the current step of the 9-step connection process
- Cancel button to abort the connection

### Connected

- **Radio Info**:
  - **Companion name**: The name of your connected MeshCore device
  - **Power Level**: The TX power your device is reporting. Tap to open the power level selector (locked during auto-ping). If your device model was auto-detected, a green banner shows the detected model and wattage. Options: ≤22dBm (0.3W), 28dBm (0.6W), 30dBm (1.0W), 33dBm (2.0W). A checkmark shows the recommended value for your device. If you override the auto-detected power, a confirmation dialog appears. "Reset to Auto" restores auto-detection. This only affects what is reported to the API, it does not change your radio's actual output.
  - **Public Key**: Your device's unique public key, used for authentication with the MeshMapper API. Tap to copy to clipboard.
  - **Registered via**: Shows your device's registration level. Devices can be registered as anonymous (no contact info), or with a signed contact URI that links the device to a MeshCore identity. Higher registration levels may grant access to additional features.
- **Regional Settings**:
  - **Zone**: The zone you are connected to (typically a city name)
  - **Scope**: The flood scope configured by the regional admin for your zone
  - **Channels**: Additional channels configured by the regional admin
- "Go Offline" / "Go Online" button to toggle offline mode while connected
- Disconnect button

For a detailed walkthrough of the connection process, see the [Connection Guide](app_connection_guide.md).

---

## Settings Tab

The Settings tab contains all user preferences and configuration options. Settings are organized into sections: General, Map Management, Ping Settings, Modes, Filtering, Radio, Data, Offline Sessions, API Endpoints, About, Exit (Android only), and Debug.

Some settings are locked while auto-ping is running to prevent mid-session changes that could affect data consistency. A yellow banner at the top indicates when settings are locked.

For a complete reference of every setting, see the [Settings Reference](app_settings_reference.md).
