# Coverage API

The Coverage API provides programmatic access to MeshMapper coverage grid-square data. Use it to draw coverage grids on your own maps or integrate MeshMapper data into external tools and dashboards.

## Authentication

Access requires a **Coverage** API key. Each key is scoped to a specific region or multiregion group and has a daily rate limit of 100 requests.

### Generating a Key

Regional administrators can generate their own API key directly from the admin panel:

1. Log in to your region's admin panel
2. Go to **User Settings**
3. Scroll to the **API Access** section
4. Enter a description/reason for the key (mandatory)
5. Click **Generate API Key**

Each administrator is limited to **one API key per region**. The key is automatically scoped to your region with a fixed rate limit of 100 requests per day. If you need to replace your key, use the **Regenerate** button — this invalidates the old key immediately.

!!! warning "Unauthorized Access"
    MeshMapper utilizes API keys and rate limits to protect server resources and prevent access to data that regions do not wish to have shared externally.  As such, accessing unauthorized API's, scraping for data, etc., is strictly prohibited and will result in action taken to protect the server and data (which may include IP or origin bans, removal of a region, etc.).  The MeshMapper team is happy to review requests for data not provided in the API's below.

## Endpoint

```
GET https://meshmapper.net/coverage.php?key=YOUR_API_KEY
```

