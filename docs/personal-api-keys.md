# Personal API keys

A personal API key is for your own scripts: chart your points, or watch how close you are to the top of your region's leaderboard. Every portal account can make one. Send it in the `X-API-Key` header and your script gets a proper, documented way in instead of being flagged as automated traffic.

## Get a key

1. Sign in at [portal.meshmapper.net](https://portal.meshmapper.net).
2. Open **Profile Settings** and find the **API key** card.
3. Press **Generate key**. Use **Show** or **Copy** to get the value.

Each account has one key.

- **Regenerate** gives the key a new value. The old value stops working at once, and the key keeps any extra APIs an admin gave it.
- **Delete** removes the key. A key you generate afterwards starts with the default APIs, but calls you already made today still count against today's limit.

## What it can read

| API | What you get | Where |
| --- | --- | --- |
| [Profile API](profile-api.md), `get_profile.php` | The same profile the site shows for a companion: points, squares, awards, regions | Any companion, anywhere |
| [Leaderboard API](leaderboard-api.md), `get_leaderboard.php` | A region's or superregion's six top 10 boards | Your regions and their superregions (below) |

**Your regions** are the regions your linked companions have pinged in, plus every superregion that contains one of them. The API key card lists them under **Leaderboards**. The list updates about once an hour, so a region you wardrive for the first time unlocks shortly after. With no linked companion there are no boards yet, but profiles still work. [Link a companion](portal.md) first.

The MeshMapper admins can add other APIs to one key, for example the [Repeaters API](repeaters-api.md). Ask in [Discord](https://discord.gg/tyXbecdxgr) if you need one. Those APIs follow the same region rule: on a superregion that contains one of your regions, they answer for the whole superregion.

## Use it

```bash
export MESHMAPPER_API_KEY='your key'

curl --fail-with-body --compressed -H "X-API-Key: $MESHMAPPER_API_KEY" \
  'https://meshmapper.net/get_leaderboard.php?region=SWE'

curl --fail-with-body -H "X-API-Key: $MESHMAPPER_API_KEY" \
  'https://meshmapper.net/get_profile.php?hex_id=<your companion public key>'
```

Keep the key out of anything you publish: source control, shared notebooks, web pages. If it leaks, regenerate it.

## Limits

By default a personal key gets **100 calls per UTC day and 10 per minute**, shared by every API the key can call. (If an admin grants your key Coverage, Coverage keeps its own daily count.) The day resets at midnight UTC. Your card shows how many calls you have used today.

When the limit is reached the answer is `503 key_rate_limited` with a `Retry-After` header: wait at least that many seconds. Leaderboards and profile points are rebuilt about once a day, so polling more often than once an hour gains nothing.

## Errors

| Status | Error | What to do |
| --- | --- | --- |
| 401 | `missing_key`, `invalid_key` | Send your current key in `X-API-Key`. A regenerated or deleted key stops working at once. |
| 403 | `api_not_allowed` | Your key can't call this API. Ask the admins if you need it. |
| 403 | `region_not_allowed` | That region isn't one of yours. The answer's `message` explains the rule. |
| 400 | `invalid_region` | Use a region or superregion code such as `SWE` or `YOW`. |
| 503 | `board_unavailable` | That board hasn't been built yet. Try again after `Retry-After`. |
| 503 | `key_rate_limited` | You've used today's or this minute's calls. Wait for `Retry-After`. |
| 503 | `auth_unavailable` | A temporary server problem. Wait for `Retry-After`. |

If your account's API access was turned off, the card says so and you can't make a new key. Ask in [Discord](https://discord.gg/tyXbecdxgr).
