# Connection Guide

This guide covers everything about connecting to your MeshCore radio, what happens during the connection process, how reconnection works, and how to use Offline Mode.

---

## Scanning for Devices

1. Open the **Connect** tab (Bluetooth icon in the bottom bar)
2. Tap **"Scan for Devices"** to start a BLE scan
3. Nearby MeshCore devices appear in a list showing their name and signal strength
4. Tap your device to begin connecting

**Platform notes:**

- **Android**: May need to grant Bluetooth and Location permissions
- **iOS**: System will prompt for Bluetooth access
- **Web**: Chrome shows its native Bluetooth pairing dialog

---

## Remembered Devices

After your first successful connection, MeshMapper remembers that device. On future launches:

- Your last device appears at the top of the Connect tab under "Last Connected Device"
- Tap it to reconnect without scanning
- To connect to a different device, just run a new scan

---

## The 9-Step Connection Process

When you tap a device, MeshMapper runs through nine steps automatically. You can watch progress on the Connect tab:

| Step | What Happens |
|------|-------------|
| 1 BLE GATT Connect | Establishes the raw Bluetooth connection |
| 2 Protocol Handshake | Verifies app and firmware compatibility |
| 3 Device Info | Retrieves manufacturer string and public key (required for API auth). If this fails, the entire connection fails. |
| 4 Device Identification | Determines your device model and TX power level for reporting. Does NOT change your radio's actual power settings. |
| 5 Time Sync | Synchronizes your radio's clock with your phone |
| 6 Session Acquisition | If Anonymous Mode is enabled, your device is first renamed to "Anonymous" on the mesh. Then authenticates with the MeshMapper API. Handles registration automatically if needed. Returns zone info, permissions, and regional settings. |
| 7 Channel Setup | Creates the #wardriving channel on your radio (or reuses existing) |
| 8 GPS Init | Waits for a GPS lock on your phone |
| 9 Connected | Unified RX Handler starts, noise floor polling begins (every 5s), ready to wardrive |

**After connection completes**, the app applies regional settings from the API response:

- **Regional channels**: Additional channels from the zone config are created on your radio
- **Flood scope**: If the regional admin has set a scope, it is applied to your radio so TX messages stay within that region
- **Regional enforcement**: Hybrid Mode, discovery drop, and minimum ping interval may be enforced by the regional admin
- **Path hash mode**: If the zone enforces a specific hop byte size (1/2/3-byte) and your radio differs, the app automatically reconfigures your radio to match. Restored on clean disconnect. Two dialogs may appear:
  - **"Multi-Byte Paths Enabled"** (info): Your radio was reconfigured to match the zone's requirement. Shows the new byte size and whether it was set by the regional admin or your own preference.
  - **"Firmware Update Recommended"** (warning): Your companion firmware does not support multi-byte paths. The app falls back to 1-byte mode and suggests updating to firmware v1.14.0+.

---

## Zone Authentication

MeshMapper uses a zone-based authentication system. The server checks your GPS coordinates and tells you which zone you are in (if any). Each zone has a code (like "YOW" for Ottawa) and a set of rules configured by the regional admin:

**Session permissions:**

- **TX Allowed**: Whether you can send channel messages. If at TX capacity, you are limited to Passive Mode only.
- **RX Allowed**: Whether passive reception is permitted
- **TX Slots Available**: How many active wardrivers the zone can support simultaneously
- **Session Expiry**: When your session expires (automatically refreshed via heartbeat)

**Regional configuration:**

