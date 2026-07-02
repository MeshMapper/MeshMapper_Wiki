# Privacy Notice

**Last Updated:** July 1, 2026

MeshMapper ("we", "us", or "our") operates the MeshMapper platform at meshmapper.net and its associated regional subdomains. This Privacy Notice explains how we collect, use, and protect your information when you use our services.

## Information We Collect

### Account Information
When you sign in or link your account via Discord OAuth, what we receive depends on where you authenticate:

- **My MeshMapper portal:** with your permission, we receive your Discord user ID, username, avatar, and the email address associated with your Discord account. Your avatar is stored only for optional display on your public leaderboard profile, and only if you choose to enable it.
- **Region administration and the main site:** we receive only your Discord user ID and username.

We use your Discord user ID to send you automated notifications, such as direct messages about your regions or pending repeaters.

If you create a **My MeshMapper** portal account, we store your chosen username, your email address (used for account verification and password resets), and a hash of your password. Your email address is never displayed publicly and is not used for marketing.

### Location and Coverage Data
When you participate in wardriving sessions, the following data is collected:

- **GPS coordinates** (latitude and longitude) of your device during active sessions
- **Signal metrics** such as RSSI, SNR, and hop counts
- **Session metadata** including timestamps, region, and session identifiers
- **Node identifiers** for mesh network repeaters and devices encountered, including your device name
- **Device identity**, including your device's public key — a persistent, unique identifier for your mesh node
- **Device and radio details**, such as your radio model, app version, radio frequency, transmit power, GPS accuracy, and noise-floor readings

This data is essential to the core function of MeshMapper: building community-driven RF coverage maps.

Note that by default the wardriving app does **not** broadcast your GPS coordinates over the mesh radio channel — pings carry a short anonymous token on the air, and your coordinates are transmitted only to our servers over the internet. An opt-in setting ("Broadcast My Coordinates") is available for users who want their position visible on the air.

### Technical Data
We may collect standard technical information such as:

- IP addresses (used for rate limiting and abuse prevention; full IP addresses are also recorded in server access logs, which are retained for approximately 30 days)
- Browser user-agent strings
- Server access logs

## How We Use Your Information

We use the information we collect to:

- **Provide the service:** Display RF coverage maps, leaderboards, and network analytics
- **Manage sessions:** Track active wardriving sessions and associate data with contributors
- **Improve the platform:** Analyze aggregate usage patterns to improve map accuracy and features
- **Prevent abuse:** Rate limiting, session validation, and security monitoring

## Data Sharing and Visibility

- **Coverage data is public.** GPS-tagged signal data submitted through wardriving is displayed on publicly accessible maps. This is the core purpose of MeshMapper.
- **Leaderboard data is public.** Usernames and contribution statistics appear on regional and global leaderboards (if "anonymous" mode is not enabled on the wardriving app).
- **We do not sell your personal data** to third parties.
- **We do not share your data with advertisers.**
- We may share data with regional administrators who manage their respective MeshMapper regions.
- **Optional third-party forwarding.** The wardriving app includes an optional feature, off by default, that forwards your ping data to a custom endpoint that *you* configure. If you enable it, data is sent to the third-party destination you specify, and that destination's handling of your data is your responsibility.

## Data Storage and Security

- All data is stored in databases on our servers.
- Sessions are managed server-side using PHP sessions and API key authentication.
- Data sent from the wardriving app to our servers is transmitted over secure (HTTPS/TLS) connections, and our MQTT data ingestion also runs over TLS.
- Wardriving-channel messages carried over the mesh use the MeshCore channel's standard AES encryption and are decrypted on our ingestion server. This relies on the shared public channel key, and some mesh traffic (such as repeater advertisements and status pings) is transmitted unencrypted as part of the mesh protocol — the mesh channel should not be treated as a private or confidential transport.
- We take reasonable measures to protect your data, but no method of electronic transmission or storage is 100% secure.

## Third-Party Services

MeshMapper integrates with the following third-party services:

- **Discord** for OAuth authentication ([Discord Privacy Policy](https://discord.com/privacy))
- **MapLibre GL** as the map rendering engine ([MapLibre](https://maplibre.org/))
- **OpenFreeMap** for standard, bright, and dark base map tiles ([OpenFreeMap](https://openfreemap.org/))
- **OpenTopoMap** for topography tiles ([OpenTopoMap](https://opentopomap.org/))
- **Esri** for satellite imagery — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-GP, and the GIS User Community ([Esri Privacy Policy](https://www.esri.com/en-us/privacy/overview))
- **Google Maps** for the Google Satellite and Google Hybrid base layers ([Google Privacy Policy](https://policies.google.com/privacy))
- **AWS Open Data Terrain Tiles** for 3D terrain elevation data
- **Nominatim** for geocoding / location search ([Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/))
- **OpenStreetMap** for map data ([OpenStreetMap Privacy Policy](https://wiki.osmfoundation.org/wiki/Privacy_Policy))
- **LetsMesh.net** as the MQTT broker for wardriving data ingestion ([LetsMesh](https://letsmesh.net/))
- **GitHub** for handling in-app bug reports, which may include information you choose to submit in a report ([GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement))
- **OpenTopoData** for elevation lookups ([OpenTopoData](https://www.opentopodata.org/))
- **Content delivery networks** — our web interface loads fonts, scripts, and an anti-abuse CAPTCHA widget from third-party CDNs (including Google Fonts, unpkg, jsDelivr, Cloudflare cdnjs, and cap.js). These providers may receive your IP address and browser user-agent when their assets are loaded.

## Data Retention

- Coverage and session data is retained indefinitely to maintain historical map accuracy.
- Records of individual mesh repeaters that have not been heard for 30 days may be automatically removed.
- You can view and delete your own contributed data yourself through the [My MeshMapper portal](portal.md) after verifying ownership of your device.
- You may also request deletion of your data by contacting us at admin@meshmapper.net.

## Your Rights

Depending on your jurisdiction, you may have the right to:

- **Access** the personal data we hold about you
- **Correct** inaccurate or incomplete data
- **Delete** your personal data (subject to legitimate retention needs)
- **Object** to or restrict certain processing of your data

To exercise any of these rights, please contact us at admin@meshmapper.net.

## Children's Privacy

MeshMapper is not directed at children. We do not knowingly collect personal information from children. If you believe a child has provided us with personal data, please contact us at admin@meshmapper.net so we can remove it.

## Changes to This Notice

We may update this Privacy Notice from time to time. Changes will be reflected by updating the "Last Updated" date at the top of this page.

## Contact

If you have questions about this Privacy Notice, please reach out via the MeshMapper Discord community or contact us at admin@meshmapper.net.
