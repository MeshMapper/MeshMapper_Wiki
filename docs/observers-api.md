# Observers API

The Observers API lists a region's or superregion's MQTT observers and when MeshMapper last heard from each one, as JSON. It's the list behind the map's **Observers** button. Use it to check that your observer is still reporting. Send a [personal API key](personal-api-keys.md) or an [integration key](api-keys.md) in the `X-API-Key` header.

```
GET https://meshmapper.net/get_observers.php?region=YOW
GET https://meshmapper.net/get_observers.php?region=YOW&pubkey=1A2B3C
```

| Parameter | Description |
| --- | --- |
| `region` | A region or superregion code, such as `YOW` or `SWE`. Upper or lower case. |
| `pubkey` | Optional. Your observer's public key, or at least its first 6 characters. Upper or lower case. Only observers whose key starts with it are listed. |

- A **personal key** reads the regions its owner's linked companions have pinged in, plus the superregions that contain them.
- An **integration key** reads the regions it is assigned to.

## Response

```json
{
  "region": "YOW",
  "name": "Ottawa, CA",
  "is_group": false,
  "generated_at": 1762052400,
  "count": 1,
  "observers": [
    {
      "pubkey": "1A2B3C...",
      "name": "Kanata Observer",
      "region": "YOW",
      "status": "online",
      "mqtt_status": "online",
      "last_status": 1762052100,
      "last_packet": {"meshmapper": 1762052280, "letsmesh": 1762051990},
      "firmware": "v1.9.0",
      "radio": "910.525,62.5,7"
    }
  ]
}
```

| Field | Description |
| --- | --- |
| `region`, `name` | The code you asked for (uppercase) and its name. |
| `is_group` | `true` for a superregion. Its list combines every member region. |
| `generated_at` | When the list was read, as a Unix timestamp in seconds. The list is read fresh on every call. |
| `count` | How many observers are listed. |
| `observers` | Online first, then stale, then offline. Within each, the most recent status comes first. A pubkey with no match gives an empty list. |

### Observer fields

| Field | Description |
| --- | --- |
| `pubkey` | The observer's full public key, uppercase. |
| `name` | The observer's name, or `null` when it has none. |
| `region` | The region it reports to. In a superregion, the member region that heard from it most recently. |
| `status` | The map's label: `online` when its last status message arrived in the last 24 hours, `stale` in the last 7 days, `offline` when older. |
| `mqtt_status` | The status the observer last reported over MQTT, usually `online`. `offline` means the broker reported that the observer's connection dropped. `null` when not known. |
| `last_status` | When its last status message arrived, as a Unix timestamp in seconds. `null` when none has arrived. |
| `last_packet` | For each broker, when that broker last passed on anything from this observer (a packet it heard, or its status message), as a Unix timestamp in seconds. A broker that stopped carrying it keeps its old time. `{}` when none has. |
| `firmware` | The firmware version it reports, or `null`. |
| `radio` | The radio preset it reports, as `frequency,bandwidth,spreading factor` (MHz, kHz, SF), or `null`. |

MeshMapper records an observer's status messages and packets at most once every 10 minutes, so a time up to about 10 minutes old is normal.

Observers that are also hidden repeaters (🚫 at the start or end of the name) are never listed, just as on the map.

## Example: is my observer still reporting?

Checking every 30 minutes uses 48 calls a day, within a personal key's default 100.

```python
import os
import time
import requests

KEY = {'X-API-Key': os.environ['MESHMAPPER_API_KEY']}
r = requests.get('https://meshmapper.net/get_observers.php',
                 params={'region': 'YOW', 'pubkey': '1A2B3C'}, headers=KEY, timeout=30)
r.raise_for_status()
found = r.json()['observers']
if not found:
    print('Not listed in YOW')
else:
    obs = found[0]
    newest = max([obs['last_status'] or 0, *obs['last_packet'].values()])
    quiet = (time.time() - newest) / 60
    if obs['mqtt_status'] == 'offline' or quiet > 30:
        print(f"{obs['name']}: nothing for {quiet:.0f} minutes, time to restart it")
```

Pick a limit that suits your mesh: 30 minutes works for a busy one, a quiet one may need longer.

## Errors

| Status | Error | Meaning |
| --- | --- | --- |
| 400 | `invalid_region` | `region` is missing or not a region code. |
| 400 | `invalid_pubkey` | `pubkey` isn't hex, or is shorter than 6 or longer than 64 characters. |
| 403 | `region_not_allowed` | Your key can't read this region (see above). |
| 503 | `observers_unavailable` | A temporary server problem reading the list. Try again after `Retry-After`. |

Key and limit errors are listed on [Personal API keys](personal-api-keys.md#errors) and [API keys and access](api-keys.md#read-api-errors).