- **Scope**: Flood scope for the zone. When set, your TX channel messages are scoped to that region instead of flooding the entire global mesh. Shown on the Connect tab (e.g., "#ottawa"). If no scope is set, it shows "Global." Applied automatically by setting a transport key on your radio.
- **Channels**: Additional channels configured by the regional admin (e.g., regional monitoring channels)
- **Enforce Hybrid**: Whether Hybrid Mode is mandatory for the zone. When enforced, the Hybrid Mode toggle in Settings is locked.
- **Minimum TX Ping Interval**: The minimum auto-ping interval (15, 30, or 60 seconds). If set, you cannot choose a faster interval than the regional minimum.
- **Mark Failed Discovery as Drop**: When enabled, discovery requests with no response are counted as "no coverage" data and shown as DROP on the coverage map.
- **Hop Bytes**: Enforces a specific path hash size (1-byte, 2-byte, or 3-byte) for consistent data across all wardrivers in the zone. During connection, the app checks your radio's current path hash mode against the region's requirement. If they differ (e.g., your radio is set to 1-byte but the region requires 2-byte), the app automatically reconfigures your radio to match. On clean disconnect, the app restores your radio to its original setting. If your firmware does not support multi-byte paths (pre-1.14), the app will warn you that it cannot apply the regional setting.

If you are outside all zones, the status bar shows an orange dash with the name and distance to the nearest zone.

---

## Automatic Reconnection

If your Bluetooth connection drops unexpectedly (out of range, radio restart, etc.), MeshMapper will attempt to reconnect automatically.

**What you see:**

- "Reconnecting..." overlay on the map
- Current attempt number (up to 3 attempts)
- Device name
- Cancel button to stop trying

**What is preserved:**

- API session
- Upload queue
- Noise floor session
- Auto-ping restarts automatically after successful reconnect

**If all 3 attempts fail:** The app falls back to a full disconnect cleanup.

---

## Disconnecting

Tap the **Disconnect** button on the Connect tab. The app performs a clean shutdown:

1. Stops auto-ping mode if running
2. Ends the current noise floor session
3. Stops the background service
4. Flushes any buffered RX observations
5. Clears the API upload queue (pings won't have a valid session after disconnect)
6. Releases your session with the MeshMapper API
7. Deletes the #wardriving channel from your radio (if "Delete Channel on Disconnect" is enabled in Settings)
8. Restores your device's original name if Anonymous Mode renamed it during connection
9. Restores your radio's original path hash mode if it was changed during connection (e.g., region required 2-byte but your radio was set to 1-byte)
10. Closes the Bluetooth connection
11. Resets all state

!!! warning
    Steps 7, 8, and 9 (channel deletion, name restoration, and path hash restoration) all happen while BLE is still connected because these commands need the BLE link to reach the radio.

---

## Offline Mode

If you don't have internet, or the MeshMapper API is in maintenance mode, use **Offline Mode** to continue wardriving. Data is saved locally and can be uploaded later.

**To enable:**

- Tap the **"Go Offline"** button on the Connect tab

**In Offline Mode:**

- Zone validation is skipped (zone chip shows a grey dash)
- All ping data (TX, RX, DISC) is saved to local session files
- Session files are named by date (e.g., "2026-03-20.json")
- Manage sessions in **Settings > Offline Sessions**

**When you are back online:**

1. Open **Settings > Offline Sessions**
2. Tap upload button next to each session to send to MeshMapper
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
    You must **disconnect cleanly** for your device name to be restored. If the app crashes or BLE drops unexpectedly, your radio may still advertise as "Anonymous" until you connect and disconnect again cleanly.

---

## Session Heartbeat

During long wardriving sessions, MeshMapper automatically sends heartbeat requests to keep your session alive:

- Fires about 1 minute before session expiry
- Server responds with a new expiration time
- Happens transparently in the background

---

## Background Operation

When you start auto-ping, MeshMapper enables background operation to keep Bluetooth and GPS alive:

- **Android**: Persistent foreground notification showing the current mode and live stats. No sound or vibration.
  - Active / Hybrid: `TX: N | RX: M | Queue: P`
  - Passive: `RX: M | Queue: P`
  - Trace: `Trace: N | RX: M | Queue: P`
- **iOS**: Uses declared background modes (bluetooth-central, location). For best results, enable "Background Location" in Settings to upgrade to "Always" location permission, which prevents iOS from throttling during extended sessions.
- **Web**: Not available. Browser tab must remain active for Web Bluetooth.

The background service starts automatically with auto-ping and stops when you stop auto-ping or disconnect.
