# Troubleshooting

Common issues and how to resolve them.

---

## Connection Issues

### "No devices found" when scanning

**Possible causes:**

- Radio is not powered on or out of BLE range (typically 10-30m)
- Bluetooth is disabled on your phone
- Android: Location permission not granted (required for BLE scanning)
- Another app/device is already connected (MeshCore only supports one BLE connection at a time)

**Solutions:**

- Power cycle your radio and scan again
- Move closer to the radio
- Check Bluetooth and Location are enabled in system settings
- Disconnect other apps connected to the device

### Connection fails at "Device Info" step

Retrieves your radio's public key (required for API auth). If this fails, the entire connection fails.

**Causes:** Firmware compatibility issue or transient BLE error

**Solutions:**

- Try connecting again (transient errors often resolve on retry)
- Verify your radio runs MeshCore firmware with companion protocol support
- Power cycle the radio if the problem persists

### Connection fails at "Session Acquisition" step

Authenticates with the MeshMapper API.

**Causes:**

- No internet connection
- MeshMapper API in maintenance mode

**Solutions:**

- Check internet connection
- Use Offline Mode during maintenance

### Bluetooth disconnects unexpectedly

**Causes:**

- Out of Bluetooth range
- Radio battery died
- Transient BLE error
- iOS: Aggressive background app management

**What happens:**

- Auto-reconnect up to **3 attempts** (3-second delay between each, 30-second overall timeout)
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
- Android: If permanently denied, a snackbar appears with "Settings" button

### Zone shows orange dash (outside coverage area)

- You are outside any registered MeshMapper zone
- Tap the zone chip to see nearest zone name and distance
- Travel to a registered zone, or use Offline Mode to wardrive in unregistered areas

### "GPS data is stale" warnings

- Zone status queries need GPS < 60 seconds old and < 50m accuracy
- Regular pings only check the 25m movement requirement

**Solutions:**

- Make sure GPS is actively tracking (not cached)
- Move to improve accuracy
- iOS: Enable Background Mode in Settings for continuous tracking

---

## Ping Issues

### "Send Ping" button is disabled

Check these requirements:

- **External antenna not set** — Choose Yes or No in Controls panel
- **Power level not set** — Device model was not recognized. Go to Settings to manually select your TX power level.
- **Not connected** — Need active Bluetooth connection
- **No GPS lock** — App needs valid GPS position
- **GPS accuracy too low** — GPS accuracy is too poor (> 100m). Move to a location with better reception.
- **Not in a zone** — Must be in a coverage zone (or use Offline Mode)
- **TX Disabled (Offline Mode)** — TX pings are not available in Offline Mode. Only discovery and passive RX work offline.
- **Zone Full** — All TX slots in your zone are taken. You can still use Passive Mode.
- **Controls locked** — Ping in progress (5s listening window or API upload)
- **Cooldown active** — Brief cooldown after a manual ping (15s) or after stopping Active/Hybrid Mode

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

- Pings skip when you haven't moved the minimum distance (default 25m)
- If "Auto-Stop After Idle" is enabled, auto-ping stops entirely after 30 minutes without movement

---

## Data Upload Issues

### Queue keeps growing but nothing uploads

**Causes:**

- Poor or no internet connection
- API in maintenance mode
- API authentication expired

**Solutions:**

- Check internet connection
- Try "Force Upload" in Settings > Data > Queued Pings
- Switch to Offline Mode during maintenance
- Disconnect and reconnect to refresh API session

### Data uploaded but not appearing on meshmapper.net

- Server-side processing may take a few minutes
- Check the [MeshMapper Discord](https://discord.gg/tyXbecdxgr) for status updates if data still doesn't appear

---

## Audio Issues

### No sound on ping events

**Causes:**

- Sound notifications disabled in Settings
- Phone on silent/vibrate mode
- Another app has exclusive audio focus

**Solutions:**

- Enable in Settings > General > Sound Notifications
- Check phone volume and ringer mode

### Audio hangs or freezes

- App has a 3-second timeout protection
- On corruption, the app automatically resets and reloads audio assets
- If persists, toggle Sound Notifications off and on in Settings

---

## Web-Specific Issues

### "Web Bluetooth not supported" error

- Web Bluetooth only works in **Chrome** and **Edge**
- Safari, Firefox, and other browsers are not supported

### CORS errors during local development

- Add the web security flag: `flutter run -d chrome --web-browser-flag="--disable-web-security"`

### Web Bluetooth requires active tab

- Unlike mobile, Web Bluetooth only works in the **foreground tab**
- Switching tabs or minimizing = Bluetooth connection lost
- No background mode for the web version

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
2. Describe the issue (what you expected vs what happened)
3. Optionally enable "Upload debug logs" and select which log files to include
4. Submit — a confirmation toast appears with a "View" link to track your report

Also report issues on:

- [**GitHub**](https://github.com/MeshMapper/MeshMapper_Project)
- [**Discord**](https://discord.gg/tyXbecdxgr)
