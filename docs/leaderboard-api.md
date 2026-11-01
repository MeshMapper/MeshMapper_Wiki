# Leaderboard API

The Leaderboard API returns a region's or superregion's leaderboards as JSON: the top 10 of each of the six people boards the [leaderboard page](leaderboards.md) shows. Send a [personal API key](personal-api-keys.md) or an [integration key](api-keys.md) in the `X-API-Key` header.

```
GET https://meshmapper.net/get_leaderboard.php?region=SWE
```

| Parameter | Description |
| --- | --- |
| `region` | A region or superregion code, such as `YOW` or `SWE`. Upper or lower case. |

- A **personal key** reads the regions its owner's linked companions have pinged in, plus the superregions that contain them.
- An **integration key** reads the regions it is assigned to.

## Response

```json
{
  "region": "SWE",
  "name": "Sweden",
  "is_group": true,
  "generated_at": 1761955200,
  "boards": {
    "all_time": [
      {"rank": 1, "user": "Anna", "points": 20511, "hex": "1A2B...", "account": 1},
      {"rank": 2, "user": "louie", "points": 18342, "hex": "077F...", "account": 1}
    ],
    "weekly": [],
    "pioneers": [],
    "airtime_savers": [],
    "explorers": [],
    "repeater_admins": []
  }
}
```

| Field | Description |
| --- | --- |
| `region`, `name` | The code you asked for (uppercase) and its name. |
| `is_group` | `true` for a superregion. Its boards combine every member region. |
| `generated_at` | When the boards were built, as a Unix timestamp in seconds. |
| `boards` | Six boards, each a list of up to 10 rows, best first. A board nobody scored on yet is an empty list. |

| Board | On the leaderboard page |
| --- | --- |
| `all_time` | All-Time |
| `weekly` | Weekly (the last 7 days) |
| `pioneers` | Pioneers: squares pinged first |
| `airtime_savers` | Airtime Savers, valued in points |
| `explorers` | Explorers: squares travelled |
| `repeater_admins` | Most Repeaters Administered |

### Row fields

| Field | Description |
| --- | --- |
| `rank` | 1 to 10. |
| `user` | The name the board shows. |
| `points` | The board's score: points, squares or repeaters, depending on the board. |
| `hex` | The companion's public key. Pass it to the [Profile API](profile-api.md) as `hex_id` to get that person's profile. |
| `account` | `1` when the row is a portal account (all its linked devices together), `0` for a single device. |

Boards are rebuilt about once a day, so `generated_at` usually changes once a day. Asking more than once an hour gains nothing.

## Example: how far am I from first place?

```python
import os
import requests

KEY = {'X-API-Key': os.environ['MESHMAPPER_API_KEY']}
board = requests.get('https://meshmapper.net/get_leaderboard.php',
                     params={'region': 'SWE'}, headers=KEY, timeout=30).json()
rows = board['boards']['all_time']
me = next((r for r in rows if r['user'] == 'louie'), None)
if me:
    print(f"#{me['rank']}, {rows[0]['points'] - me['points']} points behind #1")
```

If you're outside the top 10, look your own points up with the [Profile API](profile-api.md).

## Errors

| Status | Error | Meaning |
| --- | --- | --- |
| 400 | `invalid_region` | `region` is missing or not a region code. |
| 403 | `region_not_allowed` | Your key can't read this region (see above). |
| 503 | `board_unavailable` | This board hasn't been built yet. Try again after `Retry-After`. |

Key and limit errors are listed on [Personal API keys](personal-api-keys.md#errors) and [API keys and access](api-keys.md#read-api-errors).
