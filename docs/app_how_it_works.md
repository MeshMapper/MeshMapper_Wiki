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

MeshMapper talks to your radio over **Bluetooth Low Energy (BLE)**, **TCP** (Wi-Fi), or **USB serial** (Android only). Over BLE it uses the Nordic UART service (`6E400001-…`):

- The app **writes** commands to characteristic `6E400002-…` (the "RX" characteristic, named from the radio's side)
- The app **receives notifications** (responses and events) on characteristic `6E400003-…` (the "TX" characteristic)

All communication follows the **MeshCore Companion Protocol**, a binary protocol where the app sends commands and the radio responds with data or event notifications. The same protocol runs over all three links.

**Bluetooth library:** `flutter_blue_plus` on Android and iOS.

---

## How TX Channel Messages Work

When you send a TX ping (manually or via auto-ping), you are sending a **channel message** that floods the mesh:

1. **Message composition**: By default the message is a short **anonymous token**, `MM:` followed by a keyed "wire tag" unique to your session and ping. Your GPS coordinates and power level travel to MeshMapper only via the API, not in the on-air message. If **Broadcast My Coordinates** is enabled in Settings, your coordinates are appended to the token (`MM:<tag>:lat,lon`).
2. **Sending and encryption**: The app hands the plain text to your radio with the `CMD_SEND_CHANNEL_TXT_MSG` command on the #wardriving channel. The radio encrypts it with AES-128-ECB, using the #wardriving channel key (the first 16 bytes of the SHA-256 hash of "#wardriving"). ECB mode is mandated by the MeshCore protocol. Anyone with the community channel key can decrypt the message, which is why it carries a token rather than your location by default.
3. **Broadcast and flooding**: The radio transmits it as a group text (GRP_TXT) packet that **floods the entire mesh** by default (every repeater relays it). If a **flood scope** is configured by the regional admin, only repeaters within the scope relay it.
4. **Echo listening (5-second window)**: After sending, the app opens a 5-second listening window. Every incoming packet is checked in this order, and is counted as an echo only if it passes them all:
    - Packet is a GRP_TXT packet
    - Path length is > 0 (the packet has traveled through at least one repeater)
    - If the **first hop** is your own CARpeater: a single-hop packet is dropped; otherwise your CARpeater's hop is stripped and the next repeater is credited, with no SNR/RSSI (those readings belong to your CARpeater)
    - Neither the first hop nor the credited repeater is on the region's shared CARpeater list
    - The repeater is not excluded by your CARpeater filter
    - RSSI is NOT -30 dBm or stronger (closer to zero), which would suggest a vehicle-mounted "CARpeater". This check can be switched off in Settings, and is skipped when a CARpeater hop was stripped.
    - Channel hash matches #wardriving
    - Decrypted content matches the ping just sent
5. **Which repeater is credited**: An echo that came straight from one repeater (1 hop) is credited to that repeater and goes in the TX ping's results. An echo that traveled through several repeaters (path longer than 1) is credited to the **last** repeater in its path, the one you heard, and is uploaded as a separate RX item at the ping's location.
6. **Deduplication**: If the same repeater is heard more than once, only the reading with the best SNR is kept.
7. **Queuing**: After the 5-second window closes, the TX ping and its echo results are added to the **upload queue**. A 5-second flush timer starts. When the timer expires, the queue uploads.

A session can send at most **2047** TX pings (the wire tag's counter limit). When it runs out, the app uploads what is queued and disconnects; reconnect to start a new session.

### TX vs RX Queuing

TX pings are queued differently from RX observations:

- **TX, DISC and Trace** results go directly into the upload queue as items (a TX ping and its echoes are one item; each discovered repeater is one DISC item). A **5-second flush timer** triggers an upload shortly after.
- **RX observations** go through a **two-stage pipeline**: first the RX Logger batches by repeater (best SNR, 25 meter/30 second flush), then the upload queue holds up to **4 RX entries per repeater** before moving them to the main queue. Any more from the same repeater before that move are dropped.

---

## How RX Observations Work

While an **auto mode is running** (Active, Passive, Hybrid or Trace), the app logs mesh traffic your radio overhears. When no auto mode is running, the only packets it uses are the echoes of a manual ping during its 5-second window.

- Mesh traffic the radio overhears is processed, validated, and queued for upload
- RX observations are "free data" requiring no transmission from you
- They capture other devices' mesh traffic, adding extra coverage data from your location
- An observation needs a GPS fix. Packets heard while the phone has no fix are dropped.

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

1. **Request**: Control data command (0x37) with the DISCOVER_REQ flag, asking repeaters and room servers in direct range to answer. It carries a random 4-byte tag.
2. **Response**: Repeaters respond with node type, public key, and their assessment of signal quality from their end (remote SNR).
3. **Tracking**: The app listens for 7 seconds. It accepts answers carrying any tag, so an answer to another phone's discovery heard in that window counts too (the tag is only used to time replies to your own request). Answers are grouped by the repeater's ID (the first 1 to 3 bytes of its public key, following your TX Bytes setting), keeping the best local SNR. Answers from the region's shared CARpeaters, from your own CARpeater, and at -30 dBm or stronger (unless the RSSI filter is off) are dropped. The result is **bidirectional** signal quality (how you hear them & how they hear you).
4. **Upload**: One "DISC" item per repeater, with its public key, node type, and bidirectional signal quality. If nobody answered and **Discovery Drop** is on, a single DISC item with no repeater is uploaded instead.

---

## How Trace Pings Work

Trace pings target a specific repeater by hex ID:

1. **Command**: CMD_SEND_TRACE_PATH (0x24) as a zero-hop trace. The target ID is 1, 2 or 4 bytes, following your **Trace Bytes** setting.
2. **Response**: If in range, the repeater responds with PUSH_CODE_TRACE_DATA (0x89) containing signal quality
3. **Logging**: Successful traces → uploaded to API. Failed traces (no response within 5s) → logged locally, shown as grey markers on the noise floor graph.

---

## How Smart Pinging Works

Smart Pinging is the app's way of not repeating work the map already shows. It is on by default and applies to Hybrid, Passive and Active modes.

1. **Coverage lookup**: While connected, the app keeps MeshMapper's recent coverage for roughly 500m around you loaded. It uses the same vector tiles the map draws, filtered to two-way (green) and discovery (cyan) results inside your Smart Pinging window. The lookup re-checks after every 100m of movement and refreshes tiles older than 5 minutes at the next 100m. Squares you cover yourself during the session (a heard TX, an answered discovery) are marked covered immediately.
2. **The check**: When an auto ping (TX or discovery) is due, the app looks up the square under your current GPS fix. The square is the cell of your Grid Mode setting (300m, or 100m in Detailed). A recent green or cyan result there means the ping is deferred, and the countdown reads "Deferred". The check runs before the minimum distance rule, so a covered square reads "Deferred" rather than "Skipped".
3. **The hold**: A deferred ping is banked in a single slot. On every GPS fix the app asks whether you have reached a square with no recent coverage and moved at least your minimum ping distance since the last ping of that kind. If so, the banked ping goes out and the interval timer restarts. A later deferral replaces an earlier one, so at most one ping is ever waiting. The regular interval keeps running underneath, so a phone that never reaches a fresh square still tries at its normal cadence.
4. **Fail open**: If the coverage data is not loaded yet, a fetch failed, you are outside a zone, or you are in Offline Mode, the ping is sent as normal. Smart Pinging only ever holds a ping it knows to be redundant.
5. **Credit**: A deferred ping posts no coverage row, so on its own it would cost you the point that ping would have earned. Instead the app reports a small `DEFER` item for each square where it held a ping (one per 300m square per session, whatever your Grid Mode) in the normal upload batch. MeshMapper verifies the square really was covered in its own data, drops any it cannot confirm, and credits the accepted ones at 1.5 points each. Accepted squares also drive the Airtime awards and the Top Airtime Savers leaderboard.

!!! note
    Manual pings, Trace Mode and passive RX listening are never deferred. RX is free coverage, and the other two are you asking for a specific measurement.

---

## How Scope Discovery Works

Scope discovery asks repeaters which **regions (flood scopes)** they carry. It runs when **Scope Discovery** is on (switched on by you, or enforced by the region), your region's server offers it, and your companion firmware is 1.16.0 or newer.

1. **After a discovery**: The app picks up to 3 of the strongest repeaters the discovery found that are due to be asked. A repeater is due only if nobody has asked it within the refresh interval.
2. **The question**: One at a time, the app sends each one a short anonymous "regions" request, routed directly to it. Your pings are not delayed.
3. **The answer**: The repeater replies with its list of region names (`*` means it passes unscoped traffic). The app uploads it as a `SCOPES` item, always after the DISC item for the discovery that found the repeater.

See [Scope Discovery](app_settings_reference.md#scope-discovery) for the settings.

---

## Packet Filtering and Validation

Every overheard (RX) packet goes through a strict validation pipeline before being accepted. If a packet fails any step, it is dropped immediately.

### 1 Path length check

- Packet must have traveled through **at least one repeater** (path length > 0)
- Direct transmissions from nearby devices are not repeater coverage data
- **Direct-routed** packets are dropped too: their path lists the route still ahead of them, not the repeater you heard

### 2 Vehicle-mounted "CARpeater" ID check

- If you have set your CARpeater's public key in the CARpeater Filter:
    - **Single hop** from your CARpeater → **dropped** (this is just your own repeater relaying back to you, no real coverage info)
    - **Multiple hops** with your CARpeater as the last hop → your CARpeater's hop is **stripped**, and the second-to-last hop is used as the real repeater (the packet traveled through a distant repeater first, then your CARpeater delivered it to you. The distant repeater is the real coverage data. SNR/RSSI are set to null since they reflect your CARpeater's signal, not the distant repeater's.)
- If the repeater about to be credited is on the region's shared **Regional CARpeaters** list → **dropped**

**No GPS fix**: a packet that passes the checks so far is dropped if the phone has no GPS fix, since it could not be placed on the map.

### 3 RSSI check (CARpeater failsafe)

- Signal must be **weaker (farther from zero) than -30 dBm**
- Anything stronger implies the relaying node is right next to you (likely a CARpeater)
- Acts as a safety net even without the CARpeater ID filter
- Skipped if the Disable RSSI Filter option is ENABLED in app Settings or if a CARpeater hop was already stripped

### 4 Packet type check

- Only two payload types accepted:
    - **GRP_TXT** (0x05) — Channel messages
    - **ADVERT** (0x04) — Node advertisements

### 5 Channel hash check (GRP_TXT only)

- Payload must be at least 3 bytes (channel hash plus MAC)
- Channel hash must match an **allowed channel**: Public, #wardriving, and your region's channels
- Prevents random mesh traffic from being counted as coverage data

### 6 Decryption (GRP_TXT only)

- Payload decrypted with the matching channel's AES-128-ECB key
- Dropped if decrypted data is too short (< 5 bytes)

### 7 Printable character check (GRP_TXT only)

- At least **60%** of the decrypted message must be printable ASCII (codes 32-126)
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

1. **Grouped by repeater ID** (last hop in path, the repeater that delivered the packet to you, or the one behind your CARpeater)
2. **Best SNR kept** per repeater. If multiple packets arrive from the same repeater, only the one with the strongest SNR is retained. GPS location is pinned to where you **first** heard that repeater.
3. **Flushed to upload queue** when you move **25 meters** from the first observation OR **30 seconds** pass, whichever comes first
4. The upload queue then holds up to **4 RX entries per repeater** before adding them to the main batch for API upload

---

## The Noise Floor

The noise floor is the ambient radio energy when no intentional signals are present:

- Polled every **5 seconds** from your radio's stats, from the moment you connect
- Included with every TX, RX, DISC and Trace item uploaded
- Helps the community understand the radio environment at each coverage point
- The noise floor graph overlays ping events on the timeline for visual correlation
- On the map, MeshMapper shows each reading as its difference from **your own** baseline (the 10th percentile of all your readings), which evens out differences between radios. See [Noise Floor](layers.md#noise-floor).

---

## The Upload Queue

All wardriving data (TX, RX, DISC, Trace, plus DEFER and SCOPES items) flows through a single persistent upload queue before reaching the MeshMapper API.

- **Storage**: Hive database on your device. If Hive becomes corrupted, it falls back to an in-memory queue (data lost if the app closes).
- **Batch upload**: Auto-flushes every **15 seconds** on a timer, up to **50 items** per batch. Queuing a TX, DISC, Trace, DEFER or SCOPES item also triggers a **5-second flush**. On a constrained link (such as satellite) both timers stretch to **60 seconds**.
- **Retry logic**: A batch the server rejects is retried up to **5 times** with exponential backoff. Items that ran out of retries get another chance after the next successful upload.
- **No answer**: If the server can't be reached, or asks the app to wait, the batch is held without using up a retry.
- **Discarded batches**: A batch the server refuses for its data (`gps_inaccurate`, `gps_stale`, `invalid_request`, `zone_disabled`, `outofdate`, `outside_zone`) is dropped rather than retried. Session errors such as `zone_full` also end the session. An expired session refreshes itself and the batch waits.
- **Authentication**: Handled automatically by the app
- **Fresh start**: The queue is cleared when you connect. When you disconnect, the app uploads what it can first, then clears the rest. During an automatic reconnect after a dropped link, the queue and session are kept.
- **Offline mode**: When offline, pings accumulate in a separate list instead of the upload queue. They are saved to session files and can be uploaded later from Settings > Data.

---

## Carpeater Filtering

A "carpeater" (car + repeater) is a repeater mounted in/on your vehicle. It will always have a very strong signal and does not provide useful coverage data.

**Three filter methods:**

1. **RSSI threshold**: RSSI equal to or stronger (closer to 0) than -30 dBm → automatically dropped (device is right next to you)
2. **Your CARpeater**: Set your repeater's full public key in Settings > Wardriving > CARpeater Filter. Its hop is stripped and the repeater behind it is credited instead; packets that only reached your CARpeater are dropped.
3. **Regional CARpeaters**: CARpeaters shared for your region are always dropped, and nothing behind them is credited.

The RSSI threshold can be switched off in Settings (Disable RSSI Filter). See [CARpeater settings](app_settings_reference.md#carpeater).

---

## Multi-Byte Path Support

Each packet carries a "path" showing which repeaters it traveled through, with each hop identified by the first bytes of the repeater's public key.

- **1 byte** (default): 256 possible values, can cause collisions in large networks
- **2 bytes**: ~65K values, reduced collisions
- **3 bytes**: ~16M values, maximum resolution

**Key details:**

- Configurable in Settings > Wardriving > Radio > TX Bytes (firmware 1.14+ required)
- RX auto-detects path size regardless of your TX setting
- Trace pings have their own **Trace Bytes** setting (1, 2 or 4 bytes)
- Regional administrators can require a specific TX Bytes setting in the admin panel
- When a hop ID matches more than one repeater, MeshMapper only credits it if exactly one repeater fits. See [Duplicate Repeater IDs](duplicaterepeaterid.md#the-rules).

---

## Platform Differences

| Feature | Android | iOS |
|---------|---------|-----|
| BLE library | flutter_blue_plus | flutter_blue_plus |
| Other connections | TCP, USB serial | TCP |
| Background mode | Foreground service + notification | Background modes (bluetooth-central, location) |
| Debug logging | File-based | File-based |
| Background location | Foreground service; Background Location asks for "Allow all the time" | Background Location asks for "Always" |
| App exit option | Yes (Settings > General > Close App) | No |
| Audio focus | Transient with ducking | Ambient category |

---

## Community and Data Privacy

Your wardriving data contributes to the public coverage map at [meshmapper.net](https://meshmapper.net/). The data includes:

- GPS coordinates, repeater signal quality, noise floor, device power level
- Your device's public key, used to authenticate your session

**On-air privacy:** your GPS position is not broadcast over the mesh by default — TX pings carry a short anonymous token, and coordinates go only to the MeshMapper API. Enable "Broadcast My Coordinates" only if you want your live position visible on the air.

If you prefer not to broadcast your device name either, enable Anonymous Mode in Settings. Your device is renamed "Anonymous" and you are left off the public leaderboard, but your sessions are still recorded against your public key.

See [Privacy](privacy.md) for what is collected and kept. You can also view and manage the data you've contributed through the [My MeshMapper portal](portal.md).
