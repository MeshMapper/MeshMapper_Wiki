# Frequently Asked Questions

---

## General

??? question "What is MeshMapper?"
    MeshMapper is a community-driven, web-based RF coverage mapping platform for MeshCore LoRa mesh networks. Users "wardrive" with mobile devices to collect GPS-tagged signal data, which is then visualized on interactive maps showing coverage areas, dead zones, and repeater locations.

??? question "How much does MeshMapper cost?"
    MeshMapper is completely free to use. The platform is community-driven and maintained by volunteers.

??? question "How do I get my region added to MeshMapper?"
    Use the [new region form](onboarding.md). You need a valid email address and at least one observer sending data to the MeshMapper MQTT broker (see [MQTT setup](mqtt-main.md)). Linking Discord is optional.

??? question "What is a region?"
    A region is a geographic area on MeshMapper that has its own map, administrators, and settings. Regions are typically centered around a city or metropolitan area. Some regions are grouped into multi-region setups that share a single map view.

??? question "My repeater shows as Ambiguous. Why?"
    As a region's mesh network grows, two repeaters can end up sharing the same short ID. When MeshMapper can't tell a repeater apart from another at the ID width it advertises, it marks it **Ambiguous** and doesn't credit pings to it.  [Read more about it here](duplicaterepeaterid.md).


??? question "Does MeshMapper support multibyte?"
    Yes, MeshMapper fully supports multibyte repeater hops/paths.  [Read more about it here](multibyte.md).

