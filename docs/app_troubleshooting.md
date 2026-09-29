# Troubleshooting

Common issues and how to resolve them.

---

## Connection Issues

### "No devices found" when scanning

**Possible causes:**

- Radio is not powered on or out of BLE range (typically 10-30m)
- Bluetooth is disabled on your phone (the Connect tab shows **Bluetooth is Off**)
- Location Services are off (the Connect tab shows **Location Services Disabled**)
- Android: Location permission not granted (required for BLE scanning)
- Another app/device is already connected (MeshCore only supports one BLE connection at a time)

**Solutions:**

- Power cycle your radio and scan again
- Move closer to the radio
- Check Bluetooth and Location are enabled in system settings
- Disconnect other apps connected to the device

If the Connect tab shows **Region Not Available** instead of a device list, you are outside every MeshMapper zone. See [Zone shows orange dash](#zone-shows-orange-dash-outside-coverage-area).

### Connection fails at "Device Info" step

The step reads **Querying device info...** on screen. It retrieves your radio's public key (required for API auth). If this fails, the entire connection fails.

**Causes:** Firmware compatibility issue or transient BLE error

**Solutions:**

- Try connecting again (transient errors often resolve on retry)
- Verify your radio runs MeshCore firmware with companion protocol support
- Power cycle the radio if the problem persists

### Connection fails at "Session Acquisition" step

The step reads **Acquiring API slot...** on screen. It authenticates with the MeshMapper API.

If MeshMapper can't be reached at all, the screen shows **Server Unreachable**: check your internet connection, try again, or use Offline Mode. Otherwise the app shows the server's reason:

| Message | What to do |
|---------|------------|
| "Unknown device. Please advertise yourself on the mesh using the official MeshCore app." | Send an advert from the MeshCore app so MeshMapper learns your radio, then try again |
| "App version outdated. Please update to the latest version." | Update the app |
| "Your phone's clock is out of sync. Turn on automatic date and time in your phone settings." | Turn on automatic date and time |
| "GPS signal is weak (need <50m). Waiting for a stronger signal..." | Wait for a better fix, or move somewhere with a clearer sky view |
| "Device clock error. Power-cycle your device to reset it." (or the server's own wording) | Power-cycle your radio |
| "Zone is at TX capacity. Only Passive mode works here." | Use Passive Mode, or try later |
| "This zone is currently disabled. Try again later." | Try later |
| "Rate limited. Please slow down." | Wait a moment before reconnecting |
| "Service is under maintenance. Try again later." | Use Offline Mode during maintenance |

### Bluetooth disconnects unexpectedly

**Causes:**

- Out of Bluetooth range
- Radio battery died
- Transient BLE error
- iOS: Aggressive background app management

**What happens:**

- Auto-reconnect up to **3 attempts** (3 seconds apart, 30-second overall limit)
- Session, upload queue, and noise floor data are **preserved**
- If auto-reconnect fails → full disconnect cleanup, manual reconnect needed

---

## GPS Issues

### Status bar shows "GPS..." and never resolves

**Causes:**

- Location permission denied
- GPS/Location services disabled
- Indoors with poor reception

**Solutions:**

- Check location permission is granted for MeshMapper
- Enable Location Services system-wide
- Move to a location with clear sky view
- If the permission was permanently denied, a snackbar appears ("Location permission is disabled in system settings.") with a **Settings** button

### Zone shows orange dash (outside coverage area)

- You are outside any registered MeshMapper zone
- Tap the GPS chip to see the nearest zone's name and distance
- The Connect tab shows **Region Not Available**, with a **Request Region Onboarding** button
- Travel to a registered zone, or use Offline Mode to wardrive in unregistered areas

### "Phone Clock Out of Sync" or "Weak GPS Signal"

A zone check can fail in two related ways:

- **Phone Clock Out of Sync**: your location looks out of date because your phone's clock is wrong. This is a time problem, not a GPS problem. Turn on automatic date and time (and time zone), then tap **Retry Zone Check**.
- **Weak GPS Signal**: zone checks need accuracy better than 50m. Move to improve accuracy, then tap **Retry Zone Check**.

Pings themselves need accuracy of 100m or better, plus the minimum distance since your last ping.

**Solutions:**

- Make sure GPS is actively tracking
- iOS: Turn on Background Location in Settings > General for continuous tracking

---

## Ping Issues

### "Send Ping" button is disabled

A hint under the buttons explains most blocks. Check these requirements:

- **External antenna not set** ("Select antenna option") — Choose Yes or No in the Controls panel
- **Power level not set** ("Select power level in Connect tab") — Device model was not recognized. Pick your power level in the Connect tab.
- **Not connected** — Need an active connection to your radio
- **No GPS lock** ("Waiting for GPS") — App needs a valid GPS position
- **GPS accuracy too low** ("GPS signal is weak") — Accuracy is worse than 100m. Move to a location with better reception.
- **Airborne** ("Airborne, wardriving blocked") — Wardriving from an aircraft is blocked
- **Passive only (Offline Mode)** — TX pings are not available in Offline Mode. Only discovery and passive RX work offline.
- **Passive only (zone full)** — All TX slots in your zone are taken, or the region allows no TX. You can still use Passive Mode.
- **Controls locked** — A ping is in progress (its 5-second listening window). The buttons do not wait for the upload.
- **Cooldown active** — Brief cooldown after a manual ping (15s) or after stopping Active/Hybrid Mode (5s)

### "No repeaters heard" on every ping

**Causes:**

- No MeshCore repeaters in range
- Antenna not connected or poorly oriented
- Signal blocked by terrain or buildings
- Repeaters on a different channel

**Solutions:**

- Try Passive/Discovery Mode to query repeaters directly
- Check antenna connection
- Move to a location with known repeater coverage

### Pings are being skipped in auto-ping mode

This is **normal behavior**:

- Pings are **Skipped** when you haven't moved the minimum distance (default 25m)
- Pings are **Deferred** by Smart Pinging when your square already has recent coverage. See [Smart Pinging](app_wardriving_modes.md#smart-pinging).
- If "Auto-Stop After Idle" is enabled, auto-ping stops entirely after 30 minutes without movement

---

## Data Upload Issues

If your phone has internet but the app says **Server Unreachable**, the app could not reach MeshMapper's services. Try again after checking [system status](systemstatus.md), or use offline mode and upload the saved session later. A working browser connection alone does not prove the MeshMapper service is reachable.

If pings are missing from the map, check that the upload queue has cleared, the correct region map and time filters are selected, and your session was inside an active region. The map and leaderboards update on different schedules. See the upload checks below before repeating a drive.

### Queue keeps growing but nothing uploads

**Causes:**

- Poor or no internet connection
- API in maintenance mode

**Solutions:**

- Check internet connection
- Tap the **Force upload** button (cloud icon) in Settings > Data > Queued Pings
- Switch to Offline Mode during maintenance

An expired session refreshes itself, so you don't need to reconnect for that.

### Data uploaded but not appearing on meshmapper.net

- Server-side processing may take a few minutes
- Check the [MeshMapper Discord](https://discord.gg/tyXbecdxgr) for status updates if data still doesn't appear

---

## Audio Issues

### No sound on ping events

**Causes:**

- Sound notifications disabled in Settings
- The individual sound (Ping Sent, Response Received, Disconnect Alert) is switched off
- Phone media volume turned down
- Another app has exclusive audio focus

**Solutions:**

- Enable in Settings > General > Sound Notifications, and check the three sounds under it
- Check phone media volume

### Audio hangs or freezes

- App has a 3-second timeout protection
- On a timeout, the app automatically resets the audio session and reloads the sounds
- If it persists, toggle Sound Notifications off and on in Settings

---

## Debug Logging

To capture detailed logs for a bug report:

1. Go to **Settings > About & Support > Debug Logs**
2. Enable **Debug Logs** (orange "LOGGING" badge confirms)
3. Reproduce the issue
4. Use **Submit Feedback** (Settings > About & Support) or the **Upload** button in the Debug Logs section

Logs include timestamped entries for BLE communication, GPS events, ping lifecycle, API calls, and more.

---

## Reporting Bugs

1. Go to **Settings > About & Support > Submit Feedback**
2. Choose **Bug** (or **Feature**), add a short title, and describe the issue (what you expected vs what happened)
3. Optionally switch on **Include with feedback** and select which log files to include
4. Submit — a confirmation toast appears with a "View" link to track your report

Also report issues on:

- [**GitHub**](https://github.com/MeshMapper/MeshMapper_Project)
- [**Discord**](https://discord.gg/tyXbecdxgr)
