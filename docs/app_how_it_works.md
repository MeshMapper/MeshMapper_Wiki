# How MeshMapper Works

This guide explains the technology behind MeshMapper for users who want to understand what is happening under the hood. You do not need to know any of this to use the app, but it can help you make better wardriving decisions and understand your data.

---

## What is Wardriving?

Wardriving is the practice of surveying wireless network coverage by moving through an area with a receiver. MeshMapper applies this to MeshCore mesh radio networks. As you move with a connected MeshCore device, the app records:

- Where repeaters can be heard
- How strong the signal is
- What the radio environment looks like

This data is aggregated with contributions from other wardrivers on the [MeshMapper community map](https://meshmapper.net/).

---

## How Bluetooth Communication Works

MeshMapper communicates with your radio over **Bluetooth Low Energy (BLE)** using the UART (serial) service:

- **TX Characteristic**: Write commands to the device
- **RX Characteristic**: Receive notifications (responses and events) from the device

All communication follows the **MeshCore Companion Protocol**, a binary protocol where the app sends commands and the radio responds with data or event notifications.

**Platform libraries:**

- Android / iOS: `flutter_blue_plus`
- Web: `flutter_web_bluetooth`

---

## How TX Channel Messages Work

When you send a TX ping (manually or via auto-ping), you are sending a **channel message** that floods the mesh:

1. **Message composition**: By default, a short **anonymous token** (a keyed "wire tag" unique to your session and ping). Your GPS coordinates and power level travel to MeshMapper only via the API — they are not in the on-air message. If **Broadcast My Coordinates** is enabled in Settings, your GPS coordinates are appended to the message as well.
2. **Encryption**: AES-ECB with the #wardriving channel key (SHA-256 hash of "#wardriving"). ECB mode is mandated by the MeshCore protocol. Note that anyone with the community channel key can decrypt the message — which is why it carries a token rather than your location by default.
3. **Broadcast and flooding**: The encrypted message is sent via BLE as a GROUP_TEXT packet. It **floods the entire mesh** by default (every repeater relays it). If a **flood scope** is configured by the regional admin, only repeaters within the scope relay it.
4. **Echo listening (5-second window)**: After sending, the app opens a 5-second listening window. Every incoming packet is checked against these criteria, proceeding to step 5 if all of the following conditions are met:
   - Packet is of the GROUP_TEXT type
   - RSSI is NOT stronger (closer to zero) than -30 dBm (likely a vehicle-mounted "carpeater" if so). This can be overridden by the user in the MeshMapper app settings.
   - Channel hash matches that of #wardriving
   - Decrypted content matches that of the ping just sent
   - Path length is > 0 (the packet has traveled through at least one repeater)
5. **Deduplication**: If the same packet is heard from the same repeater more than once, only the one with the best SNR value is kept.
6. **Queuing**: After the 5-second window closes, the TX ping and its echo results are added to the **upload queue**. A 5-second flush timer starts. When the timer expires, the queue uploads.

### TX vs RX Queuing

TX pings are queued differently from RX observations:

- **TX/DISC/Trace** go directly into the upload queue as a single item (the ping + its results from the listening window). A **5-second flush timer** triggers an upload shortly after.
- **RX observations** go through a **two-stage pipeline**: first the RX Logger batches by repeater (best SNR, 25 meter/30 second flush), then the API queue buffers up to **4 RX entries per repeater** before flushing to the main queue.

---

## How RX Observations Work

While connected, the **Unified RX Handler** continuously monitors all incoming BLE packets from your radio, regardless of mode.

- Any mesh traffic the radio overhears is processed, validated, and queued for upload
- RX observations are "free data" requiring no transmission from you
- They capture other devices' mesh traffic, adding extra coverage data from your location

### RX Batching (Aggregation)

RX packets aren't uploaded individually. Instead, they are **grouped by repeater ID** and aggregated before upload. This reduces API traffic and ensures the best observation is reported for each repeater at each location.

**How it works:**

1. A packet arrives from a repeater at your current GPS location
2. The app creates a **batch** for that repeater, recording your GPS position and the packet's SNR/RSSI
3. More packets arrive from the same repeater. If a new packet has a **better SNR**, it replaces the previous one in the batch. Worse SNR packets are discarded, leaving only the **best SNR observation** to be sent to the API.
4. The batch keeps the **original GPS location** where you first heard that repeater (the map pin doesn't follow you as you move)

**The batch flushes (uploads) when either condition below is met:**

- You move **25 meters** from where you first heard the repeater, OR
- **30 seconds** pass since the first observation

After flushing, if you hear the same repeater again, a new batch starts at your new location.

**On disconnect or stopping auto-ping**, all active batches are flushed immediately, so no data is lost.

---

## How Discovery Pings Work

Discovery pings use a fundamentally different mechanism than TX channel messages. Instead of flooding the mesh, discovery sends a **direct control data request** (zero-hop) to nearby repeaters. Note: Only repeaters and room servers with firmware 1.10.0 or newer support and will respond to discovery pings.

1. **Request**: ControlData command (0x37) with DISCOVER_REQ flag, requesting responses from repeaters and rooms in direct range. Includes a random 4-byte tag for matching.
2. **Response**: Repeaters respond with node type, public key, and their assessment of signal quality from their end (remote SNR).
3. **Tracking**: Discovery Tracker collects responses during a 7-second window, deduplicates by public key, and filters carpeaters. Gives you **bidirectional** signal quality (how you hear them & how they hear you).
4. **Upload**: "DISC" type data with repeater public key, node type, and bidirectional signal quality.

---

## How Trace Pings Work

Trace pings target a specific repeater by hex ID:

1. **Command**: CMD_SEND_TRACE_PATH (0x24) as a zero-hop trace
2. **Response**: If in range, repeater responds with PUSH_CODE_TRACE_DATA (0x89) containing signal quality
3. **Logging**: Successful traces → uploaded to API. Failed traces (no response within 5s) → logged locally, shown as grey markers on noise floor graph.

---

## Packet Filtering and Validation

Every packet goes through a strict validation pipeline before being accepted. If a packet fails any step, it is dropped immediately.

### 1 Path length check

- Packet must have traveled through **at least one repeater** (path length > 0)
- Direct transmissions from nearby devices are not repeater coverage data

### 2 Vehicle-mounted "CARpeater" ID check (optional)

- If you have configured a CARpeater filter with a repeater hex ID in the MeshMapper app settings:
  - **Single hop** from your CARpeater → **dropped** (this is just your own repeater relaying back to you, no real coverage info)
  - **Multiple hops** with CARpeater as last hop → CARpeater hop is **stripped**, second-to-last hop used as the real repeater (the packet traveled through a distant repeater first, then your CARpeater delivered it to you. The distant repeater is the real coverage data, your CARpeater just happened to be the final relay. SNR/RSSI are set to null since they reflect your CARpeater's signal, not the distant repeater's.)

### 3 RSSI check (CARpeater failsafe)

- Signal must be **weaker (farther from zero) than -30 dBm**
- Anything stronger implies the relaying node is right next to you (likely a carpeater)
- Acts as a safety net even without the CARpeater ID filter
- Skipped if the Disable RSSI Filter option is ENABLED in app Settings or if CARpeater hop was already stripped

### 4 Packet type check

- Only two types accepted:
  - **GROUP_TEXT** (0x15) — Channel messages
  - **ADVERT** (0x11) — Node advertisements

### 5 Channel hash check (GROUP_TEXT only)

- Channel hash must match a **subscribed channel** (#wardriving or regional channels)
- Prevents random mesh traffic from being counted as coverage data

### 6 Decryption (GROUP_TEXT only)

- Payload decrypted with the matching channel's AES-ECB key
- Dropped if decrypted data is too short (< 5 bytes)

### 7 Printable character check (GROUP_TEXT only)

- At least **60%** of decrypted message must be printable ASCII (codes 32-126)
- Filters corrupted packets that coincidentally have a valid channel hash
- 60% threshold allows for emojis and Unicode in legitimate messages

### 8 ADVERT name validation (ADVERT only)

- Node name must be present, non-empty, and pass the 60% printable character check

### Why this matters

Without this pipeline, the coverage map would be polluted with:

- **False coverage data** from CARpeaters (your own vehicle-mounted repeater always reporting perfect signal)
- **False repeater IDs** from corrupt or non-conforming packets that partially decode, causing phantom repeaters to appear in the path with garbage data

### After validation

Validated packets enter the RX batching pipeline (see [How RX Observations Work](#how-rx-observations-work) above):

1. **Grouped by repeater ID** (last hop in path, the repeater that delivered the packet to you)
2. **Best SNR kept** per repeater. If multiple packets arrive from the same repeater, only the one with the strongest SNR is retained. GPS location is pinned to where you **first** heard that repeater.
3. **Flushed to upload queue** when you move **25 meters** from the first observation OR **30 seconds** pass, whichever comes first
4. The upload queue then buffers up to **4 RX entries per repeater** before adding them to the main batch for API upload

---

## The Noise Floor

The noise floor is the ambient radio energy when no intentional signals are present:

- Polled every **5 seconds** from your radio's hardware stats while in auto-ping mode
- Included with every data point uploaded (TX, RX, DISC, Trace)
- Helps the community understand the radio environment at each coverage point
- The noise floor graph overlays ping events on the timeline for visual correlation
- Values are reported as dBm departure from a device's 10th percentile baseline to account for variances between hardware types. See [How Calibration Works](https://wiki.meshmapper.net/layers/#how-calibration-works).

---

## The Upload Queue

All wardriving data (TX, RX, DISC, Trace) flows through a single persistent upload queue before reaching the MeshMapper API.

- **Storage**: Hive database on your device. If Hive becomes corrupted, falls back to in-memory queue (data lost if app closes).
- **Batch upload**: Auto-flushes every **15 seconds** on a timer, up to **50 items** per batch. TX/DISC/Trace pings also trigger a **5-second flush** after being queued.
- **Retry logic**: Failed uploads retry up to **5 times** with exponential backoff. Non-retryable errors (invalid data) are discarded immediately.
- **Authentication**: Handled automatically by the app
- **Fresh start**: Queue is always cleared on connect and disconnect. Pings without a valid session cannot be uploaded.
- **Offline mode**: When offline, pings accumulate in a separate list instead of the upload queue. They are saved to session files and can be uploaded later from Settings.

---

## Carpeater Filtering

A "carpeater" (car + repeater) is a repeater mounted in/on your vehicle. It will always have a very strong signal and does not provide useful coverage data.

**Two filter methods:**

1. **RSSI threshold**: RSSI equal to or stronger (closer to 0) than -30 dBm → automatically dropped (device is right next to you)
2. **User-configured repeater ID**: Specify your repeater's hex ID in Settings > Filtering > CARpeater Filter. Echoes from that repeater are stripped before upload.

Both can be adjusted or disabled in Settings for testing.

---

## Multi-Byte Path Support

Each packet carries a "path" showing which repeaters it traveled through, with each hop identified by a hash of the repeater's public key.

- **1 byte** (default): 256 possible values, can cause collisions in large networks
- **2 bytes**: ~65K values, reduced collisions
- **3 bytes**: ~16M values, maximum resolution

**Key details:**

- Configurable in Settings > Radio > TX Bytes (firmware 1.14+ required)
- RX auto-detects path size regardless of your TX setting
- Regional administrators can require a specific TX path setting in the admin panel

---

## Platform Differences

| Feature | Android | iOS | Web |
|---------|---------|-----|-----|
| BLE library | flutter_blue_plus | flutter_blue_plus | flutter_web_bluetooth |
| Background mode | Foreground service + notification | Background modes (bluetooth-central, location) | Not available |
| Debug logging | File-based | File-based | Browser console (`?debug=1`) |
| Background location | Automatic with foreground service | Requires "Always" permission | N/A |
| App exit option | Yes (Settings) | No | No |
| Audio focus | Transient with ducking | Ambient category | Default |

---

## Community and Data Privacy

Your wardriving data contributes to the public coverage map at [meshmapper.net](https://meshmapper.net/). The data includes:

- GPS coordinates, repeater signal quality, noise floor, device power level
- No personal information beyond what is inherent to the mesh protocol (device public key for auth)

**On-air privacy:** your GPS position is not broadcast over the mesh by default — TX pings carry a short anonymous token, and coordinates go only to the MeshMapper API. Enable "Broadcast My Coordinates" only if you want your live position visible on the air.

If you prefer not to broadcast your device name either, enable Anonymous Mode in Settings.

You can also view and manage the data you've contributed through the [My MeshMapper portal](portal.md).
