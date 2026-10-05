# Zones API

The Zones API lists MeshMapper regions and serves their boundaries as GeoJSON. Use it to show MeshMapper regions on your own map, link to them, or keep a local copy of their outlines. Send your Coverage API key in the `X-API-Key` header.

Two endpoints work together:

1. **`get_zones.php`** on meshmapper.net lists the regions in one country, without boundaries.
2. **`get_geojson.php`** on each region's own site returns that region's boundary.

Call the first one, then fetch `url + "get_geojson.php"` for each region you want.

## Authentication

Send your existing **Coverage API key** in the `X-API-Key` header. No new key is needed. See [API keys and access](api-keys.md) for generation, group permissions, custom GLOBAL integrations and the v1.5.117 rollout.

Fetch from your backend and serve your own parsed data to visitors. Keep the key out of client-side JavaScript.

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

The directory also returns `400 country_required` or `400 invalid_country` for a missing or malformed country. Results include only regions authorized by your key; group member lists are filtered to the same access scope. The sample above illustrates a key authorized for all listed regions. A group boundary request requires access to every enabled member.

## Example

With `MESHMAPPER_API_KEY` set in your backend environment:

```bash
curl --fail-with-body --compressed \
  -H "X-API-Key: $MESHMAPPER_API_KEY" \
  'https://meshmapper.net/get_zones.php?country=CA'
```

Schedule polling to fit your key budget, retain the last successful data on failure, and respect `Retry-After`.
