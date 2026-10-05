# API keys and access

MeshMapper uses the same **Coverage API key** for Coverage and the read APIs below. Existing keys keep their values, geographic assignments and Coverage quota. There is no need to regenerate a key for the new endpoints.

!!! info "Server v1.5.117 rollout"
    Zones, boundaries, scopes and channels require keys when the updated server endpoints are deployed. Send your key now as part of the migration. Repeater authentication has a separate switch, off by default until app 1.4.1 is shipped and the update is forced. This page describes the new contract, not a confirmation that every region has deployed it.

## Endpoints and key types

| API | Credential | Geographic access |
| --- | --- | --- |
| [Coverage](coverage-api.md), `coverage.php` | Coverage key in `X-API-Key` or legacy `?key=` | Assigned region, group, selected regions or GLOBAL |
| [Region directory](zones-api.md), `get_zones.php` | Coverage key in `X-API-Key` | Authorized regions within the requested country |
| [Boundaries](zones-api.md#region-boundary), `get_geojson.php` | Coverage key in `X-API-Key` | Requested region or fully authorized group |
| [Scopes](scopes-api.md), `get_scopes.php` | Coverage key in `X-API-Key` | Requested region or fully authorized group |
| [Channels](channels-api.md), `get_channels.php` | Coverage key in `X-API-Key` | Requested region or fully authorized group |
| Repeaters, `get_repeaters.php` | Scoped Coverage key or existing mobile App key in `X-API-Key`; optional during transition | Coverage keys stay within their assignments; App keys support the app's cross-region repeater reads |

Only Coverage accepts a query-string key. App keys do not grant access to Coverage, zones, boundaries, scopes or channels. The mobile app can send its existing App key for repeaters before connecting a radio or starting a session.

## Generate or reuse a key

In your region or group's admin panel, open **User Settings > API Access**. Generate a key with a description, or show your existing key. Each administrator can have one self-service key per region or group. Regeneration invalidates the old value immediately.

Group keys cover the group's current enabled member IATAs, including membership changes without issuing a new key. A key for just one member cannot fetch a whole group's boundaries, scopes or channels unless it covers every enabled member. Repeater exports are filtered to the Coverage key's authorized members, even where a member URL normally expands to its group.

Contact the MeshMapper team for custom integrations, selected-region or GLOBAL access, endpoint permissions, or larger limits. Master admins can allow only the endpoints an integration needs. GLOBAL permits geographic access across regions; it does not remove required parameters or turn every endpoint into an all-region feed. For example, `get_zones.php` still requires `country`.

## Send the key

Keep integration keys in your backend configuration, outside source control and visitor-facing JavaScript. For example, with `MESHMAPPER_API_KEY` set in your environment:

```bash
curl --fail-with-body --compressed \
  -H "X-API-Key: $MESHMAPPER_API_KEY" \
  'https://yow.meshmapper.net/get_scopes.php'
```

Send the header on every request, including conditional requests. CORS preflights allow `X-API-Key` and `If-None-Match`.

## Limits and caching

The five read APIs share a default budget of **1,000 admitted requests per UTC day and 30 per fixed minute per Coverage key**. Custom keys may have different limits. Coverage retains its separate daily quota, normally 100 calls for self-service keys. Read calls do not consume Coverage calls.

Every admitted read counts, including a `304` and a downstream data error. Authentication and authorization failures do not consume the read budget. `OPTIONS` preflights do not count. Existing IP burst protection also applies; App repeater reads do not put all phones behind one shared daily key budget.

Authenticated reads replace the previous once-per-target IP interval. Key quota exhaustion returns `503 key_rate_limited` with `Retry-After`; wait at least that long before retrying. The daily allowance resets at midnight UTC. A zones/boundaries/scopes/channels IP burst rejection returns `503 slow_down`; repeaters may return `429 rate_limited`. Coverage retains its own documented `429` responses.

Protected responses use `Cache-Control: private, no-store`. Keep your backend's parsed data and any ETag separately for each credential and geographic scope, and discard data when access changes. Where supported, `If-None-Match` saves bandwidth but not quota. Do not expose keys in shared cache URLs. Coverage's server-side grid cache is unchanged.

## Read API errors

| Status | Error | Action |
| --- | --- | --- |
| 401 | `missing_key`, `invalid_key` | Supply a current key in `X-API-Key`. |
| 403 | `wrong_key_type` | Use a Coverage key; App keys only support repeaters. |
| 403 | `api_not_allowed` | Ask the key owner to review endpoint permissions. |
| 403 | `no_region`, `region_not_allowed` | Check the key's region/group assignment. |
| 503 | `key_rate_limited` | Wait for `Retry-After`. |
| 503 | `auth_unavailable` | Authentication storage is temporarily unavailable; respect `Retry-After`. |

Endpoint-specific errors remain documented on each API page. Coverage keeps its existing missing/invalid-key errors and adds `403 api_not_allowed` and `503 auth_unavailable`.
