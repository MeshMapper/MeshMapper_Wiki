# Getting Started

Welcome to MeshMapper, a community-driven wardriving app for MeshCore mesh network devices. MeshMapper connects to your MeshCore radio, sends pings across the mesh, and adds what it hears to the [MeshMapper community map](https://meshmapper.net/). Your location goes only to the MeshMapper server; by default, pings on the air carry an anonymous token, not your coordinates.

---

## What You Need

1. **A MeshCore-compatible radio device**
— Any device that supports MeshCore will work with MeshMapper. It is recommended to run up-to-date firmware on your device, as some features require v1.14.0 or newer.
2. **An Android or iOS phone**
3. **GPS/location services** enabled on your phone
4. **Bluetooth** enabled on your phone (or use TCP or USB instead, see below)

---

## Get the App

**App Store Releases:**

- **Android:** [Get it on the Play Store](https://play.google.com/store/apps/details?id=net.meshmapper.app)
  - You can also grab the [APK from GitHub](https://github.com/MeshMapper/MeshMapper_Project/releases/) if you prefer sideloading
- **iOS:** [Get it on the App Store](https://apps.apple.com/us/app/meshmapper/id6758073991)

**Beta releases:**

To hear about betas, join the MeshMapper Discord server, open **Channels & Roles**, and opt in to beta testing. Then choose your platform:

- **iOS:** [Join the beta in TestFlight](https://testflight.apple.com/join/PXxfr5Jr).
- **Android:** [Download the beta APK from GitHub](https://github.com/MeshMapper/MeshMapper_Project/releases/), or [add MeshMapper to Obtainium](https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/%7B%22id%22%3A%22net.meshmapper.app%22%2C%22url%22%3A%22https%3A%2F%2Fgithub.com%2FMeshMapper%2FMeshMapper_Project%22%2C%22author%22%3A%22MeshMapper%22%2C%22name%22%3A%22MeshMapper%22%2C%22preferredApkIndex%22%3A0%2C%22additionalSettings%22%3A%22%7B%5C%22includePrereleases%5C%22%3Atrue%2C%5C%22fallbackToOlderReleases%5C%22%3Atrue%7D%22%2C%22overrideSource%22%3A%22GitHub%22%7D) to follow prereleases.

---

## First Launch

When you first open MeshMapper, you will see a **Location Access Required** dialog explaining why the app needs GPS access. It says MeshMapper collects your location to:

- Track where you send pings on the mesh network
- Map coverage areas for the community
- Record which repeaters hear your device

It also explains that your location data is uploaded to the MeshMapper API and used for the public coverage maps at meshmapper.net, and that Offline Mode stores data on your phone without uploading it.

!!! info "What is a 'ping'?"
    Throughout MeshMapper, "ping" refers to any packet the app sends out on the mesh. This includes channel messages (TX), discovery requests (DISC), and trace requests (TRC). Each type works differently, but they are all "pings."

After tapping **Continue**, your phone will ask for location permission. Grant "While Using the App" at minimum.

Next, a **Welcome to MeshMapper** prompt offers a short tour. Tap **Start Guide** to open the **Quick Guide**, 12 short pages ("Page X of 12") covering connecting, online vs offline, privacy, the antenna setting, CARpeaters, background use, modes, Smart Pinging, map controls, results, your account, and getting help. Tap **Skip Guide** to skip it. You can reopen it any time from **Settings > About & Support > Quick Guide**.

!!! tip "Privacy options"
    Two privacy settings live under **Settings > Wardriving > Privacy**:

    - **Anonymous Mode** renames your radio to "Anonymous" for mesh pings and keeps you off the public leaderboard. It hides your name only: your radio's public key is still used to sign in, and your sessions are still recorded against it.
    - **Broadcast My Coordinates** is off by default, so your coordinates are sent only to the MeshMapper server, not over the air.

    You can also wardrive in Offline Mode and never upload your sessions.

!!! warning "Wardriving in the background"
    To keep wardriving on iOS with the screen off or the app in the background, turn on **Background Location** under Settings > General in MeshMapper and allow location access **Always**. Without it, iOS may slow or stop GPS updates when the app is not in the foreground. Android needs no extra location permission, but some phones pause apps when the screen is off; if that happens, set MeshMapper's battery usage to **Unrestricted** in Android settings.

---

## Connecting to Your Radio

1. **Navigate to the Connect tab** (the Bluetooth icon in the bottom navigation bar)
2. **Make sure your radio is powered on** and nearby
3. **Tap "Scan"** at the bottom of the screen to start a Bluetooth scan. Your MeshCore device should appear in the list within a few seconds. Scan only works when you are inside a MeshMapper zone (or in Offline Mode).
4. **Tap your device** to begin the connection process

The app runs a **9-step connection sequence** automatically:

| Step | What Happens |
|------|-------------|
| 1. Connecting to device | Opens the Bluetooth, TCP, or USB link to your radio |
| 2. Protocol handshake | Verifies the app and firmware can communicate |
| 3. Querying device info | Retrieves your device's manufacturer string and public key (required for API auth) |
| 4. Identifying device | Matches your radio against the device database to determine model and TX power |
| 5. Syncing time | Synchronizes your radio's clock with your phone |
| 6. Acquiring API slot | Authenticates with the MeshMapper API, gets zone info and regional settings |
| 7. Setting up channel | Makes sure the #wardriving channel exists on your radio |
| 8. Initializing GPS | Starts GPS tracking on your phone |
| 9. Connected | Ready to wardrive |

Once complete, the Connect tab icon turns **green** and the label changes to "Connected."

!!! tip
    MeshMapper remembers your last connected device. On future launches, the **Last Connected Device** card lets you tap **Reconnect** without scanning (or **Forget** it).

!!! note "Not just Bluetooth"
    Bluetooth is the standard way to connect, but the Connect tab also supports **TCP** (network-attached radios, such as a Wi-Fi companion) and **USB** (Android only, via an OTG cable). Pick BLE, TCP, or USB in the bar at the bottom of the Connect tab. See the [Connection Guide](app_connection_guide.md) for details.

---

## Your First Ping

Before you can send a ping, two things need to be set:

1. **External antenna** — On the Map tab, the Controls panel has an **External Antenna** switch with **No** and **Yes** (in landscape it is labelled **Antenna**, with **Internal** and **External**).
   - This is required before any pings can be sent (the panel shows "Select antenna option" until you choose)
   - Select **No** (Internal) if the antenna is inside a metal vehicle cabin, a metal box, or another enclosure that reduces reception, e.g. the radio and antenna are inside the car
   - Select **Yes** (External) if nothing like that blocks the antenna, e.g. a roof-mounted antenna, a handheld radio, or walking with the radio in your pocket
   - This does not change your radio or its power. It records how the antenna was set up so the coverage data can be read correctly.
   - The app remembers your choice for each radio

2. **Coverage zone** — The status bar shows your zone status:
   - Green zone code (like "YOW") = you are in a zone and TX is allowed
   - Red zone code = you are in a zone but TX is at capacity (Passive Mode only)
   - Blue zone code = your region has flood traffic turned off (Passive and Trace only)
   - Grey zone code = you are in a zone but not yet connected
   - Orange dash = you are outside any zone
   - Orange "GPS..." = GPS is still searching

If your device model was not recognised, you may also need to pick a power level on the Connect tab (the panel says "Select power level in Connect tab").

!!! note "Flood traffic"
    Send Ping, Active Mode, and Hybrid Mode send flood traffic, so they only appear when your region allows it. Regions that have not been set up yet have flood traffic turned off by default. When flood traffic is off, or the zone is at capacity, those buttons are hidden and only Passive and Trace are available.

Once both are set, tap **Send Ping**:

- The app sends a channel message to #wardriving
- This message **floods the entire mesh network**, with every repeater relaying it onward
- **Your GPS position is not in the on-air message.** By default the message carries a short anonymous token, and your coordinates are sent only to the MeshMapper server over the internet. (You can opt in to broadcasting coordinates on the air via Settings > Wardriving > Broadcast My Coordinates.)
- If your regional admin has configured a **scope**, the message stays within that region instead
- The app listens for **5 seconds** to see which repeaters echoed your message back
- On the backend, MeshMapper uses **MQTT observers** that also listen to the #wardriving channel. If an observer receives your message, the backend marks that ping as **bidirectional (bidir)**
- Results appear as markers on the map and entries in the Log tab
- After a manual ping, Send Ping has a 15-second cooldown

---

## Understanding the Status Bar

The status bar sits below the app bar on the Map tab:

- **Zone chip** (left): Zone code when in coverage, dash when outside, "GPS..." while acquiring. Tap for details.
- **TX**: Channel messages sent (flood the mesh, or scoped if your region has a scope set)
- **RX**: Mesh packets passively received
- **DISC**: Discovery requests that got a response
- **TRC**: Successful trace responses
- **Upload**: Pings successfully uploaded to MeshMapper servers

Tap any stat chip to see a description of what it means.

---

## What Happens to Your Data

Every ping you send (TX), mesh packet you passively receive (RX), discovery response (DISC), and trace result (TRC) is queued for upload to the MeshMapper API. The app batches these uploads (up to 50 at a time) and sends them automatically. In Offline Mode nothing is uploaded until you upload the saved session yourself from Settings > Data. You can see the current queue size in Settings under "Data > Queued Pings."

Your data contributes to the community coverage map at [meshmapper.net](https://meshmapper.net/), helping everyone understand where MeshCore mesh coverage exists.

---

## Next Steps

- [**Wardriving Modes**](app_wardriving_modes.md) — Learn about Hybrid, Passive, Active, and Trace modes
- [**App Tabs**](app_tabs.md) — Detailed walkthrough of each tab
- [**Settings Reference**](app_settings_reference.md) — Every setting explained
- [**Connection Guide**](app_connection_guide.md) — Deep dive into connection, reconnection, and offline mode
- [**Troubleshooting**](app_troubleshooting.md) — Common issues and how to resolve them
