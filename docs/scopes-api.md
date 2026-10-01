# Scopes API

The Scopes API lists the Mesh Scopes a region's repeaters carry, with a repeater count per scope. Use it to show which scopes are active in a region without scraping the map. No key is needed.

```
GET https://yow.meshmapper.net/get_scopes.php
```

- On a **region** site: that region's own repeaters.
- On a **group** site (e.g. `pnw.meshmapper.net`): every enabled member region's repeaters, combined. A repeater carried by several members is counted once.

There are no parameters.

!!! warning "One call per hour, or you're banned"
    Each region site's answer can be fetched **once every 55 minutes per IP address**. A second request to the same region site inside that window is refused with `429` **and bans your IP address from all of meshmapper.net for an hour**. Every repeat doubles the ban, up to a week. See [Call limits](#call-limits). Accessing anything that isn't a published API, or scraping pages for data, is not allowed; see the warning on the [Coverage API](coverage-api.md) page.

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

## Call limits

- **One call per region site every 55 minutes per IP address.** A group site counts as its own site, separate from its members.
- **A second call inside the window bans your IP address.** The request is refused with `429` and your IP address is banned from all of meshmapper.net (the map included, and every device behind that IP address) for 1 hour. Each repeat doubles the ban: 2 hours, 4 hours, 8 hours, up to a week.
- **Only a successful answer counts.** A `200` or a `304` uses your call. A `404` or `503` doesn't, so retrying after one of those is safe.
- **Only `GET` counts.** A browser's CORS preflight (`OPTIONS`) doesn't. `HEAD` and other methods get `405` and don't count either.
- **The window is 55 minutes, not 60**, so a scheduled job that runs once an hour always has room. A job that runs more often than hourly will get banned.
- **While testing, don't open the URL twice.** Save the response to a file once and work from the file.

## Caching

Sends `Cache-Control: public, max-age=3300` (55 minutes) and a strong `ETag`, so a standard HTTP cache won't ask again before your next call is allowed. On your next call, send the `ETag` back in `If-None-Match` to get `304 Not Modified` with no body when nothing changed. `generated_at` isn't part of the `ETag`. A `304` uses your call for that window, just like a `200`.

`ETag` and `Retry-After` are readable from browser JavaScript on other sites (`Access-Control-Expose-Headers`).

Responses are gzip-compressed.

## Errors

Errors are JSON: `{"error": "<code>"}`. A `429` also carries `retry_after`.

| Status | `error` | Meaning |
| --- | --- | --- |
| 404 | `zone_not_found` | The region is unknown, pending or turned off. |
| 405 | `method_not_allowed` | Only `GET` (and the `OPTIONS` preflight) are answered. |
| 429 | `rate_limited` | This region site was already fetched from your IP address in the last 55 minutes. `Retry-After` and `retry_after` give the seconds left. Your IP address is now banned; see [Call limits](#call-limits). |
| 503 | `unavailable` | Temporary server problem. Try again later; it doesn't use your call. |

## Example

Run this at most once an hour from a scheduled job, never in a loop:

```python
import httpx

r = httpx.get("https://yow.meshmapper.net/get_scopes.php").json()
for s in r["scopes"]:
    print(s["name"], s["repeaters"], "of", r["repeaters"])
```
