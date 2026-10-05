# Scopes API

The Scopes API lists the Mesh Scopes a region's repeaters carry, with a repeater count per scope. Use it to show which scopes are active in a region without scraping the map. Send your Coverage API key in the `X-API-Key` header.

```
GET https://yow.meshmapper.net/get_scopes.php
```

- On a **region** site: that region's own repeaters.
- On a **group** site (e.g. `pnw.meshmapper.net`): every enabled member region's repeaters, combined. A repeater carried by several members is counted once.

There are no parameters.

## Authentication

Send your existing **Coverage API key** in the `X-API-Key` header. No new key is needed. See [API keys and access](api-keys.md) for generation, group permissions, custom GLOBAL integrations and the v1.5.117 rollout.

Fetch from your backend and serve your own parsed data to visitors. Keep the key out of client-side JavaScript.

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
  'https://yow.meshmapper.net/get_scopes.php'
```

Schedule polling to fit your key budget, retain the last successful data on failure, and respect `Retry-After`.
