# My MeshMapper (User Portal)

**My MeshMapper** is a self-service portal where wardrivers can create an account, prove ownership of their companion devices, and view and manage the data they have contributed to MeshMapper.

**Portal URL:** [https://portal.meshmapper.net](https://portal.meshmapper.net)

You can also reach it from any region map via the **About** menu → **My Portal / Sign in**.

---

## Creating an Account

1. Open the portal and choose **Register**.
2. Pick a username (3–30 characters; letters, numbers, `_`, `.`, `-`), enter your email address, and choose a password (8+ characters).
3. Check your inbox for a **verification email** and click the link. Verification links expire after 24 hours — you can request a new one from the login screen if needed.
4. Once verified, log in with your username (or email) and password.

Forgot your password? Use the **password reset** option on the login screen — a reset link is emailed to you (valid for 1 hour).

!!! info "Portal accounts vs admin accounts"
    Portal accounts are for wardrivers and are separate from region **administrator** accounts (which are managed through the [Admin Portal](admins.md)).

---

## Linking Your Companion Devices

Linking a device proves you own it and connects that device's wardriving history to your account. MeshMapper uses a cryptographic proof — the portal sends your radio a random one-time challenge (a "nonce"), your radio signs it with its private key, and the server verifies the signature against the public key it already knows for that device. Nobody can claim a device they don't physically control.

The in-browser signing is built on **Liam Cottle's [meshcore.js](https://github.com/meshcore-dev/meshcore.js) library**, specifically his [companion_sign_data.js example](https://github.com/meshcore-dev/meshcore.js/blob/master/examples/companion_sign_data.js) — thanks Liam!

**To link a device:**

1. Log in to the portal and choose to link a device.
2. Connect your MeshCore companion to the browser via **USB** or **Bluetooth** when prompted.
3. The portal sends a one-time challenge to your radio, which signs it and returns the signature. This happens automatically in a few seconds.
4. Optionally give the device a label (e.g., "Car T1000"). Done!

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

Once logged in with at least one linked device:

- **View your sessions** — Your wardriving sessions across every region, with ping counts.
- **View your pings on the map** — Jump from the portal straight to a region map showing only *your* contributions ("My Pings" mode).
- **Delete your data** — Remove the pings from a single session, or delete everything you've ever contributed. Deletions apply across all regions and take effect on the map immediately.
- **Set a display name** — Choose the name shown on your profile and leaderboards.
- **Manage your account** — Change your email address or password.

!!! warning "Deletions are permanent"
    Deleting pings from the portal permanently removes them from MeshMapper's coverage data. There is no undo.

---

## Privacy

The portal only ever shows you data belonging to devices you have cryptographically proven you own. Region administrators can still manage data within their own regions (see [Admin Portal](admins.md)), but your portal account and email address are never displayed publicly.

For questions or problems with the portal, ask in the [MeshMapper Discord](https://discord.gg/tyXbecdxgr).
