# Wardriving Modes

MeshMapper offers four automated wardriving modes plus manual pinging. Each mode serves a different purpose, and choosing the right one depends on your goals and environment.

While a mode runs, its button turns green with an **Active** label underneath, and the button text counts down what happens next: **Next ping Ns**, **Next disc Ns**, **Listening Ns**, **Deferred Ns**, **Skipped Ns** or **Stopping Ns**. A small **Scopes** badge appears on the running Passive or Hybrid button while [Scope Discovery](app_settings_reference.md#scope-discovery) is asking repeaters for their scopes.

---

## Manual Ping

The simplest way to wardrive. Tap the **Send Ping** button on the Map tab to send a single channel message to #wardriving.

**What happens:**

1. The app checks that you have a TX slot, that your antenna and power level are set, that you have a GPS fix accurate to 100 m or better, that you are not airborne, and that the 15-second manual cooldown has passed. There is no minimum distance for manual pings. Whether you are inside a zone is checked by the server.
2. A short message is encrypted and sent as a channel message to #wardriving. This message **floods the entire mesh network**. If a **scope** is configured, it is scoped to that region instead.
   - **By default, the message does not contain your GPS position.** It carries a short anonymous token, and your coordinates travel only to the MeshMapper server via the API. Anyone listening on the channel sees the token, not your location. (See [Broadcast My Coordinates](app_settings_reference.md#broadcast-my-coordinates) to opt in to on-air coordinates.)
3. The app listens for **5 seconds** for repeater echoes
4. Echoes are matched (decrypted and compared to what you sent) and logged as "heard repeats"
5. Ping and echo data are queued for upload

The controls unlock as soon as the 5-second window ends. The upload happens in the background. Send Ping itself then shows **Cooldown** until its 15 seconds are up.

**When to use:** Quick testing, spot-checking a specific location, or occasional pings.

---

## Hybrid Mode

*Thanks to HerculesMulligan for coming up with the idea for this mode.*

Hybrid Mode is the **recommended default** for wardriving. It alternates between channel messages (TX) and discovery requests at your configured interval.

**To start:** Tap the **Hybrid Mode** button in the Controls panel on the Map tab. Hybrid is on by default. If Hybrid Mode is switched off under Settings > Wardriving > Modes, this button shows as "Active Mode" instead.

The button only appears while **Flood Traffic** is on. Flood Traffic is off on a fresh install, but the app turns it on each time you connect in a region that allows flood traffic. The button is also hidden while your zone is full (see [TX Capacity Limits](#tx-capacity-limits)).

**What happens each interval (alternating):**

- **1** Discovery request (direct query, does not flood the mesh)
- **2** Channel message / TX (floods the mesh or is scoped)
- **3** Discovery request
- **4** Channel message / TX
- And so on...

**What it produces:** TX channel messages, discovery responses, and passive RX observations, all interleaved. The richest dataset of any mode.

**Why Hybrid is the default:** 50% fewer channel messages than Active Mode while also collecting discovery data. Better for mesh health and more useful coverage data.

**Minimum distance:** Enforced between pings (configurable in Settings, default 25m). Pings are skipped while you are stationary.

**Regional enforcement:** A regional admin can require Hybrid Mode for a radio preset ("Enforce Hybrid", off by default). When it is enforced, the Hybrid Mode switch in Settings is locked on.

!!! warning "Firmware requirement"
    The discovery half requires repeater firmware **1.10 or newer**. Repeaters on older firmware will not respond to discovery requests, but will still echo your channel messages normally. TX pings work with any firmware version.

---

## Passive Mode

No channel messages (no mesh flooding at all). Sends **discovery requests** every 30 seconds and listens to other mesh traffic.

**To start:** Tap the **Passive Mode** button (ear icon) in the Controls panel.

**What happens:**

1. Every 30 seconds, sends a zero-hop discovery request (direct query, not a broadcast). Like the other auto modes, it skips the request if you have not moved your minimum ping distance, and defers it in squares with recent coverage ([Smart Pinging](#smart-pinging)).
2. Repeaters/rooms respond with node type, public key, and signal quality (local + remote SNR/RSSI)
3. Responses are collected for 7 seconds and deduplicated by public key. CARpeaters are filtered out: anything received at -30 dBm or stronger, your own CARpeater (matched by its full public key), and any CARpeater on your region's shared list.
4. The app also listens to other mesh traffic it hears (RX)
5. All discovery responses and RX observations are queued for upload

**What it produces:** Discovery data (which repeaters are in direct range, bidirectional signal quality) and passive RX observations.

**When to use:** Map repeater locations without flooding the mesh. Also available when your zone is at TX capacity (see [TX Capacity Limits](#tx-capacity-limits)).

!!! warning "Firmware requirement"
    Discovery requests require repeater firmware **1.10 or newer**. Repeaters on older firmware will not respond, so Passive Mode (and the discovery half of Hybrid Mode) will not detect them.

---

## Active Mode

!!! warning "Legacy mode"
    Hybrid Mode has replaced Active Mode as the default and is recommended for all wardriving. Active Mode is kept for backward compatibility but Hybrid produces richer data with less mesh traffic. To use Active Mode, turn off Hybrid Mode in Settings > Wardriving > Modes (not possible where your region enforces Hybrid).

Sends only channel messages (no discovery requests) at a regular interval (15, 30, or 60 seconds).

**What happens each interval:**

1. Checks your GPS fix and the minimum distance
2. If you haven't moved far enough (based on Settings, default 25m), the ping is skipped
3. Channel message sent (floods mesh or scoped) + 5-second echo listening window
4. The app also listens to other mesh traffic it hears (RX)
5. All data (TX + RX) queued for upload

**What it produces:** TX data (location, repeater echoes, SNR/RSSI) and passive RX observations.

---

## Trace Mode

Targets a **specific repeater** by hex ID for focused signal testing.

**To start:** In the Trace row under the mode buttons (route icon), type the repeater's hex ID or tap the list button to choose it, then tap **Trace Mode**. The ID length follows your [Trace Bytes](app_settings_reference.md#trace-bytes) setting.

**What happens each interval:**

1. Sends a zero-hop trace path command to the target repeater, at your auto-ping interval. Traces are skipped until you have moved your minimum ping distance.
2. The app listens **5 seconds** for a response
3. If the repeater responds: logs RX SNR, RX RSSI, and remote (TX) SNR
4. Successful traces are uploaded. Failed traces are logged on the phone only, and show as grey markers on the noise floor graph.

**What it produces:** Point-to-point signal quality over time and distance.

**When to use:** Antenna alignment, evaluating a specific repeater's coverage, diagnosing signal quality to a particular node. Trace Mode also works when your zone is full or your region has turned flood traffic off.

---

## Smart Pinging

Smart Pinging holds back auto pings in squares that MeshMapper has already mapped recently, so your airtime goes where it adds something new. It is **on by default** and applies to Hybrid, Passive and Active modes.

**What happens:**

1. While you are connected, the app keeps MeshMapper's recent coverage for the area around you loaded.
2. When an auto ping is due in a square that already has a recent two-way (green) or discovery (cyan) result, the ping is **deferred** instead of sent. The countdown reads **"Deferred"** while it waits.
3. The deferred ping is kept, not dropped. As soon as you reach a square with no recent coverage (and have moved your minimum ping distance), it goes out and the interval restarts.
4. Only one ping is ever held. If the next interval is deferred too, it takes the place of the one waiting.

Each deferral leaves a hollow circle on the map. You can hide these with **Show Deferred Markers** in Settings.

**What counts as covered:** a square with a green or cyan result inside your Smart Pinging window (default 14 days). Squares follow your [Grid Mode](app_settings_reference.md#grid-mode) setting, so what is deferred is exactly what is already painted on the map.

**Never deferred:**

- Manual pings
- Trace Mode
- Passive listening to other mesh traffic (RX), which is free coverage
- Anywhere the coverage data cannot be loaded (no network, Offline Mode, outside a zone). The ping simply goes out.

!!! note "Deferred is not Skipped"
    A ping that fails the minimum distance rule reads "Skipped" and is dropped. A deferred ping reads "Deferred" and is still owed.

**You keep your points.** Every square where a ping was held is reported to MeshMapper, checked against the region's own coverage data, and credited at **1.5 points** once verified (once per 300m square per session). Verified squares also count toward the Airtime awards and the Top Airtime Savers leaderboard. See [Top Airtime Savers](leaderboards.md#top-airtime-savers).

To turn Smart Pinging off or change the window, see [Smart Pinging](app_settings_reference.md#smart-pinging) in the Settings Reference. Regional admins can enforce it for their zone, in which case the switch is locked on and the window is the region's.

---

## TX Capacity Limits

Regional admins set a **maximum number of active TX wardrivers** (slots) for each radio preset in their region. This prevents too many users from flooding the mesh at once. A preset the admin has not set up gets 0 slots, flood traffic turned off and a 60-second minimum interval.

!!! note "Regions can disable flood traffic entirely"
    Some regions disable flood (TX) wardriving traffic altogether. In those zones the **Flood Traffic** setting is locked off and shows as set by the regional admin, the Active/Hybrid and Send Ping buttons are hidden, and Passive and Trace modes are the available options.

**When the zone is at capacity:**

- **Send Ping and the Hybrid / Active Mode button are hidden** (they all send TX channel messages)
- **Passive Mode and Trace Mode still work**
- Tapping the zone chip in the Map tab's status bar explains that the zone is at capacity

**To get a TX slot:**

- Wait for another wardriver to disconnect and free up a slot
- Slots are handed out when a session starts, so disconnect and reconnect to pick one up

---

## Which Mode Should I Use?

| Scenario | Recommended Mode |
|----------|-----------------|
| General wardriving (driving/walking) | Hybrid Mode |
| Mapping coverage in a new area | Hybrid Mode |
| Finding nearby repeaters without mesh traffic | Passive Mode |
| Zone at TX capacity | Passive Mode (or Trace Mode) |
| Testing signal to a specific repeater | Trace Mode |
| Quick spot-check at one location | Manual Ping |

---

## Stopping Auto-Ping

- Tap the running mode button again (green, with **Active** under it). If a listening window is still open, the button reads **Stopping** until it ends.
- After stopping Active or Hybrid Mode there is a 5-second cooldown to prevent accidental toggling
- If "Auto-Stop After Idle" is enabled (the default): auto-ping stops after **30 minutes** without movement. Moving means leaving a 150 m circle around where you stopped, on 3 GPS fixes in a row.

---

## Data Flow

Regardless of mode, all data follows the same pipeline:

1. **Ping event** (TX, RX, DISC, or Trace)
2. **Logged in app** (Log tab, and the noise floor graph in the History tab)
3. **Queued for upload** (a queue saved on the phone)
4. **Batch uploaded** (up to 50 items per batch). Pings are sent within about 5 seconds, other items about every 15 seconds. On a slow link, such as satellite, both stretch to 60 seconds.
5. **Appears on meshmapper.net** (community coverage map)

!!! note
    RX observations have an extra buffering step: grouped by repeater ID, flushed to the upload queue when you move 25m or after 30 seconds, whichever comes first. At most 4 RX observations per repeater go into each batch.

---

## Sound Notifications

Off by default. If enabled (Settings > General > Sound Notifications):

- **TX sent or Discovery sent:** Transmitted packet sound
- **Repeater echo or RX received:** Received packet sound

Helpful when wardriving with phone mounted and out of direct view.
