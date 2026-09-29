# Scopes API

The Scopes API lists the Mesh Scopes a region's repeaters carry, with a repeater count per scope. Use it to show which scopes are active in a region without scraping the map. No key is needed.

```
GET https://yow.meshmapper.net/get_scopes.php
```

- On a **region** site: that region's own repeaters.
- On a **group** site (e.g. `pnw.meshmapper.net`): every enabled member region's repeaters, combined. A repeater carried by several members is counted once.

There are no parameters.

!!! note "Fair use"
    Public, cached for 5 minutes, and rate limited to 60 requests per minute per IP address. Cache the results, respect `ETag`, and don't poll more than once every few minutes. Accessing anything that isn't a published API, or scraping pages for data, is not allowed; see the warning on the [Coverage API](coverage-api.md) page.

## Response

```json
{
  "generated_at": "2026-09-27T16:58:49Z",
  "region": "YOW",
  "zones": ["YOW"],
  "repeaters": 5,
  "scoped": 3,
  "scopes": [
    { "name": "yow", "repeaters": 2, "default": 1, "monitored": true, "wardriving": true },
    { "name": "pnw", "repeaters": 1, "default": 0, "monitored": false, "wardriving": false },
    { "name": "mon", "repeaters": 0, "default": 0, "monitored": true, "wardriving": false }
  ]
}
```

### Top-level fields

| Field | Description |
| --- | --- |
| `generated_at` | When this answer was built. |
| `region` | The region code this page serves, uppercase. On a group site this is the group's own code. |
| `zones` | The region codes counted in this answer: one code on a region site, every enabled member on a group site. |
| `repeaters` | How many of this page's repeaters are enabled and public. This is the same population the map's Scope Finder tool checks, **not** the population MeshMapper's Scope Onboarding leaderboard uses: that board only counts repeaters inside the region's own drawn boundary, so a region with repeaters placed outside its boundary can show a different total there. |
| `scoped` | How many of those repeaters carry at least one Mesh Scope, by any evidence, or put a scope on their own adverts (even one MeshMapper can't name yet). A repeater whose only answer is `✱ Not set` doesn't count. |
| `scopes` | One entry per scope name seen on this page's repeaters, plus every name on the region's monitored list (see `monitored` below) or set as its Wardriving Scope, even at zero repeaters. Sorted by `repeaters` highest first, then by name. |

### Scope entry fields

| Field | Description |
| --- | --- |
| `name` | The scope name, as configured on the repeaters that carry it. |
| `repeaters` | How many of this page's repeaters carry this scope. |
| `default` | Of those, how many put this scope on their own adverts (as opposed to only being reported or observed carrying it). |
| `monitored` | `true` when MeshMapper is watching for this name right now: the region's Scopes to Monitor list, which automatically includes its Wardriving Scope and scopes its repeaters have reported (up to 48 names). |
| `wardriving` | `true` when this is a configured Wardriving Scope of this region (on a group site, of any member), the name it asks wardrivers' apps to use. |

Names and counts only. There is no per-repeater list, no repeater ID, and no key of any kind in this response.

## Caching

Sends `Cache-Control: public, max-age=300` and a strong `ETag`. Send the `ETag` back in `If-None-Match` to get `304 Not Modified` with no body when nothing changed. `generated_at` isn't part of the `ETag`. A `304` still counts against the rate limit.

Responses are gzip-compressed.

## Errors

Errors are JSON: `{"error": "<code>"}`.

| Status | `error` | Meaning |
| --- | --- | --- |
| 404 | `zone_not_found` | The region is unknown, pending or turned off. |
| 429 | `rate_limited` | Over 60 requests in a minute. Wait for the `Retry-After` header (seconds). |
| 503 | `unavailable` | Temporary server problem. Try again later. |

## Example

```python
import httpx

r = httpx.get("https://yow.meshmapper.net/get_scopes.php").json()
for s in r["scopes"]:
    print(s["name"], s["repeaters"], "of", r["repeaters"])
```
