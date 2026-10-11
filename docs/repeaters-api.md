# Repeaters API

The Repeaters API lists every repeater a region knows about, with its position, status, the site details its administrators have filled in, and what MeshMapper has learned about it from the mesh. It is the same list the MeshMapper app reads. Use it to show a region's repeaters on your own map or keep a local copy of them.

```
GET https://yow.meshmapper.net/get_repeaters.php
```

- On a **region** site: that region's own repeaters.
- On a **group** site (e.g. `pnw.meshmapper.net`), or on any member of a group: every member region's repeaters, combined. A repeater held by several members appears once.

## Authentication

Send your **integration key** (formerly a Coverage key) in the `X-API-Key` header. An integration key only returns repeaters from the regions it is assigned to. See [API keys and access](api-keys.md) for generation, group permissions and the rollout.

During the transition the key is optional here: a request without one is still answered. That switch flips once app 1.4.1 is out and the update is forced, so send your key now.

Fetch from your backend and serve your own parsed data to visitors. Keep the key out of client-side JavaScript.

## Parameters

All optional.

| Parameter | Description |
| --- | --- |
| `f_freq`, `f_bw`, `f_sf` | Only repeaters heard on this radio preset, e.g. `f_freq=910.525&f_bw=62.5&f_sf=7`. All three are needed; a missing or malformed part means no filter (never an error). A repeater with no preset on record is unknown and always included. |

## Response

A JSON array, one object per repeater, sorted by `id`.

```json
[
  {
    "id": "A1",
    "hex_id": "A1B2C3D4E5F60718293A4B5C6D7E8F90A1B2C3D4E5F60718293A4B5C6D7E8F9",
    "name": "Gatineau Hills",
    "lat": 45.512345,
    "lon": -75.912345,
    "last_heard": 1791234567,
    "created_at": 1773103950,
    "enabled": 1,
    "iata": "YOW",
    "advert_bytes": 2,
    "hop_bytes": 2,
    "multibyte_capable": 1,
    "time_offset": 3,
    "power": "1W",
    "hardware": "RAK4631",
    "antenna": "5.8 dBi fibreglass",
    "height_m": 12,
    "height_asl_m": 341.6,
    "power_source": "solar",
    "site_notes": "On the fire tower, east face",
    "backbone": 1,
    "backbone_share": 0.084,
    "default_scope": "yow",
    "default_scope_state": "named",
    "default_scope_at": 1791230000,
    "default_scope_src": "advert",
    "admins": ["MrAlders0n"],
    "proven_neighbours": [
      { "key": "B7C8D9E0F1A2B3C4", "resolved": 0, "snr": 6.25, "heard_at": 1791230011 }
    ],
    "radios": [
      { "preset": "910.525,62.5,7", "last_seen": 1791234500, "witnesses": 4 }
    ],
    "preset_current": "910.525,62.5,7",
    "scopes": [
      { "scope": "yow", "observed_at": 1791200000, "observed_pkts": 37, "proof": "multibyte", "reported_at": 1791100000, "uploaded_at": null }
    ],
    "scopes_checked_at": 1791100000,
    "stale_repeater_hours": 24,
    "single_observer_mode": 0,
    "is_observer": 0,
    "is_carpeater": 0
  }
]
```

### Identity and position

| Field | Description |
| --- | --- |
| `id` | The repeater's short ID as the region shows it: the first 1, 2 or 3 bytes of its key, by its advert width. Two repeaters can share an `id`; use `hex_id` as the unique key. |
| `hex_id` | The repeater's public key, uppercase hex. Usually the full 64 characters; a few legacy rows hold a shorter prefix. |
| `name` | The name from its adverts, or the one an admin set. |
| `lat`, `lon` | Position in decimal degrees. `0, 0` means no position yet. |
| `iata` | The region code its latest advert came in on. |
| `created_at` | When MeshMapper first registered it, Unix seconds. |
| `last_heard` | When MeshMapper last heard its advert, Unix seconds. |

### Status

