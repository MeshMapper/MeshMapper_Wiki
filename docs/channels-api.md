# Channels API

The Channels API lists the hashtag channels a region's admins have set up for it. That's the same list the MeshMapper app listens on for passive RX in that region. Use it to show a region's local channels, or to set them up in your own client, without scraping the map. Send your integration key in the `X-API-Key` header.

```
GET https://yow.meshmapper.net/get_channels.php
```

- On a **region** site: that region's own channels.
- On a **group** site (e.g. `pnw.meshmapper.net`): every enabled member region's channels, combined. A channel set up in several members is listed once.

There are no parameters.

## Authentication

Send your existing **integration key** (formerly a Coverage key) in the `X-API-Key` header. No new key is needed. See [API keys and access](api-keys.md) for generation, group permissions, custom GLOBAL integrations and the v1.5.117 rollout.

Fetch from your backend and serve your own parsed data to visitors. Keep the key out of client-side JavaScript.

## Response

```json
{
  "generated_at": "2026-09-30T18:00:00Z",
  "region": "YOW",
  "zones": ["YOW"],
  "count": 2,
  "channels": [
    { "name": "#ottawa", "key": "7871ec72b45617696c35c970bddd8124", "hash": "21", "zones": ["YOW"] },
    { "name": "#yow-mesh", "key": "f371e82cb45c1f1d55f97f917055c1a2", "hash": "6c", "zones": ["YOW"] }
  ]
}
```

### Top-level fields

| Field | Description |
| --- | --- |
| `generated_at` | When this answer was built. |
| `region` | The region code this page serves, uppercase. On a group site this is the group's own code. |
| `zones` | The region codes included in this answer: one code on a region site, every enabled member on a group site. |
| `count` | How many channels are listed. |
| `channels` | One entry per channel, sorted by name. Empty when the region hasn't set any up. |

### Channel fields

| Field | Description |
| --- | --- |
| `name` | The channel name with its `#`, in lowercase. |
| `key` | The channel's 16-byte secret as 32 hex characters: the first 16 bytes of the SHA-256 of `name` (including the `#`). Every MeshCore client derives the same key from the name; it's here so you don't have to. |
| `hash` | The channel's one-byte hash as 2 hex characters: the first byte of the SHA-256 of the key. This is the byte that identifies the channel in packets on air. |
| `zones` | The region codes that set up this channel. Always a list, even on a region site. |

The **Public** channel isn't listed, since every region has it and its key is fixed. Neither is the app's own wardriving channel, which isn't regional.

Hashtag channels are public by design: anyone who knows the name can derive the key. Nothing private is in this response.

To check a `key` and `hash` yourself:

```python
import hashlib

def channel_key(name):           # name includes the '#'
    return hashlib.sha256(name.lower().encode()).digest()[:16]

k = channel_key("#ottawa")
print(k.hex(), hashlib.sha256(k).hexdigest()[:2])   # 7871ec72b45617696c35c970bddd8124 21
```

## Call limits

These reads use the key's shared read budget, normally **1,000 requests per UTC day and 30 per fixed minute**, independently of Coverage's daily quota. Authenticated reads no longer use the old once-per-target IP interval. IP burst protection still applies. Every admitted request counts, including `304` responses and downstream failures. See [limits and caching](api-keys.md#limits-and-caching).

## Caching

Responses use `Cache-Control: private, no-store`. Keep your backend's parsed data and ETag separately by key and scope. Send both `X-API-Key` and `If-None-Match` on conditional requests; a `304` saves bandwidth but still counts. Responses support gzip compression.

## Errors

Authentication, permissions and quota errors are listed in [Read API errors](api-keys.md#read-api-errors).

| Status | Error | Meaning |
| --- | --- | --- |
| 404 | `zone_not_found` | The region is unknown, pending or disabled. |
| 405 | `method_not_allowed` | Use GET or an OPTIONS preflight. |
| 503 | `unavailable` | Temporary data problem; retain your previous copy and retry later. An admitted request still consumes quota. |
| 503 | `slow_down` | IP burst protection; wait for Retry-After. |

A group request requires access to every enabled member.

## Example

With `MESHMAPPER_API_KEY` set in your backend environment:

```bash
curl --fail-with-body --compressed \
  -H "X-API-Key: $MESHMAPPER_API_KEY" \
  'https://yow.meshmapper.net/get_channels.php'
```

Schedule polling to fit your key budget, retain the last successful data on failure, and respect `Retry-After`.
