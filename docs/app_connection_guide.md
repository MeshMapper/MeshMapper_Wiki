# Connection Guide

This guide covers everything about connecting to your MeshCore radio, what happens during the connection process, how reconnection works, and how to use Offline Mode.

---

## Connection Methods

The Connect tab has a selector for **how** to connect to your radio:

| Method | Platforms | Notes |
|--------|-----------|-------|
| **BLE** (Bluetooth) | Android, iOS | The standard method. Scan and tap your device. |
| **TCP** | Android, iOS | Connect to a network-attached radio by host and port (default 5000), e.g. a WiFi-connected companion or a serial-to-TCP bridge. Saved connections are remembered. |
| **USB** (serial) | Android (USB OTG) | Direct cable connection. Not available on iOS. |

Everything below the transport (the connection workflow, sessions, zones) works the same regardless of which method you use. Automatic reconnection is the exception: it covers BLE and TCP only.

---

## Before You Connect

Before it lets you connect, the app checks your location with MeshMapper. The zone status at the top of the Connect tab shows the result:

- **Zone name**: you are inside a region and can connect
- **Checking Zone...**: the check is still running
- **Outside Zone**: you are not inside any region. The Connect tab shows **Region Not Available** with the nearest zone and its distance, and a **Request Region Onboarding** button.
- **Maintenance**: MeshMapper is down for maintenance. You can still wardrive with **Enable Offline Mode**.
- **No Internet**, **Clock Out of Sync** or **GPS Unavailable**: the check could not finish. See [Zone Authentication](#zone-authentication).
- **Airborne**: you appear to be in an aircraft. Wardriving from an aircraft is not allowed, and you can connect again once you are back on the ground.

[Offline Mode](#offline-mode) skips the zone and maintenance checks, but never the airborne block.

---

## Scanning for Devices

1. Open the **Connect** tab (Bluetooth icon in the bottom bar)
2. Tap **Scan** to start a BLE scan. Before any results, the list reads "Tap Scan to search for MeshCore devices".
3. Nearby MeshCore devices appear in a list showing their name and signal strength
4. Tap your device to begin connecting

**Platform notes:**

- **Android**: May need to grant Bluetooth and Location permissions
- **iOS**: System will prompt for Bluetooth access

---

## Remembered Devices

After your first successful connection, MeshMapper remembers that device. For a BLE device, on future launches:

- Instead of an empty list, the Connect tab shows **Last Connected Device** with your device's name
- Tap **Reconnect** to connect without scanning. If you can't connect yet, the button reads **Outside Zone**, **Checking Zone...** or **Maintenance** instead.
- Tap **Scan** to look for a different device, or **Forget** to clear the remembered one

TCP connections are listed under **Saved Connections** on the TCP tab.

---

## The 9-Step Connection Process

When you tap a device, MeshMapper runs through nine steps automatically. You can watch progress on the Connect tab:

| Step | What Happens |
|------|-------------|
| 1 Transport Connect | Establishes the raw connection (BLE, TCP socket, or USB serial port) |
| 2 Protocol Handshake | A short pause while the radio gets ready |
| 3 Device Info | Sends the app's protocol version and reads the firmware, manufacturer string and public key (required for API auth). If this fails, the entire connection fails. |
| 4 Device Identification | Determines your device model and power level for reporting. Does NOT change your radio's actual power settings. |
| 5 Time Sync | Synchronizes your radio's clock with your phone |
| 6 Session Acquisition | If Anonymous Mode is enabled, your device is first renamed to "Anonymous" on the mesh. Then authenticates with the MeshMapper API. Handles registration automatically if needed. Returns zone info, permissions, and regional settings. |
| 7 Channel Setup | Creates the #wardriving channel on your radio (or reuses existing) |
| 8 GPS Init | A progress marker only. It does not wait for a GPS lock. |
| 9 Connected | Ready to wardrive. Noise floor is read every 5 seconds and battery every 30 seconds. |

**After connection completes**, the app applies regional settings from the API response:

- **Regional channels**: The app also listens to any extra channels the regional admin has set up
- **Flood scope**: If the regional admin has set a scope, it is applied to your radio so TX messages stay within that region
- **Flood traffic**: If the region allows flood traffic, the app turns **Flood Traffic** on. If the region has disabled it, Active, Hybrid and Send Ping are unavailable, and the Connect tab explains why.
- **Regional enforcement**: The regional admin may enforce Hybrid Mode, Discovery Drop, Smart Pinging (and its window), Scope Discovery (and its window), and a minimum auto-ping interval. Enforced settings are locked in Settings.
- **Regional CARpeaters**: The region's shared CARpeater list is loaded and filtered
- **Path hash mode**: If the zone enforces a specific hop byte size (1/2/3-byte) and your radio differs, the app automatically reconfigures your radio to match. Restored on clean disconnect. Two dialogs may appear:
  - **"Multi-Byte Paths Enabled"** (info): Your radio was reconfigured to match the zone's requirement. Shows the new byte size and whether it was set by the regional admin or your own preference.
  - **"Firmware Update Recommended"** (warning): Your companion firmware does not support multi-byte paths. The app falls back to 1-byte mode and suggests updating to firmware v1.14.0+.
- **Account link**: If you are signed in to [My MeshMapper](portal.md) and this radio is not linked yet, the app offers to link it

While connected, the app re-checks your zone every 60 seconds to keep slot counts fresh.

!!! note "Antenna choice resets"
    Your antenna choice (Internal or External) is cleared every time you disconnect. Select it again after each connect before you start pinging.

---

## Zone Authentication

If the zone check fails, wait for an accurate, current GPS fix and confirm that your location is inside an active MeshMapper region. The app reports a wrong phone clock (**Phone Clock Out of Sync**), weak GPS (**Weak GPS Signal**), no internet (**No Internet Connection**) and other errors (**Zone Check Failed**) separately. It retries on its own, or offers a **Retry Zone Check** button for GPS and clock problems. If your area has no region, use [onboarding](onboarding.md) rather than choosing an unrelated region code.

MeshMapper uses a zone-based authentication system. The server checks your GPS coordinates and tells you which zone you are in (if any). Each zone has a code (like "YOW" for Ottawa) and a set of rules configured by the regional admin:

**Session permissions:**

- **TX Allowed**: Whether you can send channel messages. If the zone is at TX capacity, you are limited to Passive and Trace modes.
- **RX**: Passive reception is always allowed
- **TX Slots Available**: How many active wardrivers the zone can support simultaneously
- **Session Expiry**: When your session expires (automatically refreshed via heartbeat)

**Regional configuration:**

- **Scope**: Flood scope for the zone. When set, your TX channel messages are scoped to that region instead of flooding the entire global mesh. Shown on the Connect tab (e.g., "#ottawa"). If no scope is set, it shows "Global." Applied automatically by setting a transport key on your radio.
- **Channels**: Additional channels configured by the regional admin (e.g., regional monitoring channels)

Most other rules are set **per radio preset** (frequency, bandwidth and spreading factor), so one region can have different rules for different presets:

- **Slots**: How many wardrivers can transmit at once (default 0)
- **Disable Flood**: Turns flood traffic off for the preset (default On, so flood is off until the admin allows it)
- **Enforce Hybrid**: Makes Hybrid Mode mandatory. When enforced, the Hybrid Mode switch in Settings is locked on. Default Off.
- **Min Interval**: The minimum auto-ping interval (15, 30, or 60 seconds, default 60). You cannot choose a faster interval than the regional minimum.
- **Failed DISC as DROP**: When enabled, discovery requests with no response are counted as "no coverage" data and shown as DROP on the coverage map.
- **App Path Bytes**: Enforces a specific path hash size (device default of 1 byte, 2 bytes, or 3 bytes) for consistent data across all wardrivers in the zone. If your radio differs, the app reconfigures it at connect and restores the original setting on clean disconnect. If your firmware does not support multi-byte paths (pre-1.14), the app warns you that it cannot apply the regional setting.
- **Enforce Smart Pinging**: Locks [Smart Pinging](app_wardriving_modes.md#smart-pinging) on, with the region's window (1, 3, 7, 14 or 30 days)
- **Scope discovery**: Locks [Scope Discovery](app_settings_reference.md#scope-discovery) on, with the region's re-check window (7 days or more)

If you are outside all zones, the zone chip in the status bar shows an orange "—". Tap it to see the name and distance of the nearest zone.

**Leaving your zone while wardriving.** If you drive out of your zone, the app pauses wardriving and shows **Out of Zone** with the nearest zone. You get 5 minutes to come back. If you return, wardriving resumes. If not, the app disconnects. Driving straight into a neighbouring zone shows **Changing Zone...** while your session moves to the new zone.

---

## Automatic Reconnection

If your BLE or TCP connection drops unexpectedly (out of range, radio restart, etc.), MeshMapper will attempt to reconnect automatically. USB connections do not reconnect on their own.

**What you see:**

- "Reconnecting..." overlay on the map
- Current attempt number (up to 3 attempts, 3 seconds apart, or 5 seconds after an iOS pairing error)
- Device name
- Cancel button to stop trying

**What is preserved:**

- API session
- Upload queue
- Noise floor session
- Auto-ping restarts automatically after successful reconnect

**If all 3 attempts fail, or 30 seconds pass:** The app falls back to a full disconnect cleanup.

---

## Idle Disconnect

If you stay connected without sending a manual ping or starting an auto mode for **15 minutes**, the app disconnects and logs "Disconnected: 15 minutes of inactivity".

---

## Disconnecting

Tap the **Disconnect** button on the Connect tab. The app performs a clean shutdown:

1. Stops auto-ping mode if running
2. Ends the current noise floor session
3. Stops the background service
4. Flushes any buffered RX observations
5. Saves your Offline Mode session, if you are offline
6. Clears the API upload queue (pings won't have a valid session after disconnect)
7. Releases your session with the MeshMapper API
8. Restores your device's original name if Anonymous Mode renamed it during connection
9. Restores your radio's original path hash mode if it was changed during connection (e.g., region required 2-byte but your radio was set to 1-byte)
10. Clears the flood scope from your radio
11. Deletes the #wardriving channel from your radio (if "Delete Channel on Disconnect" is enabled in Settings)
12. Closes the connection (BLE, TCP or USB)
13. Resets all state

!!! warning
    Steps 8 to 11 (name restoration, path hash restoration, scope clearing and channel deletion) happen while the radio is still connected, because these commands need the link to reach the radio.

---

## Offline Mode

If you don't have internet, or the MeshMapper API is in maintenance mode, use **Offline Mode** to continue wardriving. Data is saved locally and can be uploaded later.

**To enable:**

- Tap the **Go Offline** button on the Connect tab and confirm. This works before or while connected.
- Or tap **Enable Offline Mode** on the Connect tab when it shows no internet or maintenance

**In Offline Mode:**

- Zone validation is skipped (zone chip shows a grey dash)
- Send Ping, Active and Hybrid are unavailable (they need an online session). Passive and Trace modes work.
- Ping data is saved to local session files, and the app saves your progress every 60 seconds
- Session files are named by date (e.g., "2026-03-20.json")
- Manage sessions in **Settings > Data > Offline Sessions**

**When you are back online:**

1. Open **Settings > Data > Offline Sessions**
2. Tap the upload button next to each session to send it to MeshMapper. Uploading needs your phone's location, but not the radio.
3. Or download session files for backup

!!! warning
    Offline Mode is never persistent. It resets to "off" every time you restart the app.

---

## Anonymous Mode

Prefer not to broadcast your device's real name? Enable **Anonymous Mode** in Settings.

- Your companion device is renamed to "Anonymous" on the mesh network
- Changing this while connected triggers a brief reconnection
- Cannot be toggled while auto-ping is running (stop auto-ping first)

!!! warning
    You must **disconnect cleanly** for your device name to be restored. If the app crashes or the connection drops unexpectedly, your radio may still advertise as "Anonymous" until you connect and disconnect again cleanly.

---

## Session Heartbeat

During long wardriving sessions, MeshMapper automatically sends heartbeat requests to keep your session alive:

- Turned on when you connect online
- Fires about 1 minute before session expiry
- Server responds with a new expiration time
- Happens transparently in the background

---

## Background Operation

When you start auto-ping, MeshMapper enables background operation to keep the radio connection and GPS alive:

- **Android**: Persistent foreground notification titled "MeshMapper - *Mode* Mode" (for example "MeshMapper - Hybrid Mode") with live stats. No sound or vibration.
  - Active / Hybrid: `TX: N | RX: M | Queue: P`
  - Passive: `RX: M | Queue: P`
  - Trace: `Trace: N | RX: M | Queue: P`
- **iOS**: Uses declared background modes (bluetooth-central, location). For best results, enable "Background Location" in Settings to upgrade to "Always" location permission, which prevents iOS from throttling during extended sessions.

!!! warning "Android screen-off wardriving"
    Some Android phones may pause wardriving when the screen is off. If this happens, open **Android Settings > Apps > MeshMapper > App battery usage** and select **Unrestricted**. This may increase battery use.

The background service starts automatically with auto-ping and stops when you stop auto-ping or disconnect.