??? question "How long does it take for my region to be onboarded?"
    Once the onboarding form is completed, the MeshMapper servers perform an MQTT verification.  This checks that an observer in the region is sending data to the MeshMapper MQTT broker (we also accept data seen on the public LetsMesh broker, which isn't MeshMapper infrastructure). This can take up to 5 minutes. If verification is successful, the region is presented to the MeshMapper administration team for review. The team checks that boundaries are set correctly, reads any notes added during onboarding, determine if the region should belong to a multiregion, etc.  Once complete, the region is deployed.  As the process after MQTT verification is manual, the time to complete can vary, but typically regions are onboarded in under 24 hours.

---

## Wardriving & Coverage

??? question "What is wardriving?"
    Wardriving is the process of traveling through an area while collecting signal data from your mesh network. As you move, the MeshMapper companion app records GPS coordinates alongside signal quality data, building a picture of where your network has coverage.

??? question "What do the different coverage colours mean?"
    Each colour represents a different type of signal interaction:

    - **Green (BIDIR)** — Two-way confirmed link
    - **Orange (TX)** — Transmitted and routed through the mesh, but no repeats heard back
    - **Purple (RX)** — Heard mesh traffic, but didn't transmit
    - **Cyan (DISC/TRACE)** — A discovery or trace request got a reply
    - **Grey (DEAD)** — A repeater heard it, but no other radio received the repeat
    - **Red (DROP)** — No repeats heard and no successful route

    For more detail, see [Understanding Visuals](visuals.md).

??? question "Do I need the companion app to contribute data?"
    Yes. The MeshMapper companion app is the primary way to submit wardriving data. It is available for both Android and iOS. See [Getting Started](app_getting_started.md) for setup instructions.

??? question "Does the wardriving app broadcast my location on the mesh?"
    Not by default. TX pings sent on the #wardriving channel carry a short anonymous token instead of coordinates, and your GPS position travels only to the MeshMapper server over the internet. Anyone listening on the channel sees the token, not where you are. If you *want* your live position visible on the air (e.g., so local mesh users can follow your drive), enable **Broadcast My Coordinates** under Settings > Wardriving in the app.

??? question "Can I view or delete the data I have contributed?"
    Yes. Create an account on the [My MeshMapper portal](portal.md), link your companion device (a quick cryptographic proof over USB or Bluetooth), and you can view your sessions, see your own pings on the map, set your leaderboard display name, and delete some or all of your contributed pings. To delete your account itself, contact admin@meshmapper.net.

??? question "Why isn't my recent data showing on the leaderboard?"
    Leaderboards and profile statistics are regenerated about once a day, so new contributions can take up to 24 hours to appear. The coverage map itself updates in near-real-time.

??? question "Why does the app show Deferred instead of sending a ping?"
    Smart Pinging is holding that ping because the square you are in already has recent coverage on the map. The ping is kept, not dropped: it goes out the moment you reach a square with nothing recent, and you are credited for the square you crossed without transmitting. It is on by default. See [Smart Pinging](app_wardriving_modes.md#smart-pinging), or turn it off under Settings > Wardriving in the app.

??? question "Do I lose leaderboard points when Smart Pinging holds a ping?"
    No. Each square where a ping was held is reported to MeshMapper, checked against the region's own coverage data, and credited at 1.5 points once verified. Verified squares also count toward the Airtime Saver, Airtime God and Airtime Legend awards and the Top Airtime Savers board. Like the rest of the leaderboard, the credit appears after the next daily update.

??? question "Do coverage tiles expire when a repeater moves or disappears?"
    Coverage remains until its underlying pings are removed or filtered out. An admin can enable [stale ping cleanup](admins.md#stale-ping-cleanup-auto-delete-orphaned-pings) for pings whose repeater moved or vanished, or preview and confirm a one-time purge. A time filter can hide older tiles without deleting their data.

---

## Mobile App

??? question "Where can I download the MeshMapper app?"
    The companion app is available on both the Google Play Store (Android) and the Apple App Store (iOS). Search for "MeshMapper" or visit the [App Overview](app_overview.md) page for direct links.

??? question "How does the app connect to my MeshCore device?"
    The app connects to your MeshCore device over Bluetooth, over TCP/Wi-Fi, or over USB on Android. See the [Connection Guide](app_connection_guide.md) for pairing instructions and troubleshooting tips.

??? question "How do I join the app beta?"
    In the MeshMapper Discord server, open **Channels & Roles** and select **Yes** for beta testing. Then use [TestFlight for iOS](https://testflight.apple.com/join/PXxfr5Jr) or the [GitHub APK for Android](https://github.com/MeshMapper/MeshMapper_Project/releases/). Android users can also [add MeshMapper to Obtainium](https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/%7B%22id%22%3A%22net.meshmapper.app%22%2C%22url%22%3A%22https%3A%2F%2Fgithub.com%2FMeshMapper%2FMeshMapper_Project%22%2C%22author%22%3A%22MeshMapper%22%2C%22name%22%3A%22MeshMapper%22%2C%22preferredApkIndex%22%3A0%2C%22additionalSettings%22%3A%22%7B%5C%22includePrereleases%5C%22%3Atrue%2C%5C%22fallbackToOlderReleases%5C%22%3Atrue%7D%22%2C%22overrideSource%22%3A%22GitHub%22%7D) to follow prereleases.

??? question "How do I claim a repeater I administer?"
    Sign in to your MeshMapper account in the app, connect your companion, select the repeater on the map, then tap **Manage**. Sign in with the repeater's admin password and tap **Claim**. The claim lists your account as a repeater administrator on the map.

??? question "Why does the app say my companion is unknown?"
    The server has not recognized that radio's public key yet. Use the official MeshCore app to advertise the companion on the mesh, wait for an observer to receive it, then reconnect to MeshMapper. Check that you are in an active region with an observer.

??? question "Does MeshMapper work with CarPlay or Android Auto?"
    The iOS Live Activity can appear as a small CarPlay dashboard card on supported iOS versions. There is no full CarPlay map or Android Auto screen in the app. Android audio is designed to duck and release car audio during app sounds.

??? question "What happens when I drive across a region boundary?"
    The app pauses if it is outside every active region. When it enters another region, the server can transfer the active session to that region and the app resumes after zone authentication. A multiregion group provides a shared map for neighboring regions. Keep GPS accurate and watch the zone indicator on a long drive.

??? question "Can I wardrive from an airplane?"
    No. The app blocks or ends wardriving when GPS indicates aircraft travel. The server also flags suspiciously fast uploaded sessions for administrator review. Map an area from the ground instead.

---

## Administration

??? question "How do I become a region administrator?"
    For a new region, volunteer in the [onboarding form](onboarding.md#volunteer-as-region-administrator). For an existing region, ask its administrator for an invite. If the region has no administrator, ask a Moderator in the MeshMapper Discord for help with access.

??? question "Where can I find my region's administrator?"
    Open **Region Info** on your region's map. See [Finding Your Region's Administrators](administratorlist.md) for other ways to reach them.

??? question "I'm an admin. Where do I manage my region?"
    Region administrators can manage settings, repeaters, and sessions through the Admin Portal. See [Admin Portal](admins.md) for details.

### Region setup and access

??? question "How do I rename my region?"
    Ask a global administrator to change its display name. The region editor in the global admin panel controls the name; the region's own settings panel does not.

??? question "What if my region's administrator is inactive?"
    Contact a Moderator through the [administrator contact guide](administratorlist.md). A global administrator can grant region access to another verified MeshMapper account, so an inactive administrator does not have to issue the invite.

??? question "How do I split or merge regions?"
    Coordinate the new boundaries with neighboring admins, then ask a global administrator. The global panel can merge whole regions, including their sessions, or move pings within a selected area. An area transfer does not move whole sessions. Changing a boundary alone does not move earlier data.

??? question "How big should my region be?"
    Drop the pin on your area and use **Load Boundary** (State/Prov, County or Local) to pick an OpenStreetMap boundary that matches the mesh you expect to map, and coordinate it with nearby regions. Custom drawn or GeoJSON boundaries are for special cases only. The onboarding form checks for substantial overlap, and the MeshMapper team reviews each request. See [Boundary](onboarding.md#3-boundary).

??? question "Can I use any three letters as my region code?"
    No. Pick a recognized IATA airport code near your area. The form checks that the code is available and geographically appropriate; it will suggest nearby codes when one is too far away. See [Code](onboarding.md#1-code).

??? question "Why does the form say my code is already used or pending?"
    A code can belong to only one active or pending region. Open that region's subdomain to check its pending status, and contact a Moderator if the request appears stuck. Do not submit another region with a made-up code.

??? question "Why did my onboarding submission fail?"
    Read the error shown by the form. It checks the airport code, region name, email, boundary and overlap with existing regions. Correct the reported field and retry; if the form says you have submitted too often, wait a few minutes.

??? question "Does my area already have a region?"
    Check the [MeshMapper region map](https://meshmapper.net) before starting a request. If a nearby region can reasonably expand to include your area, contact its administrator first. The new-region form checks for overlap with existing boundaries.

??? question "My observer is online. Why is onboarding still pending?"
    The pending request must receive observer reports tagged for its region code through a supported MQTT broker. A connected observer that has sent no matching reports does not complete verification. Check the pending status page and [observer setup](mqtt-main.md), then wait for manual approval once verification passes.

??? question "Which code should an observer use? Can a region have aliases?"
    Set the observer's IATA topic to the region code shown in MeshMapper. Each region has one code; a multiregion group joins separate coded regions for a shared map. If you need the code changed, ask a global administrator instead of publishing under an unrelated code.

??? question "How do I get a Discord region-admin role?"
    Admin panel access and the Discord role are separate. The bot assigns the role when a Moderator grants access through the bot, but an email invite may not update Discord. If your admin access works and the role is missing, ask a Moderator to check it.

??? question "Why has my admin invite not arrived?"
    Check the email address used by the inviting admin and your spam folder. The inviter can resend or revoke a pending email invite from the admin panel. Bot-issued invites go by Discord DM, so allow DMs from the server if that route was used.

??? question "Why am I no longer listed as an admin?"
    Sign in with the MeshMapper account that received the invite and check that it was accepted. If the region is absent from that account, ask a global administrator to check its current region access. The admin panel checks current permissions when you open it.

??? question "How do admins work in a multiregion group?"
    A group administrator can work across the group's member regions; a member-region administrator keeps access to that region. Ask a global administrator to grant the group or additional region to the right verified account. See [Multiregion Administration](multiregions.md#administration).

??? question "What if my admin login stopped working after an account change?"
    Use the [portal](portal.md) **Forgot password** flow or **Sign in with Discord** for the account you linked. If login succeeds but your region is missing, ask a global administrator to check its access grant. The bot cannot reset an admin password.

??? question "Is a separate portal account needed for each region?"
    No. One verified MeshMapper account can hold access to several regions. The same login works on the portal and on each admin panel you are allowed to use.

??? question "Why do my region's wardriving settings revert?"
    If your region belongs to a multiregion group, its radio presets are controlled by the group and copied to member regions. Change them in the group admin panel, or ask a group administrator. For a standalone region, save the preset in its own **Settings** tab and check for any save error.

??? question "What does the traffic scope setting do?"
    **Wardriving Scope** is the scope the app sends its own pings in. **Scopes to Monitor** controls which scopes the map looks for in heard traffic. The wardriving scope and scopes reported by local repeaters are included automatically; add other scopes only when you need to track them.

??? question "Can my region keep wardriving traffic within its own scope?"
    Set the **Wardriving Scope** in the region or group admin settings for the radio preset your app uses. This chooses the scope of the app's outgoing pings; **Scopes to Monitor** only affects what the map tracks and does not constrain those pings.

??? question "Why does my region map open in the wrong place?"
    A single-region map starts at the region's stored centre; a group map starts around its members. Your browser may also remember a zoom level. A region admin can adjust the boundary editor's centre pin; ask a global administrator if the region's stored centre or name needs correction.

??? question "Where do I edit my region description, contact details or channels?"
    Open your region's admin panel and use **Settings** for the region message, links and public channels. Your own contact details are under **User Settings**. Ask a global administrator to change the region's display name.

??? question "How do I group several companions under one contributor?"
    Link your own devices to one [portal account](portal.md#linking-your-companion-devices). They then appear together as one entry on the leaderboards.

??? question "Can duplicate leaderboard entries or old device data be merged?"
    Link the devices you still control to one portal account. If the old device cannot be linked, ask a Moderator on Discord for help. Do not delete an account or device record to try to merge history.

### Portal accounts

??? question "Where do I link Discord, and is it required?"
    Sign in to the [portal](portal.md), open your account settings, and choose **Connect Discord**. It is optional for an ordinary account. A Discord-bound admin invite must be accepted while signed in with the invited Discord account.

??? question "Why did Discord linking fail?"
    If the portal says that Discord account is already linked elsewhere, sign in to the other MeshMapper account or ask a Moderator for help. If the sign-in expired or was cancelled, start the connection again from the portal. Do not create a third account to work around it.

??? question "Can I merge or remove duplicate MeshMapper accounts myself?"
    There is no account-merge button in the portal. Pick the account you want to keep and ask a Moderator to review the duplicate before deleting anything. A Discord account and a companion device can each be linked to only one portal account at a time.

---

## Support & Contributing

??? question "How do I report a bug?"
    You can report bugs by tagging the MeshMapper bot on Discord with `!bug` followed by a description, or through the MeshMapper website and mobile app. See [Report Bugs & Features](reportbugs.md) for more info.

??? question "How do I request a feature?"
    Tag the MeshMapper bot on Discord with `!feature` followed by your idea, or through the MeshMapper website or mobile app. See [Report Bugs & Features](reportbugs.md) for more info.

??? question "Where can I get help if my question isn't answered here?"
    Try the [MeshMapper Wiki](https://wiki.meshmapper.net) first. If you still need help, post in the MeshMapper Discord server. You can also tag the @MeshMapper AI bot directly and it will do its best to answer based on the wiki and its training.

??? question "I would like to contribute!"
    Thank you!  Feature requests can be submitted through the MeshMapper AI bot, website, or mobile app (see above).  If you would like to help support the costs of development, servers, hosting, etc., [you're welcome to do so via BuyMeACoffee](https://buymeacoffee.com/meshmapper).  Thank you!

---

## Access to Data

??? question "Can I export my regions data?"
    Yes, data can be exported in .csv format through the admin panel.

??? question "Can I scrape for data or call your API's?"
    Unauthorized scraping or access to undocumented API's is strictly prohibited and will result in action being taken to protect MeshMapper's data and servers.

    The publicly available APIs are [listed here](coverage-api.md) and require the use of a provisioned API key.

??? question "Can I have access to the MeshMapper MQTT broker or raw data?"
    MeshMapper does not offer a public raw MQTT feed. For tools that need map coverage data, use the documented [Coverage API](coverage-api.md) and request an API key. A region admin can configure a broker that sends observer reports *to* MeshMapper; that is separate from read access to MeshMapper's collected data.

??? question "Is MeshMapper open source?  Can I run a local copy?"
    The MeshMapper wardriving app for Android and iOS is open source.  It can also natively be configured to send wardriving data to additional endpoints outside of MeshMapper.

    The MeshMapper web interface is not open source and cannot be run locally.  The MeshMapper development team has put time, effort, and money into developing a tool that can be used and is accessible to all globally without the requirement/complexity/cost of any per-region/local configuration of code, servers, MQTT engines, hosting, etc.  Part of MeshMapper's appeal is global leaderboards and comparing region by region, which is not possible unless made a global platform.
