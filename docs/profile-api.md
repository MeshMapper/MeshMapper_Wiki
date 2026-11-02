# Profile API

The Profile API returns one companion's profile: the same data the profile card on the site shows. Send a [personal API key](personal-api-keys.md) or an [integration key](api-keys.md) in the `X-API-Key` header.

```
GET https://meshmapper.net/get_profile.php?hex_id=<hex>
```

| Parameter | Description |
| --- | --- |
| `hex_id` | The companion's public key. The full 64 hex characters is best. A shorter prefix also works (at least 4 hex characters; 6 or more is better), but it can match several companions; see `candidates` below. A `hex` from the [Leaderboard API](leaderboard-api.md) always works. |

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
  "regions": "SWE,STO,HB",
  "primary_region": "SWE",
  "user_group_name": "louie",
  "all_time_points": 18342,
  "weekly_points": 412,
  "grid_squares": 2210,
  "pioneer_squares": 845,
  "unattributed_points": 0,
  "region_points": [
    {"region": "SWE", "all_time_points": 18338, "weekly_points": 410, "grid_squares": 2209,
     "pioneer_squares": 844, "generated_at": 1761955200,
     "zones": [{"region": "STO", "all_time_points": 16120, "weekly_points": 380, "grid_squares": 1950,
                "pioneer_squares": 760, "generated_at": 1761917580}]},
    {"region": "HB", "all_time_points": 4, "weekly_points": 2, "grid_squares": 1,
     "pioneer_squares": 1, "generated_at": 1761938520, "zones": []}
  ],
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
| `region_points` | One line per region board this companion (or account) is on, highest `all_time_points` first. Each line has the board's `region`, `all_time_points`, `weekly_points`, `grid_squares`, `pioneer_squares`, its `generated_at`, and `zones`. See [Matching the leaderboard](#matching-the-leaderboard). Missing on older data. |
| `first_seen`, `last_heard` | Unix timestamps in seconds, or `null`. |
| `awards` | The companion's awards. |
| `candidates` | When a short hex matched several companions: each one's `hex_id` and `name`. Ask again with the full hex. |

## Matching the leaderboard

The profile's numbers come from the region leaderboards as they stand right now, so the two APIs agree when you pull both.

- Each `region_points` line equals this companion's row in [`get_leaderboard.php?region=<region>`](leaderboard-api.md), and its `generated_at` equals that response's `generated_at`. A superregion counts as one board.
- `all_time_points`, `weekly_points`, `grid_squares` and `pioneer_squares` at the top are the sum of the lines. If you drive in several regions, the total matches no single board (in the example, SWE 18,338 + HB 4 = 18,342). That's expected.
- `zones` lists a superregion's member regions, each matching that member's own board. They're already inside the superregion's line, so they aren't added to the total.

Each board updates about once a day, so the numbers follow the boards and asking more than once an hour gains nothing. After you link or unlink a radio, its points move onto or off your account the next time each board updates, which can take up to 24 hours.

## Errors

A companion that can't be found is answered with HTTP 200 and an `error` field, as the site's own profile card expects:

| Body | Meaning |
| --- | --- |
| `{"error": "Companion not found"}` | No companion matches that hex. |
| `{"error": "Missing hex_id parameter"}` | Add `hex_id`. |

A companion on its first day may be on a board before its profile is built. Ask with its full 64-character hex to find it; a shorter prefix won't match it until the next day.

Key and limit errors (401, 403, 503) are listed on [Personal API keys](personal-api-keys.md#errors) and [API keys and access](api-keys.md#read-api-errors).
