# Frequently Asked Questions

---

## General

??? question "What is MeshMapper?"
    MeshMapper is a community-driven, web-based RF coverage mapping platform for MeshCore LoRa mesh networks. Users "wardrive" with mobile devices to collect GPS-tagged signal data, which is then visualized on interactive maps showing coverage areas, dead zones, and repeater locations.

??? question "How much does MeshMapper cost?"
    MeshMapper is completely free to use. The platform is community-driven and maintained by volunteers.

??? question "How do I get my region added to MeshMapper?"
    Visit the [Onboarding New Regions](https://wiki.meshmapper.net/onboarding) page for a step-by-step guide on how to request a new region. You'll need to join the MeshMapper Discord server to get started.

??? question "What is a region?"
    A region is a geographic area on MeshMapper that has its own map, administrators, and settings. Regions are typically centered around a city or metropolitan area. Some regions are grouped into multi-region setups that share a single map view.

??? question "My repeater shows as Excluded or Duplicate.  Why?"
    As a regions mesh network grows, the likelihood of two repeaters sharing the same ID increases. MeshMapper has a robust system for detecting, handling, and resolving these "collisions" to ensure data integrity.  Part of this duplicate detection logic is disabling repeaters that share the same ID in order to protect data integrity.  [Read more about it here](https://wiki.meshmapper.net/duplicaterepeaterid/).


??? question "Does MeshMapper support multibyte?"
    Yes, MeshMapper fully supports multibyte repeater hops/paths.  [Read more about it here](https://wiki.meshmapper.net/multibyte/).

---

## Wardriving & Coverage

??? question "What is wardriving?"
    Wardriving is the process of traveling through an area while collecting signal data from your mesh network. As you move, the MeshMapper companion app records GPS coordinates alongside signal quality data, building a picture of where your network has coverage.

??? question "What do the different coverage colours mean?"
    Each colour represents a different type of signal interaction:

    - **Green (BIDIR)** — Two-way confirmed link
    - **Orange (TX)** — Sent a packet, but didn't hear back
    - **Purple (RX)** — Heard a response, but didn't transmit
    - **Cyan (DISC)** — Discovery packets received
    - **Grey (DEAD)** — Repeater heard, but no route available
    - **Red (DROP)** — Failed packet delivery

    For more detail, see [Understanding Visuals](visuals.md).

??? question "Do I need the companion app to contribute data?"
    Yes. The MeshMapper companion app is the primary way to submit wardriving data. It is available for both Android and iOS. See [Getting Started](https://wiki.meshmapper.net/app_getting_started) for setup instructions.

---

## Mobile App

??? question "Where can I download the MeshMapper app?"
    The companion app is available on both the Google Play Store (Android) and the Apple App Store (iOS). Search for "MeshMapper" or visit the [App Overview](https://wiki.meshmapper.net/app_overview) page for direct links.

??? question "How does the app connect to my MeshCore device?"
    The app communicates with your MeshCore device over Bluetooth. See the [Connection Guide](app_connection_guide.md) for pairing instructions and troubleshooting tips.

---

## Administration

??? question "How do I become a region administrator?"
    Region administrators are assigned during the onboarding process when a new region is created. If you'd like to help administer an existing region, reach out to the current administrator or a Moderator on Discord.

??? question "Where can I find my region's administrator?"
    A full list of region administrators is available on the [Administrator List](https://wiki.meshmapper.net/administratorlist) page.

??? question "I'm an admin. Where do I manage my region?"
    Region administrators can manage settings, repeaters, and sessions through the Admin Portal. See [Admin Portal](admins.md) for details.

---

## Support & Contributing

??? question "How do I report a bug?"
    You can report bugs by tagging the MeshMapper bot on Discord with `!bug` followed by a description, or through the MeshMapper website and mobile app. See [Report Bugs & Features](https://wiki.meshmapper.net/reportbugs) for more info.

??? question "How do I request a feature?"
    Tag the MeshMapper bot on Discord with `!feature` followed by your idea, or through the MeshMapper website or mobile app. See [Report Bugs & Features](https://wiki.meshmapper.net/reportbugs) for more info.

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

    The publicly available API's are [listed here](https://wiki.meshmapper.net/coverage-api) and require the use of a provisioned API key.

??? question "Can I have access to the MeshMapper MQTT broker or raw data?"
    No.  MeshMapper is not a data broker.