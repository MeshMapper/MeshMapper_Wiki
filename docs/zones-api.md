# Zones API

The Zones API lists MeshMapper regions and serves their boundaries as GeoJSON. Use it to show MeshMapper regions on your own map, link to them, or keep a local copy of their outlines. No key is needed.

Two endpoints work together:

1. **`get_zones.php`** on meshmapper.net lists the regions in one country, without boundaries.
2. **`get_geojson.php`** on each region's own site returns that region's boundary.

Call the first one, then fetch `url + "get_geojson.php"` for each region you want.

!!! note "Fair use"
    Both endpoints are public, cached for an hour, and rate limited to 60 requests per minute per IP address (shared between the two). Cache the results, respect `ETag`, and don't poll more than once an hour. Accessing anything that isn't a published API, or scraping pages for data, is not allowed; see the warning on the [Coverage API](coverage-api.md) page.

## List regions

```
GET https://meshmapper.net/get_zones.php?country=CA
```

| Parameter | Required | Description |
| --- | --- | --- |
| `country` | Yes | Two-letter country code (ISO 3166-1 alpha-2, e.g. `CA`, `US`, `GB`). Case doesn't matter. |

Only enabled regions are listed. Regions that are pending or turned off never appear.

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
| `code` | Region code, uppercase. Usually three letters, but can be 2 to 6 letters or digits. |
| `name` | Region name as MeshMapper stores it, including the country suffix. |
| `short_name` | `name` without the `, CC` country suffix. |
| `country` | Two-letter country code. |
| `lat`, `lon` | The region's center point. |
| `url` | The region's MeshMapper site. Append `get_geojson.php` for its boundary. |
| `has_boundary` | `true` when the region has a drawn boundary. When `false`, `get_geojson.php` returns the region with `geometry: null`. |
| `group` | The multi-region group this region belongs to (see [Multiregions](multiregions.md)), or `null`. |

### Group fields

`groups` lists each group that contains at least one of the listed regions. `members` is the group's full member list, which can include regions from other countries (`SEA` above).

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
- `center` is `[longitude, latitude]` too.

## Caching

Both endpoints send `Cache-Control: public, max-age=3600` and an `ETag`. To check for changes cheaply, send the `ETag` back in `If-None-Match`; you'll get `304 Not Modified` with no body if nothing changed. `generated_at` changes on every response and isn't part of the `ETag`.

## Errors

Errors are JSON: `{"error": "<code>"}`.

| Status | `error` | Meaning |
| --- | --- | --- |
| 400 | `country_required` | `get_zones.php` was called without `country`. |
| 400 | `invalid_country` | `country` isn't two letters. |
| 404 | `zone_not_found` | The region is unknown, pending or turned off. |
| 429 | `rate_limited` | Over 60 requests in a minute. Wait for the `Retry-After` header (seconds). |
| 503 | `unavailable` | Temporary server problem. Try again later. |

## Example

Fetch every Canadian region with a boundary into one GeoJSON file:

```python
import json, httpx

zones = httpx.get("https://meshmapper.net/get_zones.php", params={"country": "CA"}).json()
features = []
for z in zones["zones"]:
    if z["has_boundary"]:
        fc = httpx.get(z["url"] + "get_geojson.php").json()
        features.extend(fc["features"])
json.dump({"type": "FeatureCollection", "features": features}, open("meshmapper-ca.geojson", "w"))
```
