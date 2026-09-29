# Webhooks

Webhooks allow MeshMapper to send real-time notifications to any external HTTPS endpoint when events occur in your region. This is useful for integrating with services like Home Assistant, custom bots, or any system that can receive HTTP POST requests.

Webhooks work alongside Discord DM notifications — enabling a webhook does not disable Discord notifications.

## Setup

1. Open your region's admin panel and go to the **Settings** tab.
2. In the **Notifications** section, enter your **Webhook URL**.
3. Select which events should trigger a webhook notification.
4. Click **Save All Settings**.
5. Use the **Send Test** button to check your endpoint receives the test payload. (It tests the URL as typed, even before saving.)

For a region in a [multiregion group](multiregions.md), the group admin can set a separate webhook for each region in the group settings.

!!! warning "HTTPS Required"
    Only HTTPS URLs are accepted. HTTP, internal, and private network URLs are blocked for security, and a non-HTTPS URL is cleared when you save.

## Events

You can enable or disable each event type individually:

| Event | Description |
|-------|-------------|
| **Ambiguous Repeater ID** | Two or more repeaters share an ID, so one or more were marked Ambiguous. See [Duplicate Repeater IDs](duplicaterepeaterid.md). |
| **Pending Repeater** | Your region has repeaters in Pending state awaiting admin review. Checked once daily. |
| **Offline Observer** | One or more MQTT observers in your region may be offline. |
| **Visitor Message** | A visitor has sent a message to your region's administrators via the map. |
| **Suspicious Flight** | A wardriving session in your region moved faster than ground travel allows. Checked once daily. |
| **Pending Repeater Link** | Pings were held for review instead of being linked to a repeater that's unusually far away. Checked once daily. |

By default, all events are enabled when a webhook URL is configured.

## Payload Format

Every webhook sends an HTTP POST request with a JSON body. The structure is consistent across all event types:

```json
{
  "event": "duplicate_repeater",
  "region": "YOW",
  "timestamp": 1744123456,
  "message": "**New Ambiguous Repeater ID Detected on YOW.**\n\n**Shared ID prefix:** `A1` (1-byte)\n\n**Repeaters:**\n[EXCLUDED] RepeaterA — 1-byte ID (A1B2C3D4)\n[ACTIVE] RepeaterB — 1-byte ID (A1E5F6A7)",
  "data": {
    "collision_group": "A1",
    "repeaters": ["[EXCLUDED] RepeaterA — 1-byte ID (A1B2C3D4)", "[ACTIVE] RepeaterB — 1-byte ID (A1E5F6A7)"]
  }
}
```

### Fields

- **event** — The event type: `duplicate_repeater`, `pending_repeater`, `offline_observer`, `visitor_message`, `suspicious_flight`, `pending_link` or `test`.
- **region** — The region code (e.g., `YOW`).
- **timestamp** — Unix timestamp of when the webhook was sent.
- **message** — A readable summary using Discord markdown, mostly the same text as the Discord DM, so simple integrations can use it directly.
- **data** — Event-specific structured data (see below).

### Event-Specific Data

**duplicate_repeater:**

- `collision_group` — The shared ID prefix (1–3 bytes, e.g. `A1`).
- `repeaters` — Array of the repeaters sharing it, each marked `[EXCLUDED]` or `[ACTIVE]`.

**pending_repeater:**

- `count` — Number of repeaters currently in Pending state.

**offline_observer:**

- `stale_observers` — Array of observer descriptions that appear to be offline.

**visitor_message:**

- `body` — The full text of the visitor's message.

**suspicious_flight:**

- `sessions` — Array of the session IDs flagged.

**pending_link:**

- `repeaters` — Array of the repeater IDs with held pings.

**test:**

- `info` — A static test string confirming the webhook is working.

## Troubleshooting

**Webhook not firing:**

- Ensure the URL starts with `https://`.
- Verify the event type checkbox is enabled in Settings.
- Check that the URL is reachable from the MeshMapper server.
- Use the **Send Test** button to isolate the issue.

**Test button doesn't show "Sent!":**

- It shows the error or the HTTP status code instead. The endpoint may be unreachable, returning an error, or timing out (3-second limit).
- Verify the URL is correct and the endpoint is accepting POST requests with JSON content.

**Receiving duplicate notifications:**

- Webhooks and Discord DMs operate independently. If you receive both, this is expected behavior.

## Technical Details

- Webhook requests use HTTP POST with `Content-Type: application/json`.
- Requests have a 3-second timeout and do not follow redirects.
- Failed notifications are not re-sent.
- After a temporary error (timeout, network error, HTTP 408, 425, 429 or 5xx), the webhook pauses for 5 minutes, doubling up to 6 hours (a `Retry-After` header is respected). Events during the pause are skipped.
- After 3 permanent errors in a row, the webhook is switched off and a warning appears in Settings. A successful **Send Test** or a new URL switches it back on.