### Query Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `key` | Yes | Your Coverage API key. |
| `include` | No | Comma-separated list of optional sections to add to the response. Currently supports `repeaters` (e.g. `?include=repeaters`) — see [Repeater Fields](#repeater-fields). |

## Response Format

```json
{
  "success": true,
  "region": "[IATA]",
  "region_name": "Ottawa, CA",
  "grid_size": { "lat": 0.0027, "lon": 0.00384 },
  "schema_version": 2,
  "generated_at": 1710547200,
  "data_age_seconds": 312,
  "total_squares": 1234,
  "point_count": 48210,
  "coverage_type_counts": { "BIDIR": 540, "TX": 60, "RX": 410, "DISC": 90, "DEAD": 12, "DROP": 122 },
  "type_bits": { "BIDIR": 1, "TX": 2, "RX": 4, "DISC": 8, "DEAD": 16, "DROP": 32 },
  "bbox": { "minLat": 45.108, "minLon": -76.351, "maxLat": 45.621, "maxLon": -75.299 },
  "grid_squares": [
    {
      "grid_id": "16816_-19718",
      "bounds": {
        "south": 45.4032,
        "west": -75.7177,
        "north": 45.4059,
        "east": -75.7138
      },
      "coverage_type": "BIDIR",
      "fill_color": "#1e7e34",
      "border_color": "#14522d",
      "snr": 8.5,
      "timestamp": 1710547200,
      "count": 14,
      "snr_min": -2.1,
      "snr_max": 11.3,
      "status_mask": 37,
      "first_seen": 1710201600,
      "noise": 17.4,
      "effective": 2.43
    }
  ]
}
```

!!! info "Backward compatibility"
    The fields documented here are **additive** — every field present in earlier versions of the API (`grid_id`, `bounds`, `coverage_type`, `fill_color`, `border_color`, `snr`, `timestamp`, and the original top-level fields) is unchanged. Existing integrations continue to work without modification; simply ignore any fields you do not need.

## Field Reference

### Top-Level Fields

| Field | Type | Description |
| --- | --- | --- |
| `success` | boolean | `true` if the request succeeded. |
| `region` | string | The region or group code this key is scoped to. |
| `region_name` | string | Human-readable name of the region (falls back to the code for groups). |
| `grid_size` | object | Grid square dimensions in degrees (`lat` and `lon`). |
| `schema_version` | integer | Response schema version. New fields are added without breaking the existing contract. |
| `generated_at` | integer | Unix timestamp of when this response was built (see [Caching](#http-caching-and-compression)). |
| `data_age_seconds` | integer or null | Seconds between the most recent ping in the dataset and when the response was built — a freshness indicator. `null` if the region has no data. |
| `total_squares` | integer | Number of grid squares returned. |
| `point_count` | integer | Total number of pings aggregated across all grid squares. |
| `coverage_type_counts` | object | Number of grid squares per dominant `coverage_type`. |
| `type_bits` | object | Legend mapping each coverage type to the bit value used in a square's `status_mask`. |
| `bbox` | object or null | Bounding box covering all returned squares (`minLat`, `minLon`, `maxLat`, `maxLon`). `null` if empty. |
| `grid_squares` | array | Array of grid square objects (see below). |
| `repeaters` | array | Only present when `?include=repeaters` is set — see [Repeater Fields](#repeater-fields). |

### Grid Square Fields

| Field | Type | Description |
| --- | --- | --- |
| `grid_id` | string | Unique identifier for the grid cell in `"latIndex_lonIndex"` format. |
| `bounds` | object | Bounding box with `south`, `west`, `north`, `east` in decimal degrees. |
| `coverage_type` | string | Dominant type for the cell. One of: `BIDIR`, `TX`, `RX`, `DISC`, `DEAD`, `DROP`. |
| `fill_color` | string | Hex fill colour matching MeshMapper's map rendering. |
| `border_color` | string | Hex border colour matching MeshMapper's map rendering. |
| `snr` | float or null | Average signal-to-noise ratio (dB) across the cell's pings, if available. |
| `timestamp` | integer or null | Unix timestamp of the dominant (most recent, highest-priority) ping colouring this square. |
| `count` | integer | Number of pings aggregated into this cell — a confidence/density indicator. |
| `snr_min` | float or null | Lowest SNR (dB) among the cell's pings. |
| `snr_max` | float or null | Highest SNR (dB) among the cell's pings. |
| `status_mask` | integer | Bitmask of **all** coverage types present in the cell (OR of `type_bits`). See [Cell Quality and Status Mask](#cell-quality-and-status-mask). |
| `first_seen` | integer or null | Unix timestamp of the **oldest** ping in the cell (`timestamp` is the newest/dominant). |
| `noise` | float or null | Average noise level (dB above the receiver's noise floor) across the cell's pings. |
| `effective` | float | Average coverage-quality score for the cell, `0`–`3` (see below). |

### Repeater Fields

Returned in the top-level `repeaters` array **only** when the request includes `?include=repeaters`. Each entry describes a repeater known to the region:

| Field | Type | Description |
| --- | --- | --- |
| `hex` | string | Repeater hex ID (prefix). |
| `name` | string or null | Repeater name. |
| `lat` | float or null | Latitude. |
| `lon` | float or null | Longitude. |
| `last_heard` | integer or null | Unix timestamp the repeater was last heard. |
| `enabled` | integer | `1` = active, `2` = flagged for an ID collision (still listed). |
| `advert_bytes` | integer or null | Advertised path-ID width in bytes. |

## Coverage Types

Each grid square's `coverage_type` is the **dominant** ping in that square — when multiple pings exist, the highest-priority type wins.

| Type | Colour | Priority | Description |
| --- | --- | --- | --- |
| `BIDIR` | Green (`#1e7e34`) | 6 | Two-way confirmed link. |
| `DISC` | Cyan (`#17a2b8`) | 5 | Discovery or trace packet. |
| `TX` | Orange (`#fd7e14`) | 4 | Transmitted but not heard back. |
| `RX` | Purple (`#6f42c1`) | 3 | Heard traffic, without transmitting. |
| `DEAD` | Grey (`#6c757d`) | 2 | Repeater heard but no route. |
| `DROP` | Red (`#bd2130`) | 1 | No connection. |

## Cell Quality and Status Mask

`coverage_type` reflects only the single dominant ping in a square. The `effective` and `status_mask` fields summarise the **whole mix** of pings in the cell.

### `effective` — average quality (0–3)

`effective` is the mean, over every ping in the cell, of a per-ping quality score:

| Ping type | Score |
| --- | --- |
| `BIDIR` | 3 |
| `TX`, `RX`, `DISC` | 2 |
| `DEAD` | 1 |
| `DROP` | 0 |

A cell that is entirely `BIDIR` scores `3.0`; a cell that is mostly `BIDIR` with some failed pings scores lower. This makes `effective` ideal for a smooth red→green quality gradient, where `coverage_type` alone would only show the single best ping.

### `status_mask` — which types are present

`status_mask` is a bitwise-OR of the `type_bits` for every type that appears anywhere in the cell. Use the top-level `type_bits` legend to decode it:

```text
BIDIR=1  TX=2  RX=4  DISC=8  DEAD=16  DROP=32

status_mask = 37  →  1 (BIDIR) + 4 (RX) + 32 (DROP)
              i.e. the cell contains BIDIR, RX, and DROP pings.
```

## Drawing Grid Squares

Each grid square can be reconstructed as a rectangle using the `bounds` object:

```javascript
// Leaflet.js example
data.grid_squares.forEach(sq => {
    L.rectangle(
        [[sq.bounds.south, sq.bounds.west], [sq.bounds.north, sq.bounds.east]],
        {
            fillColor: sq.fill_color,
            color: sq.border_color,
            fillOpacity: 0.6,
            weight: 1
        }
    ).addTo(map);
});
```

The grid uses fixed cell sizes of **0.0027 degrees latitude** by **0.00384 degrees longitude** (approximately 300m squares). These match MeshMapper's Simplified Mode rendering.

## HTTP Caching and Compression

The API is built for efficient, low-frequency polling. Coverage data does not change second-to-second, so please poll sparingly.

- **Compression.** Responses are gzip-compressed. Send `Accept-Encoding: gzip` (most HTTP clients do this automatically) to receive compressed data — payloads are roughly 9× smaller.
- **Server-side cache.** Responses carry `Cache-Control: public, max-age=900` and are cached for up to **15 minutes**. Polling more often than that returns identical data (and still counts toward your daily limit), so a poll interval of **15 minutes or longer is recommended**. `generated_at` tells you when the cached data was built.
- **Conditional requests.** Each response includes an `ETag` (and `Last-Modified`). Send the `ETag` value back in an `If-None-Match` header; if nothing has changed since, you'll get a **`304 Not Modified`** with an empty body, saving you the download.

```bash
# First request — note the ETag header
curl -s --compressed -D - "https://meshmapper.net/coverage.php?key=YOUR_API_KEY" -o coverage.json

# Later — only download if the data changed
curl -s --compressed -H 'If-None-Match: "THE_ETAG_VALUE"' \
     "https://meshmapper.net/coverage.php?key=YOUR_API_KEY"
```

## Rate Limits

Each API key has a **daily** request limit (100 requests). Counters reset daily. Every request that reaches your data — including cache hits and `304 Not Modified` responses — counts toward this limit.

When you exceed your limit, the API returns HTTP 429:

```json
{
  "success": false,
  "error": "rate_limit_exceeded",
  "message": "Daily request limit reached",
  "limit": 100,
  "used": 100,
  "resets_in_hours": 12.5
}
```

A separate short-term, per-IP throttle protects against bursts; exceeding it also returns HTTP 429 (with `error: rate_limited`). Spacing requests out (see [Caching](#http-caching-and-compression)) avoids both.

## Error Responses

| HTTP Code | Error | Description |
| --- | --- | --- |
| 400 | `missing_key` | No API key provided. |
| 400 | `invalid_region` | Region code on key not found. |
| 401 | `invalid_key` | API key not found. |
| 403 | `no_region` | No region assigned to this key. |
| 429 | `rate_limit_exceeded` | Daily request limit reached. |
| 429 | `rate_limited` | Too many requests in a short period (per-IP throttle). |
| 500 | `server_error` | Internal error (database not found, etc.). |

## Managing Your Key

If you have a Coverage API key assigned to your admin account, you can view your current usage and regenerate your key from the **User Settings** tab in your region's Admin Portal. Regenerating a key invalidates the old one immediately.

## Global Coverage Feed

A special **global** Coverage key returns data for **every MeshMapper region in one request** — no region list to maintain on your side. Global keys are not self-service: they are issued by the MeshMapper team on request, for integrations that genuinely need fleet-wide data (reach out via the usual channels if that's you).

The endpoint and authentication are identical — only the key differs:

```
GET https://meshmapper.net/coverage.php?key=YOUR_GLOBAL_KEY
```

### Response Format

Instead of a single region's payload, a global key returns an envelope containing one section per region. Each section carries the **same fields as a regional response** (`region`, `region_name`, `data_age_seconds`, `total_squares`, `point_count`, `coverage_type_counts`, `bbox`, `grid_squares`, and `repeaters` when requested); `grid_size` and `type_bits` appear once at the top level since they are identical for every region.

```json
{
  "success": true,
  "global": true,
  "schema_version": 2,
  "generated_at": 1710547200,
  "grid_size": { "lat": 0.0027, "lon": 0.00384 },
  "type_bits": { "BIDIR": 1, "TX": 2, "RX": 4, "DISC": 8, "DEAD": 16, "DROP": 32 },
  "regions": [
    {
      "region": "YOW",
      "region_name": "Ottawa, CA",
      "data_age_seconds": 312,
      "total_squares": 1234,
      "point_count": 48210,
      "coverage_type_counts": { "BIDIR": 540, "TX": 60, "RX": 410, "DISC": 90, "DEAD": 12, "DROP": 122 },
      "bbox": { "minLat": 45.108, "minLon": -76.351, "maxLat": 45.621, "maxLon": -75.299 },
      "grid_squares": [ "…same grid square objects as the regional API…" ]
    }
  ],
  "region_count": 214,
  "regions_skipped": 249
}
```

| Field | Type | Description |
| --- | --- | --- |
| `global` | boolean | Always `true` for a global-key response. |
| `regions` | array | One section per region with coverage data, in region-code order. |
| `region_count` | integer | Number of sections in `regions`. Note this field arrives **after** the `regions` array — use a standard JSON parser rather than assuming key order. |
| `regions_skipped` | integer | Regions omitted because they have no coverage data yet. |

`?include=repeaters` works exactly as for regional keys, adding a `repeaters` array to each section.

### Caching and Timeouts

The global response aggregates the entire fleet, so it is cached more aggressively than regional responses:

- The server cache lasts **6 hours** (`Cache-Control: public, max-age=21600`). Polling more often returns identical data; **once or twice a day is the intended usage**.
- A request that arrives after the cache has expired triggers a rebuild. The response **streams region-by-region while it builds** — data starts flowing immediately, but the complete download can take a minute. Configure a generous *total* timeout in your HTTP client (the connection is never idle, so per-read timeouts are fine at their defaults). All other requests are served instantly from cache.
- `ETag` / `If-None-Match` conditional requests work exactly as for regional keys, and a `304 Not Modified` is by far the cheapest way to poll.

### Differences from Regional Keys

| Behaviour | Result |
| --- | --- |
| `fresh=1` | HTTP 400, `fresh_not_supported` — global rebuilds are cache-driven only. |
| `f_*` filter parameters | HTTP 400, `filters_not_supported`. |
| Rebuild already in progress elsewhere | Served the previous cached copy; if no cached copy exists yet, HTTP 503 with `error: rebuilding` and a `Retry-After` header — retry after the indicated delay. |