| Field | Description |
| --- | --- |
| `enabled` | `1` Active, `2` Ambiguous (it shares an ID with another nearby repeater, so pings through it can't be attributed and the map leaves them out; see [Duplicate Repeater IDs](duplicaterepeaterid.md)), `3` Inactive, `0` Disabled by an admin. |
| `stale_repeater_hours` | The region's own window for "stale": a repeater whose `last_heard` is older than this many hours is shown as stale on the map. |
| `single_observer_mode` | `1` when the region runs with a single observer, in which case the map never marks a repeater stale. |
| `time_offset` | The repeater's clock error in seconds when its last advert was heard: positive is behind, negative is ahead. `null` when unknown. |
| `is_observer` | `1` when this repeater is also an MQTT observer feeding MeshMapper. |
| `is_carpeater` | `1` when wardrivers have tagged it as a CARpeater, a repeater riding in a car. Its position moves, so treat it as mobile. |

### Site details

What the repeater's administrators have entered, in the region's admin panel or in [My MeshMapper](portal.md). Each one is `null` when nobody has filled it in. These keys only appear once a region has used the feature; a region that never has leaves them out entirely, so check for the key, not just the value.

| Field | Description |
| --- | --- |
| `power` | Transmit power, free text (up to 20 characters). This one is always present. |
| `hardware` | The board or device, free text (up to 80 characters). |
| `antenna` | The antenna, free text (up to 80 characters). |
| `height_m` | Height AGL: how high the antenna sits above the ground under it, in metres. |
| `height_asl_m` | Altitude ASL: the antenna's height above mean sea level, in metres. MeshMapper works it out as terrain height plus `height_m`, so it is present whenever `height_m` is. It's `null` until the terrain under the repeater has been looked up (usually within 15 minutes of a new height), and goes back to `null` for a while after the repeater moves. |
| `power_source` | `mains`, `solar`, `battery` or `poe`. |
| `site_notes` | A short public note about the site (up to 200 characters). |

Text fields are stored exactly as typed. Escape them before you put them in a web page.

### Width and routing

| Field | Description |
| --- | --- |
| `advert_bytes` | How many bytes of its key the repeater uses for path hops, from its own adverts: `1`, `2` or `3`. |
| `hop_bytes` | Old name for `advert_bytes`, kept for older readers. Use `advert_bytes`. |
| `multibyte_capable` | `1` once MeshMapper has seen this repeater forward 2-byte or wider paths. See [Multibyte](multibyte.md). |
| `backbone` | `1` when the region's [Backbone](backbone.md) view counts this repeater as part of the backbone. Absent until the region has been scored. |
| `backbone_share` | Its share of the region's routed traffic, `0` to `1`. Absent until the region has been scored. |

### Radio presets

| Field | Description |
| --- | --- |
| `radios` | Every preset this repeater has been heard on in the last 30 days, newest first: `preset` (`frequency,bandwidth,spreading factor`), `last_seen` (Unix seconds) and `witnesses` (how many independent sources heard it there, capped at 16). Empty when unknown. |
| `preset_current` | The preset MeshMapper thinks it is on now, or `null` when unknown. Use this rather than picking from `radios` yourself: it already handles a lone source that disagrees with everyone else. |

### Mesh Scopes

| Field | Description |
| --- | --- |
| `scopes` | Every scope the repeater has been confirmed carrying, sorted by name. Each entry has `scope`, plus when and how it was confirmed: `observed_at` / `observed_pkts` / `proof` (seen forwarding scoped traffic; `proof` is `multibyte` when a 2-byte or wider path proved it was this repeater, `floor` when the region's 1-byte paths are trusted for scopes), `reported_at` (an observer asked it) and `uploaded_at` (a wardriver's app asked it). A source that never confirmed it is `null`. Empty when nothing is known. |
| `scopes_checked_at` | When the repeater last answered a scope query, Unix seconds. Only present when it has been asked; an empty `scopes` with this key present means it answered with no scopes. |
| `default_scope` | The scope it puts on its own adverts, when known. |
| `default_scope_state` | `named` (the scope is known), `unknown` (it sets one but MeshMapper can't name it yet), or `none` (it sets none). |
| `default_scope_at` | When that was last updated, Unix seconds. |
| `default_scope_src` | Where it came from: `advert` or `reported`. |

The four `default_scope*` keys are absent on a region that has never recorded one. See the [Scopes API](scopes-api.md) for a per-scope summary of a region.

### Administrators and neighbours

| Field | Description |
| --- | --- |
| `admins` | Display names of the people who administer this repeater, from the MeshMapper app's repeater login. Names only, never a key. Empty when none. |
| `proven_neighbours` | The repeater's own neighbour table, as uploaded by one of its administrators from the app: `key` (the neighbour's key, or a 16-hex prefix when it didn't match a known repeater), `resolved` (`1` when `key` is a known repeater's full key), `snr` (dB) and `heard_at` (Unix seconds). Empty when none. |

Fields may be added over time. Ignore any you don't recognise.

## Call limits

With an integration key, these reads use the key's shared read budget, normally **1,000 requests per UTC day and 30 per fixed minute**. Every admitted request counts. See [limits and caching](api-keys.md#limits-and-caching).

Separately, each IP address may make **300 requests per minute**. Past that you get `429 rate_limited` with `Retry-After: 60`.

Responses support gzip compression. A group with thousands of repeaters is a multi-megabyte answer, so always ask for it.

## Errors

Authentication, permissions and quota errors are listed in [Read API errors](api-keys.md#read-api-errors).

| Status | Error | Meaning |
| --- | --- | --- |
| 429 | `rate_limited` | Over 300 requests a minute from your IP; wait for `Retry-After`. |
| 503 | `unavailable` | Temporary data problem; keep your previous copy and retry later. |

A region that is unknown, pending or disabled returns an empty array.

## Example

With `MESHMAPPER_API_KEY` set in your backend environment:

```bash
curl --fail-with-body --compressed \
  -H "X-API-Key: $MESHMAPPER_API_KEY" \
  'https://yow.meshmapper.net/get_repeaters.php'
```

Only repeaters on one preset:

```bash
curl --fail-with-body --compressed \
  -H "X-API-Key: $MESHMAPPER_API_KEY" \
  'https://yow.meshmapper.net/get_repeaters.php?f_freq=910.525&f_bw=62.5&f_sf=7'
```

Schedule polling to fit your key budget, keep the last good copy on failure, and respect `Retry-After`.
