# Wardriving Modes

MeshMapper offers four automated wardriving modes plus manual pinging. Each mode serves a different purpose, and choosing the right one depends on your goals and environment.

---

## Manual Ping

The simplest way to wardrive. Tap the **Send Ping** button on the Map tab to send a single channel message to #wardriving.

**What happens:**

1. The app checks GPS, zone, and that the 15-second manual cooldown has elapsed. No minimum distance requirement for manual pings.
2. A short message is encrypted and sent as a channel message to #wardriving. This message **floods the entire mesh network**. If a **scope** is configured, it is scoped to that region instead.
   - **By default, the message does not contain your GPS position** — it carries a short anonymous token, and your coordinates travel only to the MeshMapper server via the API. Anyone listening on the channel sees the token, not your location. (See [Broadcast My Coordinates](app_settings_reference.md#broadcast-my-coordinates) to opt in to on-air coordinates.)
3. The app listens for **5 seconds** for repeater echoes
4. Echoes are matched (decrypted and compared to what you sent) and logged as "heard repeats"
5. Ping and echo data are queued for upload

Controls lock during the 5-second window and API upload.

**When to use:** Quick testing, spot-checking a specific location, or occasional pings.

---

## Hybrid Mode

*Thanks to HerculesMulligan for coming up with the idea for this mode.*

Hybrid Mode is the **recommended default** for wardriving. It alternates between channel messages (TX) and discovery requests at your configured interval.

**To start:** Tap the **Hybrid Mode** button in the Controls panel on the Map tab. (Enabled by default. If disabled in Settings, this button shows as "Active Mode" instead.)

**What happens each interval (alternating):**

- **1** Discovery request (direct query, does not flood the mesh)
- **2** Channel message / TX (floods the mesh or is scoped)
- **3** Discovery request
- **4** Channel message / TX
- And so on...

**What it produces:** TX channel messages, discovery responses, and passive RX observations, all interleaved. The richest dataset of any mode.

**Why Hybrid is the default:** 50% fewer channel messages than Active Mode while also collecting discovery data. Better for mesh health and more useful coverage data.

**Minimum distance:** Enforced between pings (configurable in Settings, default 25m). Pings pause when stationary.

**Regional enforcement:** Enabled by default across all regions because we feel it provides the best balance between mesh load and data collected. Regional admins can disable Hybrid Mode for their zone via the admin portal if it doesn't suit their region.

!!! warning "Firmware requirement"
    The discovery half requires repeater firmware **1.10 or newer**. Repeaters on older firmware will not respond to discovery requests, but will still echo your channel messages normally. TX pings work with any firmware version.

---

## Passive Mode

No channel messages (no mesh flooding at all). Sends **discovery requests** every 30 seconds and passively monitors mesh traffic.

**To start:** Tap the **Passive Mode** button (hearing icon) in the Controls panel.

**What happens:**

1. Every 30 seconds, sends a zero-hop discovery request (direct query, not a broadcast)
2. Repeaters/rooms respond with node type, public key, and signal quality (local + remote SNR/RSSI)
3. Discovery Tracker collects responses during a 7-second window, deduplicates by public key, and filters carpeaters (RSSI stronger than -30 or by user-configured prefix value)
4. Unified RX Handler monitors for mesh traffic on subscribed channels
5. All discovery responses and RX observations queued for upload

**What it produces:** Discovery data (which repeaters are in direct range, bidirectional signal quality) and passive RX observations.

**When to use:** Map repeater locations without flooding the mesh. Also the only mode available when your zone is at TX capacity (see [TX Capacity Limits](#tx-capacity-limits)).

!!! warning "Firmware requirement"
    Discovery requests require repeater firmware **1.10 or newer**. Repeaters on older firmware will not respond, so Passive Mode (and the discovery half of Hybrid Mode) will not detect them.

---

## Active Mode

!!! warning "Legacy mode"
    Hybrid Mode has replaced Active Mode as the default and is recommended for all wardriving. Active Mode is kept for backward compatibility but Hybrid produces richer data with less mesh traffic. To use Active Mode, disable Hybrid Mode in Settings > Modes.

Sends only channel messages (no discovery requests) at a regular interval (15, 30, or 60 seconds).

**What happens each interval:**

1. Checks GPS freshness and minimum distance requirement
2. If you haven't moved far enough (based on Settings, default 25m), the ping is skipped
3. Channel message sent (floods mesh or scoped) + 5-second echo listening window
4. Unified RX Handler monitors for passive mesh traffic
5. All data (TX + RX) queued for upload

**What it produces:** TX data (location, repeater echoes, SNR/RSSI) and passive RX observations.

---

## Trace Mode

Targets a **specific repeater** by hex ID for focused signal testing.

**To start:** Tap the **Trace Mode** button (crosshair icon). Enter or select a repeater's hex ID.

**What happens each interval:**
1. Sends a zero-hop trace path command to the target repeater
2. Trace Tracker listens **5 seconds** for a response
3. If the repeater responds: logs RX SNR, RX RSSI, and remote (TX) SNR
4. Successful traces → posted to API. Failed traces → logged locally, shown as grey markers on noise floor graph.

**What it produces:** Point-to-point signal quality over time and distance.

**When to use:** Antenna alignment, evaluating a specific repeater's coverage, diagnosing signal quality to a particular node.

---

## TX Capacity Limits

Regional admins set a **maximum number of active TX wardrivers** per zone (for example, 5). This prevents too many users from flooding the mesh simultaneously.

!!! note "Regions can disable flood traffic entirely"
    Some regions disable flood (TX) wardriving traffic altogether. In those zones the Active/Hybrid/Send Ping controls are locked off (the **Flood Traffic** setting shows as set by the regional admin) and Passive and Trace modes are the available options.

**When the zone is at capacity:**

- **Manual Ping, Hybrid Mode, and Active Mode are disabled** (they all send TX channel messages)
- **Passive Mode is the only option** (discovery requests don't flood the mesh)
- The app indicates TX is not allowed for your session

**To get a TX slot:**

- Wait for another wardriver to disconnect and free up a slot
- New sessions will be granted TX access
- If already connected in Passive Mode, disconnect and reconnect to pick up a slot

---

## Which Mode Should I Use?

| Scenario | Recommended Mode |
|----------|-----------------|
| General wardriving (driving/walking) | Hybrid Mode |
| Mapping coverage in a new area | Hybrid Mode |
| Finding nearby repeaters without mesh traffic | Passive Mode |
| Zone at TX capacity | Passive Mode (only option) |
| Testing signal to a specific repeater | Trace Mode |
| Quick spot-check at one location | Manual Ping |

---

## Stopping Auto-Ping

- Tap the active mode button again (shows as "running" with a pulsing animation)
- Brief cooldown after stopping Active or Hybrid Mode to prevent accidental toggling
- If "Auto-Stop After Idle" is enabled: auto-ping stops after **30 minutes** without GPS movement

---

## Data Flow

Regardless of mode, all data follows the same pipeline:

1. **Ping event** (TX, RX, DISC, or Trace)
2. **Logged in app** (Log tab + marker on Graph)
3. **Queued for upload** (persistent Hive-based queue)
4. **Batch uploaded** (up to 50 items, auto-flush every 15 seconds)
5. **Appears on meshmapper.net** (community coverage map)

!!! note
    RX observations have an extra buffering step: grouped by repeater ID, flushed to upload queue when you move 25m or after 30 seconds, whichever comes first.

---

## Sound Notifications

If enabled (Settings > Ping Settings > Sound Notifications):

- **TX sent or Discovery sent:** Transmitted packet sound
- **Repeater echo or RX received:** Received packet sound

Helpful when wardriving with phone mounted and out of direct view.
