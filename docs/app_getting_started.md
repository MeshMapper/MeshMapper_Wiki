# Getting Started

Welcome to MeshMapper, a community-driven wardriving app for MeshCore mesh network devices. MeshMapper lets you connect to a MeshCore radio over Bluetooth, send GPS-tagged pings across the mesh, and contribute coverage data to the [MeshMapper community map](https://meshmapper.net/).

---

## What You Need

1. **A MeshCore-compatible radio device**
— Any device that supports MeshCore will work with MeshMapper. It is recommended to run up-to-date firmware on your device, as some features require v1.14.0 or newer.
2. **A phone or computer** — Android, iOS, or a Chromium-based browser (Chrome or Edge)
3. **GPS/location services** enabled on your device
4. **Bluetooth** enabled on your device

---

## Get the App

**App Store Releases:**

- **Android:** [Get it on the Play Store](https://play.google.com/store/apps/details?id=net.meshmapper.app)
  - You can also grab the [APK from GitHub](https://github.com/MeshMapper/MeshMapper_Project/releases/) if you prefer sideloading
- **iOS:** [Get it on the App Store](https://apps.apple.com/us/app/meshmapper/id6758073991)

**Web (Chrome/Edge only):**

- [wd.meshmapper.net](https://wd.meshmapper.net)
- Requires Chrome or Edge (Safari is not supported, it lacks the Web Bluetooth API)

!!! note
    The web app is experimental and has not been widely tested. It should be technically stable, but the mobile apps are the recommended experience.

---

## First Launch

When you first open MeshMapper, you will see a **location disclosure dialog** explaining why the app needs GPS access. This dialog explains that MeshMapper collects your location to:

- Track where you send pings on the mesh network
- Map coverage areas for the community
- Record which repeaters hear your device

It also discloses that your location data is uploaded to the MeshMapper API and displayed on public coverage maps at meshmapper.net. If you prefer to be more anonymous, enable the Anonymous Mode feature in Settings, or wardrive in Offline Mode and never upload your sessions.

!!! info "What is a 'ping'?"
    Throughout MeshMapper, "ping" refers to any packet the app sends out on the mesh. This includes channel messages (TX), discovery requests (DISC), and trace requests (TRC). Each type works differently, but they are all "pings."

After tapping **Continue**, your phone will ask for location permission. Grant "While Using the App" at minimum.

!!! warning "iOS Background Location"
    If you want to run MeshMapper in the background on iOS (e.g., wardriving with the screen off), you need to manually enable "Background Location" in the MeshMapper Settings tab. Apple restricts apps from requesting background location directly, so the user must enable it themselves. Without this, iOS will throttle or stop GPS updates when the app is not in the foreground.

---

## Connecting to Your Radio

1. **Navigate to the Connect tab** (the Bluetooth icon in the bottom navigation bar)
2. **Make sure your radio is powered on** and nearby
3. **Tap "Scan for Devices"** to start a Bluetooth scan. Your MeshCore device should appear in the list within a few seconds.
4. **Tap your device** to begin the connection process

The app runs a **9-step connection sequence** automatically:

| Step | What Happens |
|------|-------------|
| 1. Connecting to device | Establishes a BLE connection to your radio |
| 2. Protocol handshake | Verifies the app and firmware can communicate |
| 3. Querying device info | Retrieves your device's manufacturer string and public key (required for API auth) |
| 4. Identifying device | Matches your radio against the device database to determine model and TX power |
| 5. Syncing time | Synchronizes your radio's clock with your phone |
| 6. Acquiring API session | Authenticates with the MeshMapper API, gets zone info and regional settings |
| 7. Setting up channel | Creates the #wardriving channel on your radio |
| 8. Initializing GPS | Waits for a GPS lock on your phone |
| 9. Connected | Ready to wardrive |

Once complete, the Connect tab icon turns **green** and the label changes to "Connected."

!!! tip
    MeshMapper remembers your last connected device. On future launches, you can tap the remembered device to reconnect quickly without scanning.

!!! note "Not just Bluetooth"
    Bluetooth is the standard way to connect, but the Connect tab also supports **TCP** (network-attached radios, Android/iOS) and **USB Serial** (Android via OTG cable, or Chrome/Edge on the web). See the [Connection Guide](app_connection_guide.md) for details.

---

## Your First Ping

Before you can send a ping, two things need to be set:

1. **External antenna** — On the Map tab, the Controls panel asks "External Antenna?" Tap **Yes** or **No**.
   - This is required before any pings can be sent
   - Select **Yes** if your antenna has a clear, unobstructed path to the sky (e.g., mag-mount on a car roof, antenna outside a window)
   - Select **No** if your radio is inside a vehicle (cup holder, dash), inside a bag, or otherwise obstructed by metal or walls
   - The key distinction is whether the signal is obstructed, not just whether it is an external antenna. Being inside a metal car significantly reduces range.
   - This matters because the coverage map needs accurate data about signal conditions

2. **Coverage zone** — The status bar shows your zone status:
   - Green zone code (like "YOW") = you are in a zone and TX is allowed
   - Red zone code = you are in a zone but TX is at capacity (Passive Mode only)
   - Orange dash = you are outside any zone (or GPS is still searching)
   - Grey zone code = you are in a zone but not yet connected

Once both are set, tap **Send Ping**:

- The app sends a channel message to #wardriving
- This message **floods the entire mesh network**, with every repeater relaying it onward
- **Your GPS position is not in the on-air message.** By default the message carries a short anonymous token — your coordinates are sent only to the MeshMapper server over the internet. (You can opt in to broadcasting coordinates on the air via Settings > Ping Settings > Broadcast My Coordinates.)
- If your regional admin has configured a **scope**, the message stays within that region instead
- The app listens for **5 seconds** to see which repeaters echoed your message back
- On the backend, MeshMapper uses **MQTT observers** that also listen to the #wardriving channel. If an observer receives your message, the backend marks that ping as **bidirectional (bidir)**
- Results appear as markers on the map and entries in the Log tab

---

## Understanding the Status Bar

The status bar sits below the app bar on the Map tab:

- **Zone chip** (left): Zone code when in coverage, dash when outside, "GPS..." while acquiring. Tap for details.
- **TX**: Channel messages sent (flood the mesh, or scoped if your region has a scope set)
- **RX**: Mesh packets passively received
- **DISC**: Discovery requests sent
- **TRC**: Successful trace responses
- **Upload**: Pings successfully uploaded to MeshMapper servers

Tap any stat chip to see a description of what it means.

---

## What Happens to Your Data

Every ping you send (TX), mesh packet you passively receive (RX), and discovery response (DISC) is queued for upload to the MeshMapper API. The app batches these uploads (up to 50 at a time) and sends them automatically. You can see the current queue size in Settings under "Data > Queued Pings."

Your data contributes to the community coverage map at [meshmapper.net](https://meshmapper.net/), helping everyone understand where MeshCore mesh coverage exists.

---

## Next Steps

- [**Wardriving Modes**](app_wardriving_modes.md) — Learn about Hybrid, Passive, Active, and Trace modes
- [**App Tabs**](app_tabs.md) — Detailed walkthrough of each tab
- [**Settings Reference**](app_settings_reference.md) — Every setting explained
- [**Connection Guide**](app_connection_guide.md) — Deep dive into connection, reconnection, and offline mode
- [**Troubleshooting**](app_troubleshooting.md) — Common issues and how to resolve them
