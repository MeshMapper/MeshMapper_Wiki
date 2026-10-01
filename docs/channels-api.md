# Channels API

The Channels API lists the hashtag channels a region's admins have set up for it. That's the same list the MeshMapper app listens on for passive RX in that region. Use it to show a region's local channels, or to set them up in your own client, without scraping the map. No key is needed.

```
GET https://yow.meshmapper.net/get_channels.php
```

- On a **region** site: that region's own channels.
- On a **group** site (e.g. `pnw.meshmapper.net`): every enabled member region's channels, combined. A channel set up in several members is listed once.

There are no parameters.

!!! warning "One call per day; keep calling early and you're banned"
    Each region site's answer can be fetched **once every 23.5 hours per IP address**. A second request to the same region site inside that window is refused with `429`, and **the third refused request within the window bans your IP address from all of meshmapper.net for a day**. Every repeat doubles the ban, up to 30 days. See [Call limits](#call-limits). Accessing anything that isn't a published API, or scraping pages for data, is not allowed; see the warning on the [Coverage API](coverage-api.md) page.

!!! warning "Call this from your server, not your visitors' browsers"
    Fetch this API from your own backend, store the result, and serve your own copy to visitors. Don't call it from client-side JavaScript in a visitor's browser: everyone behind the same home router or mobile carrier shares one public IP address, so one visitor's fetch uses the call and the next visitor's fetch bans that whole IP address from all of meshmapper.net, including every MeshMapper app user on that network.

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

- **One call per region site every 23.5 hours per IP address.** A group site counts as its own site, separate from its members.
- **An early call is refused with `429`; the third refusal within the window bans your IP address.** Your IP address is banned from all of meshmapper.net (the map included, and every device behind that IP address) for 1 day. Each repeat doubles the ban: 2 days, 4 days, 8 days, up to 30 days.
- **At most 30 calls a minute from one IP address, across all these APIs together.** A call over that gets `503` with `{"error":"slow_down","retry_after":N}`. It doesn't use your call and never counts toward a ban: wait `Retry-After` seconds and carry on. Pausing 2 seconds between calls keeps you under it.
- **Only certain JSON errors hand your call back.** A `404` `zone_not_found`, a `503` `unavailable`, or a `503` `slow_down` (after waiting `Retry-After`) doesn't use your call, so retrying after one of those is safe. Anything else, a cut-off or unparseable body, a timeout on your side, an HTML `5xx` error page, a connection reset, may already have used your call: keep your previous copy and wait for your next scheduled run instead of retrying.
- **Only `GET` counts.** A browser's CORS preflight (`OPTIONS`) doesn't. `HEAD` and other methods get `405` and don't count either.
- **Don't rely on the clock, track your last call.** Store the time of your last served call for each region site and skip the call if it was less than 23.5 hours ago. Schedule in UTC: a local-time cron job gets a 23-hour day at the DST change, which is enough to trip the limit.
- **Use a generous client timeout, 60 to 120 seconds.** A short timeout on your side can cut the connection before the server finishes, and that counts against you as an "anything else" error above, not a safe-to-retry one.
- **While testing, don't open the URL twice.** Save the response to a file once and work from the file; every reload after the first is refused and counts toward a ban.

## Caching

Sends `Cache-Control: public, max-age=84600` (23.5 hours) and a strong `ETag`, so a standard HTTP cache won't ask again before your next call is allowed. On your next daily call, send the `ETag` back in `If-None-Match` to get `304 Not Modified` with no body when nothing changed. `generated_at` isn't part of the `ETag`. A `304` uses your call for that window, just like a `200`.

`ETag` and `Retry-After` are readable from browser JavaScript (`Access-Control-Expose-Headers`), for server-side tools and your own debugging, not so you can embed this call directly in a page your visitors load; see the warning above.

Responses are gzip-compressed.

## Errors

Errors are JSON: `{"error": "<code>"}`. A `429` also carries `retry_after`.

| Status | `error` | Meaning |
| --- | --- | --- |
| 404 | `zone_not_found` | The region is unknown, pending or turned off. |
| 405 | `method_not_allowed` | Only `GET` (and the `OPTIONS` preflight) are answered. |
| 429 | `rate_limited` | This region site was already fetched from your IP address in the last 23.5 hours. `Retry-After` and `retry_after` give the seconds left. Three of these within the window ban your IP address; see [Call limits](#call-limits). |
| 503 | `unavailable` | Temporary server problem. Try again later; it doesn't use your call. |
| 503 | `slow_down` | More than 30 calls in the last minute from your IP address, across all these APIs. `Retry-After` and `retry_after` give the seconds left. It doesn't use your call and never counts toward a ban. |

## Example

Run this once a day from a scheduled job on your own server, never in a loop and never from a browser. It tracks the last served call so an early rerun skips instead of risking a ban:

```python
import json, os, time, httpx

STATE = "meshmapper-state.json"
last = json.load(open(STATE)) if os.path.exists(STATE) else {}

url = "https://yow.meshmapper.net/get_channels.php"
if time.time() - last.get(url, 0) >= 23.5 * 3600:
    r = httpx.get(url, timeout=120)
    if r.status_code == 200:
        last[url] = time.time()
        json.dump(r.json(), open("yow-channels.json", "w"))
    # anything else: keep your previous copy, don't retry here
json.dump(last, open(STATE, "w"))
```
