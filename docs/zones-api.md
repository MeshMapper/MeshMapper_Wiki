# Zones API

The Zones API lists MeshMapper regions and serves their boundaries as GeoJSON. Use it to show MeshMapper regions on your own map, link to them, or keep a local copy of their outlines. No key is needed.

Two endpoints work together:

1. **`get_zones.php`** on meshmapper.net lists the regions in one country, without boundaries.
2. **`get_geojson.php`** on each region's own site returns that region's boundary.

Call the first one, then fetch `url + "get_geojson.php"` for each region you want.

!!! warning "One call per day, or you're banned"
    Each answer can be fetched **once every 23.5 hours per IP address**: `get_zones.php` once per country, and `get_geojson.php` once per region site. A second request for the same country or region inside that window is refused with `429` **and bans your IP address from all of meshmapper.net for a day**. Every repeat doubles the ban, up to 30 days. See [Call limits](#call-limits). Accessing anything that isn't a published API, or scraping pages for data, is not allowed; see the warning on the [Coverage API](coverage-api.md) page.

!!! warning "Call this from your server, not your visitors' browsers"
    Fetch this API from your own backend, store the result, and serve your own copy to visitors. Don't call it from client-side JavaScript in a visitor's browser: everyone behind the same home router or mobile carrier shares one public IP address, so one visitor's fetch uses the call and the next visitor's fetch bans that whole IP address from all of meshmapper.net, including every MeshMapper app user on that network.

## List regions

```
GET https://meshmapper.net/get_zones.php?country=CA
```

| Parameter | Required | Description |
| --- | --- | --- |
| `country` | Yes | Two-letter country code (ISO 3166-1 alpha-2, e.g. `CA`, `US`, `GB`). Case doesn't matter. |

Only enabled regions are listed. Regions that are pending or turned off never appear. A well-formed `country` with no regions returns 200 with `count: 0` and empty `zones` and `groups` arrays.

### Response

```json
{
  "generated_at": "2026-09-25T15:00:00Z",
  "country": "CA",
  "count": 3,
  "zones": [
    { "code": "YOW", "name": "Ottawa, CA", "short_name": "Ottawa", "country": "CA",
      "lat": 45.4215, "lon": -75.6972, "url": "https://yow.meshmapper.net/",
      "has_boundary": true, "group": null },
    { "code": "YVR", "name": "Vancouver, CA", "short_name": "Vancouver", "country": "CA",
      "lat": 49.2827, "lon": -123.1207, "url": "https://yvr.meshmapper.net/",
      "has_boundary": true, "group": "PNW" },
    { "code": "YQB", "name": "Quebec City, CA", "short_name": "Quebec City", "country": "CA",
      "lat": 46.8139, "lon": -71.208, "url": "https://yqb.meshmapper.net/",
      "has_boundary": false, "group": null }
  ],
  "groups": [
    { "code": "PNW", "name": "Pacific Northwest", "members": ["SEA", "YVR"],
      "url": "https://pnw.meshmapper.net/" }
  ]
}
```

### Zone fields

| Field | Description |
| --- | --- |
| `code` | Region code, uppercase, three letters or digits (e.g. `YOW`). |
| `name` | Region name as MeshMapper stores it, including the country suffix. |
| `short_name` | `name` without the `, CC` country suffix. |
| `country` | Two-letter country code. |
| `lat`, `lon` | The region's center point. |
| `url` | The region's MeshMapper site. Append `get_geojson.php` for its boundary. |
| `has_boundary` | `true` when a boundary is stored for the region. When `false`, `get_geojson.php` returns the region with `geometry: null`. In rare cases a stored boundary can't be used, so `get_geojson.php` may still return `geometry: null` when this is `true`. |
| `group` | The first enabled group (lowest id) this region belongs to (see [Multiregions](multiregions.md)), or `null`. A region in several groups shows only one. |

### Group fields

`groups` lists the group shown in each listed region's `group` field. `members` is that group's enabled member list, which can include regions from other countries (`SEA` above).

| Field | Description |
| --- | --- |
| `code` | Group code, uppercase. |
| `name` | Group name. |
| `members` | Region codes in the group. |
| `url` | The group's MeshMapper site. Its `get_geojson.php` returns every member. |

## Region boundary

```
GET https://yow.meshmapper.net/get_geojson.php
```

Returns a GeoJSON `FeatureCollection` ([RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946)):

- On a **region** site: one Feature, for that region.
- On a **group** site (e.g. `pnw.meshmapper.net`): one Feature per member region.

```json
{
  "type": "FeatureCollection",
  "generated_at": "2026-09-25T15:00:00Z",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [-75.912345, 45.201234], [-75.401234, 45.198765],
          [-75.398765, 45.612345], [-75.912345, 45.201234]
        ]]
      },
      "properties": {
        "code": "YOW", "name": "Ottawa, CA", "short_name": "Ottawa", "country": "CA",
        "center": [-75.6972, 45.4215], "radius_km": 42, "has_boundary": true,
        "url": "https://yow.meshmapper.net/"
      }
    }
  ]
}
```

- Coordinates are `[longitude, latitude]`, as GeoJSON requires, rounded to 6 decimals (about 10 cm). The outline is never simplified.
- The geometry is always a single `Polygon`.
- A region with no drawn boundary has `"geometry": null` and `has_boundary: false`. MeshMapper doesn't draw a circle in its place, but `center` and `radius_km` are there if you want one.
- `center` is `[longitude, latitude]` too. `radius_km` can be `null`.
- If the server hits a problem mid-stream, the JSON is deliberately left unclosed, so you get a truncated, unparseable body, not a clean JSON error. A parse error does **not** by itself mean your call was handed back; see [Call limits](#call-limits) for exactly which errors are safe to retry.

## Call limits

- **One call per target every 23.5 hours per IP address.** For `get_zones.php` the target is the country (`?country=CA` and `?country=US` are separate calls). For `get_geojson.php` it's the region site, and a group site counts as its own site, separate from its members. Fetching every region of a country in one run is fine: each region is its own call.
- **A second call for the same target inside the window bans your IP address.** The request is refused with `429` and your IP address is banned from all of meshmapper.net (the map included, and every device behind that IP address) for 1 day. Each repeat doubles the ban: 2 days, 4 days, 8 days, up to 30 days.
- **Only certain JSON errors hand your call back.** A `400` (missing or bad `country` on `get_zones.php`), a `404` `zone_not_found`, or a `503` `unavailable` doesn't use your call, so retrying after one of those is safe. Anything else, a cut-off or unparseable body, a timeout on your side, an HTML `5xx` error page, a connection reset, may already have used your call: keep your previous copy and wait for your next scheduled run instead of retrying.
- **Only `GET` counts.** A browser's CORS preflight (`OPTIONS`) doesn't. `HEAD` and other methods get `405` and don't count either.
- **Don't rely on the clock, track your last call.** Store the time of your last served call for each target (country or region) and skip the call if it was less than 23.5 hours ago. Schedule in UTC: a local-time cron job gets a 23-hour day at the DST change, which is enough to trip the limit.
- **Use a generous client timeout, 60 to 120 seconds.** A short timeout on your side can cut the connection before the server finishes, and that counts against you as an "anything else" error above, not a safe-to-retry one.
- **While testing, don't open a URL twice.** Save the response to a file once and work from the file.

## Caching

Both endpoints send `Cache-Control: public, max-age=84600` (23.5 hours) and an `ETag`, so a standard HTTP cache won't ask again before your next call is allowed. On your next daily call, send the `ETag` back in `If-None-Match`; you'll get `304 Not Modified` with no body if nothing changed. `generated_at` changes on every response and isn't part of the `ETag`. A `304` uses your call for that window, just like a `200`.

`ETag` and `Retry-After` are readable from browser JavaScript (`Access-Control-Expose-Headers`), for server-side tools and your own debugging, not so you can embed this call directly in a page your visitors load; see the warning above.

Responses are gzip-compressed.

## Errors

Errors are JSON: `{"error": "<code>"}`. A `429` also carries `retry_after`.

| Status | `error` | Meaning |
| --- | --- | --- |
| 400 | `country_required` | `get_zones.php` was called without `country`. |
| 400 | `invalid_country` | `country` isn't two letters. |
| 404 | `zone_not_found` | The region is unknown, pending or turned off. |
| 405 | `method_not_allowed` | Only `GET` (and the `OPTIONS` preflight) are answered. |
| 429 | `rate_limited` | This country or region was already fetched from your IP address in the last 23.5 hours. `Retry-After` and `retry_after` give the seconds left. Your IP address is now banned; see [Call limits](#call-limits). |
| 503 | `unavailable` | Temporary server problem. Try again later; it doesn't use your call. |

## Example

Run this from a scheduled job on your own server, never in a loop and never from a browser. It fetches every Canadian region with a boundary into one GeoJSON file (one call to `get_zones.php`, then one call per region), tracking the last served call per URL so an early rerun skips instead of risking a ban:

```python
import json, os, time, httpx

STATE = "meshmapper-state.json"
last = json.load(open(STATE)) if os.path.exists(STATE) else {}

def fetch(url, **params):
    if time.time() - last.get(url, 0) < 23.5 * 3600:
        return None                      # already used this call recently
    r = httpx.get(url, params=params, timeout=120)
    if r.status_code != 200:
        return None                      # keep the previous copy, don't retry here
    last[url] = time.time()
    return r.json()

zones = fetch("https://meshmapper.net/get_zones.php", country="CA")
features = []
if zones:
    for z in zones["zones"]:
        if z["has_boundary"]:
            fc = fetch(z["url"] + "get_geojson.php")
            if fc:
                features.extend(fc["features"])
    json.dump({"type": "FeatureCollection", "features": features}, open("meshmapper-ca.geojson", "w"))
json.dump(last, open(STATE, "w"))
```
