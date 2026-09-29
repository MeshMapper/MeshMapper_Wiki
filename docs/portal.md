# My MeshMapper (User Portal)

**My MeshMapper** is a self-service portal where wardrivers can create an account, prove ownership of their companion devices, and view and manage the data they have contributed to MeshMapper.

**Portal URL:** [https://portal.meshmapper.net](https://portal.meshmapper.net)

You can also reach it from any region map via **About → My Portal / Sign in**.

---

## Creating an Account

1. Open the portal and choose **Register**.
2. Pick a username (3–30 characters; letters, numbers, `_`, `.`, `-`). Your username can't be changed later, and some names like `admin` or `meshmapper` are reserved.
3. Enter your email address and choose a password (at least 12 characters; common passwords, or ones containing your username, email or "MeshMapper", are rejected).
4. Check your inbox for a **verification email** and click the link. Verification links expire after 24 hours — you can request a new one from the login screen if needed.
5. Once verified, log in with your username (or email) and password.

Forgot your password? Use the **password reset** option on the login screen — a reset link is emailed to you (valid for 1 hour).

### Sign in with Discord

You can also use **Sign in with Discord** on the login screen:

- If that Discord account is already linked, you're signed in.
- If its verified email matches an existing account, it links to that account automatically.
- Otherwise a new account is created, with no password.

Under **Settings → Discord** you can **Connect Discord** or **Disconnect**, and turn on **Show my Discord avatar on leaderboards**.

- A Discord-only account can **Set password** at any time.
- While Discord is connected, you can **Remove password (use Discord only)**.
- You must set a password before you can disconnect Discord.

!!! info "One account for the portal and admin panels"
    A region administrator uses the same MeshMapper account for the portal and every [admin panel](admins.md) they can access. You do not need a separate admin login.

### Admin Invites

If you're invited to be an administrator, you get an invite link. It lasts 7 days and is tied to one email address or Discord account.

- New to MeshMapper? Choose **Create account & accept**.
- Already have an account? Choose **Sign in & accept**.
- Already signed in? Choose **Accept admin access**.

Afterwards, **Go to the admin panel** takes you to [admin.meshmapper.net](https://admin.meshmapper.net).

---

## Linking Your Companion Devices

Linking a device proves you own it and connects that device's wardriving history to your account. MeshMapper uses a cryptographic proof — the portal sends your radio a random one-time challenge (a "nonce"), your radio signs it with its private key, and the server verifies the signature against the public key it already knows for that device. Nobody can claim a device they don't physically control.

The in-browser signing is built on **Liam Cottle's [meshcore.js](https://github.com/meshcore-dev/meshcore.js) library**, specifically his [companion_sign_data.js example](https://github.com/meshcore-dev/meshcore.js/blob/master/examples/companion_sign_data.js) — thanks Liam!

**To link a device:**

1. Log in to the portal and choose **Link a companion**.
2. Choose **Connect over Bluetooth**, or **USB instead**. If the companion is connected to your phone, close the MeshCore app on it first.
3. The portal sends a one-time challenge to your radio, which signs it and returns the signature. This happens automatically in a few seconds. The challenge expires after 2 minutes.
4. Done! The device shows up under **Your companions** using its own name.

You can also sign in and link companions from the MeshMapper mobile app. The app shows up under **Settings → Connected apps**, where you can **Revoke** it.

**Browser requirements:**

Device linking uses the Web Serial / Web Bluetooth APIs, which are only available in certain browsers. You **must** use:

| Platform | Browser |
| --- | --- |
| **Mac / Windows** | **Chrome** (or another browser with Web Serial/Web Bluetooth support, e.g. Edge) |
| **Android** | **Chrome** |
| **iOS** | **[Bluefy](https://apps.apple.com/us/app/bluefy-web-ble-browser/id1492822055)** (Safari and Chrome on iOS do not support Web Bluetooth) |

**Notes:**

- Your radio should be running reasonably recent MeshCore firmware that supports signing.
- A device can only ever be linked to **one** account. If your device shows as already linked and you believe that's wrong, contact a Moderator on Discord.
- You can link multiple devices to one account, and unlink a device at any time.

!!! tip "Bluetooth linking fails on Mac or Windows?"
    Some users have run into pairing issues when linking over Bluetooth on Mac and Windows. The fix: **forget/remove the device from your computer's system Bluetooth menu first**, then return to the portal and re-pair the companion during the linking process.

---

## What You Can Do

The portal has these tabs: **Overview**, **Regions**, **Sessions**, **Companions**, **Repeaters** and **Profile Settings**.

- **Overview**: your points, grid squares mapped, regions driven, companions and awards.
- **Regions**: the regions you've driven. **View on map** opens that region's map with only your pings. A "Showing all your pings" banner appears; click **Exit** to go back to the normal map.
- **Sessions**: your wardriving sessions across every region, 50 per page. You can search, filter by region, and sort by **Newest first**, **Oldest first** or **Most pings**. Use **View** to see a session on the map, or **Delete** to remove its pings.
- **Companions**: the devices linked to your account.
- **Repeaters** ("Repeaters you administer"): repeaters you've logged in to as admin from the app. Use **Edit** to set Hardware, Antenna, Transmit power, Height above ground, Power source (Mains, Solar, Battery or PoE) and a Site note (up to 200 characters). Use **Remove claim** to drop a repeater.
- **Profile Settings**: set your "Leaderboard display name — shown publicly and must be unique" (up to 60 characters, and it can't be "Anonymous"). You can also change your email (you'll need to verify the new one) or your password.

To delete everything, use **Danger zone → Delete ALL my pings**. It asks you to confirm twice. Deletions apply across all regions and the map updates immediately.

!!! warning "Deletions are permanent"
    Deleting pings from the portal permanently removes them from MeshMapper's coverage data. There is no undo.

---

## Privacy

The portal only ever shows you data belonging to devices you have cryptographically proven you own. Region administrators can still manage data within their own regions (see [Admin Portal](admins.md)).

Your display name is public; your username and email are not. To hide your name on the map and leaderboards, turn on [Anonymous Mode](app_connection_guide.md#anonymous-mode) in the app.

For questions or problems with the portal, ask in the [MeshMapper Discord](https://discord.gg/tyXbecdxgr).
