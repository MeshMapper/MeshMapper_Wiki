# System Status

## Checking MeshMapper Status

- **Discord** — Outages and scheduled maintenance are announced in the [MeshMapper Discord server](https://discord.gg/tyXbecdxgr). This is the fastest place to check whether an issue is already known.
- **Maintenance mode** — During maintenance the map shows an **Under Maintenance** page (a warning banner may appear on the map beforehand), and the wardriving app shows a maintenance message. You can keep wardriving in [Offline Mode](app_connection_guide.md#offline-mode) and upload your sessions once service is restored. Individual regions can also pause wardriving, in which case the app shows the region's message.
- **Your region's ingestion** — If the platform is up but your region's data seems stale, open **Region → Observers** on your region's map to see whether its MQTT observers are online. The Discord bot's `!status YOW` shows the region's status and its data, repeater and observer counts (not whether observers are online right now).

If you're seeing a problem that isn't announced anywhere, please report it — see [Report Bugs & Features](reportbugs.md).
