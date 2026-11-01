# Profile API

The Profile API returns one companion's profile: the same data the profile card on the site shows. Send a [personal API key](personal-api-keys.md) or an [integration key](api-keys.md) in the `X-API-Key` header.

```
GET https://meshmapper.net/get_profile.php?hex_id=<hex>
```

| Parameter | Description |
| --- | --- |
| `hex_id` | The companion's public key. The full 64 hex characters is best. A shorter prefix (at least 6 characters) also works, but it can match several companions; see `candidates` below. A `hex` from the [Leaderboard API](leaderboard-api.md) always works. |

Profiles work for any companion, wherever it wardrives.

## Response

```json
{
  "hex_id": "077F959F...",
  "orphaned": false,
  "name": "louie",
  "avatar_path": null,
  "avatar_url": "https://cdn.discordapp.com/avatars/...",
  "bio": null,
  "regions": "SWE,STO",
  "primary_region": "SWE",
  "user_group_name": "louie",
  "all_time_points": 18342,
  "weekly_points": 412,
  "grid_squares": 2210,
  "pioneer_squares": 845,
  "unattributed_points": 0,
  "first_seen": 1754000000,
  "last_heard": 1761950000,
  "awards": [],
  "candidates": []
}
```

| Field | Description |
| --- | --- |
| `hex_id` | The companion this profile belongs to. For a portal account it can differ from the hex you asked for. |
| `orphaned` | `true` when no contact backs this device any more. The site shows these without a name. |
| `name` | Display name: the portal account's display name for a linked device, otherwise the companion's name. |
| `avatar_url` | The avatar to show, or `null`. `avatar_path` is the older relative form. |
| `bio` | The profile bio, or `null`. |
| `regions`, `primary_region` | Regions the companion has points in (comma separated), and the main one. |
| `user_group_name` | The name the account's devices are grouped under. |
| `all_time_points`, `weekly_points` | Points, all time and over the last 7 days. For a portal account these cover all its linked devices. |
| `grid_squares` | Squares travelled (the Explorers board). |
| `pioneer_squares` | Squares this companion pinged first (the Pioneers board). |
| `unattributed_points` | Part of the account's points earned with no radio key attached. |
| `first_seen`, `last_heard` | Unix timestamps in seconds, or `null`. |
| `awards` | The companion's awards. |
| `candidates` | When a short hex matched several companions: each one's `hex_id` and `name`. Ask again with the full hex. |

Points are rebuilt about once a day, so there's no need to ask more than once an hour.

## Errors

A companion that can't be found is answered with HTTP 200 and an `error` field, as the site's own profile card expects:

| Body | Meaning |
| --- | --- |
| `{"error": "Companion not found"}` | No companion matches that hex. |
| `{"error": "Missing hex_id parameter"}` | Add `hex_id`. |

Key and limit errors (401, 403, 503) are listed on [Personal API keys](personal-api-keys.md#errors) and [API keys and access](api-keys.md#read-api-errors).
