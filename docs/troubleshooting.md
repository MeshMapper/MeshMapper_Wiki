# Troubleshooting

If you're having trouble with MeshMapper, you're in the right place. Browse the common issues below, or use the resources at the bottom of this page to get further help.

---

## Map & Coverage

??? question "My repeater isn't showing on the map."
    Repeaters appear on the map once their adverts are heard through a connected observer. Try the following:

    - Force an advert from your repeater.
    - Confirm the region has at least one active observer by checking **Region Info > Observers** from the map.  A repeaters advert must be picked up by one of these observers.  If observers are missing, contact your region's administrator, as they may have a whitelist of observers from which to ingest from configured.
    - If the repeater or observer was recently added, give it a few minutes to be picked up.
    - Ensure the repeater has location coordinates configured.
    - The region may have the option "New Repeaters Enter Pending State" enabled (check through the **Region Info** page), in which event the region administrator will need to approve the repeater before it is added.

    If your repeater or room server is also an observer, it may not "hear" its own advert.  Another observer must be within range in order to ingest it's advert and display on the map.  If there are no other observers nearby, you can mimic the repeaters advert from a companion by using the MeshCore app, select the ellipses beside the repeater, select "Share", and then select "Zero Hop Advert".  When this is the case, however, this repeater will eventually become stale and get removed.  This process must be repeated regularly.

    If it still doesn't appear, contact your region's administrator.

??? question "My repeater shows as Excluded or Duplicate."
    As a region's mesh network grows, the likelihood of two repeaters sharing the same short ID increases. MeshMapper detects these collisions and disables affected repeaters to protect data integrity. See [Duplicate Repeater IDs](https://wiki.meshmapper.net/duplicaterepeaterid/) for a full explanation and resolution steps.

??? question "The map is slow or unresponsive on my device."
    Large regions with lots of data can be demanding on older devices or slow connections. Try the following:

    - **Coverage Only Mode**: A "Switch to Coverage Only" button appears on the loading screen. This loads pre-rendered tiles instead of interactive data, significantly reducing resource usage.
    - **Increase grid size**: In Settings, increase the grid size (e.g. from 100m to 300m or larger) to reduce the number of rendered elements.
    - **Filter by time**: Use Advanced Search to limit data to a recent time range (e.g. Last 30 Days).
    - **Grid Mode**: Use the "Simplified" grid mode from within the map settings.

??? question "Grid squares are showing unexpected colours."
    Grid square colours depend on the active **Coverage Mode**:

    - **Standard**: Colours represent ping type (green=BIDIR, orange=TX, purple=RX, etc.)
    - **Effective Coverage**: Averaged quality score (green=high quality, red=low quality)
    - **Signal Strength**: Based on SNR (green=strong, red=weak)
    - **Ping Age**: Based on data recency (green=recent, red=stale)
    - **Noise Floor**: Based on RF noise relative to each companion's baseline (green=quiet, red=loud)

    Check which mode is selected in the **Coverage Mode** section of the Layer Control.

---

## Mobile App

??? question "The app won't connect to my MeshCore device."
    Bluetooth connections can be finicky. Try the following:

    1. Ensure Bluetooth is enabled on your phone.
    2. Make sure your MeshCore device is powered on and not connected to another app.
    3. Try toggling Bluetooth off and on again.
    4. Restart the MeshMapper app.
    5. If pairing fails repeatedly, remove the device from your phone's Bluetooth settings and re-pair.

    See the [Connection Guide](https://wiki.meshmapper.net/app_connection_guide/) for detailed pairing instructions.

??? question "The app says I'm outside of a region."
    You need to be within a registered MeshMapper region to start a wardriving session. If there isn't a region near you, you can [request one](https://wiki.meshmapper.net/onboarding).

??? question "GPS isn't locking or accuracy is poor."
    GPS accuracy depends on your device and environment. Try the following:

    - Ensure location permissions are granted to the MeshMapper app.
    - Move to an area with a clear view of the sky (away from tall buildings or dense tree cover).
    - Wait a minute or two for the GPS to get a solid fix before starting a session.
    - On Android, ensure location mode is set to "High accuracy."

---

## Administration

??? question "I can't access the admin portal."
    The admin portal is only available to region administrators. If you believe you should have access, confirm with the person who set up the region or contact a Moderator on Discord. See the [Administrator List](https://wiki.meshmapper.net/administratorlist/) to find your region's admin.

??? question "Observer data isn't coming through."
    If your observer isn't forwarding data:

    1. Check that the observer device is running and connected to the MQTT broker.
    2. Verify the MQTT topic and credentials in your observer configuration.
    3. Check the **Observers** panel in Region Info to see if the observer is listed and its last-heard timestamp.

    See [MeshMapper MQTT Setup](https://wiki.meshmapper.net/mqtt-main/) for configuration details.

---

## Getting More Help

If you can't find the answer here, there are several ways to get support:

- **Wiki**: Browse the full wiki documentation.
- **AI Bot (@MeshMapper)**: The MeshMapper AI bot on Discord can answer many questions. Send it a DM, tag it in a public message, or reply to a message and tag it.
- **Discord Community**: The MeshMapper community on Discord is knowledgeable and very helpful. Post your question in the appropriate channel and someone will be able to help you out.
- **Region Administrator**: For issues specific to your region (settings, configuration, etc.), reach out to your [region's administrator](https://wiki.meshmapper.net/administratorlist/). If they're unavailable, tag a `@Moderator` in the MeshMapper Discord server. Moderators (also known as Global Administrators) have access to assist any region.

### Reporting Bugs

Notice a bug? You can submit a ticket using the guided form on the [Report Bugs & Features](https://wiki.meshmapper.net/reportbugs) page, or tag the MeshMapper AI bot on Discord with **`!bug`** followed by a description.

### Feature Requests

MeshMapper was built using suggestions from the community. If you have an idea, tag the AI bot with **`!feature`** followed by your suggestion, or submit it through the website or mobile app.

> Due to the size and activity of the community, these are the **only methods** to submit tickets. The developers may miss the request if sent any other way.
