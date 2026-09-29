# Troubleshooting

If you're having trouble with MeshMapper, you're in the right place. Browse the common issues below, or use the resources at the bottom of this page to get further help.

---

## Map & Coverage

<div id="repeater-not-showing" markdown>
??? question "My repeater isn't showing on the map."
    Repeaters appear on the map once their adverts are heard through a connected observer. Try the following:

    - Force an advert from your repeater.
    - Confirm the region has at least one active observer by opening **Region → Observers** on the map. A repeater's advert must be picked up by one of these observers. If observers are missing, contact your region's administrator, as the region may only accept data from a list of chosen observers.
    - If the repeater or observer was recently added, give it a few minutes to be picked up.
    - Ensure the repeater has a name and location coordinates configured. Repeaters without a location are recorded but not placed on the map.
    - The region may have **New Repeaters Enter Pending** enabled (shown in **Region → Region Info**), in which case the region administrator must approve the repeater before it appears.
    - Repeaters well outside a region's area may not be added to the map, as an anti-spam/anti-misconfiguration measure. Please check with your region's administrator.

    If your repeater or room server is also an observer, it may not "hear" its own advert.  Another observer must be within range to pick up its advert and display it on the map. If there are no other observers nearby, you can relay the repeater's advert from a companion by using the MeshCore app, select the ellipses beside the repeater, select "Share", and then select "Zero Hop Advert".  When this is the case, however, this repeater will eventually become stale and get removed.  This process must be repeated regularly.

    If it still doesn't appear, contact your region's administrator.
</div>

<div id="repeater-excluded" markdown>
??? question "My repeater shows as Ambiguous."
    As a region's mesh network grows, two repeaters can end up sharing the same short ID. When MeshMapper can't tell your repeater apart from another at the ID width it advertises, it marks it **Ambiguous**, because pings can't be credited to it with certainty. See [Duplicate Repeater IDs](duplicaterepeaterid.md) for a full explanation and how to fix it.
</div>

<div id="map-slow" markdown>
??? question "The map is slow or unresponsive on my device."
    Large regions with lots of data can be demanding on older devices or slow connections. Try the following:

    - **Coverage Only Mode**: A "Switch to Coverage Only" button appears on the loading screen. This loads just the coverage grid without the interactive data, significantly reducing resource usage.
    - **Grid Mode**: Use **Simplified** (300 m squares) instead of **Detailed** (100 m) under **Grid Mode** in [Settings](layers.md#settings).
    - **Filter by time**: Use **Filter → Time → Show data from** to limit data to a recent range (e.g. Last 30 days).
</div>

<div id="unexpected-colours" markdown>
??? question "Grid squares are showing unexpected colours."
    Grid square colours depend on the active **Coverage Mode**:

    - **Standard**: Colours represent ping type (green=BIDIR, cyan=DISC/TRACE, orange=TX, purple=RX, grey=DEAD, red=DROP)
    - **Effective Coverage**: Averaged quality score (green=high quality, red=low quality)
    - **Signal Strength**: Based on SNR (green=strong, red=weak)
    - **Ping Age**: Based on data recency (green=recent, red=stale)
    - **Noise Floor**: Based on RF noise relative to each companion's baseline (green=quiet, red=loud)

    Check which mode is selected in the **Coverage Mode** section of the Layer Control.

    If data seems to be missing, also check the **Freq** radio preset in the navigation bar, **Hide Missing-Repeater Data** in Settings, and any active filters (such as **ID width**).
</div>

<div id="live-visualization-lines" markdown>
??? question "Visualize Live isn't drawing lines between some repeaters, or doesn't seem to show all packet paths."
    **Insights → Visualize Live** can only draw paths through repeaters whose ID matches exactly one repeater. Hops through **Ambiguous** repeaters (IDs shared with another repeater) are skipped, because MeshMapper can't tell which repeater was actually involved. This is the same logic used elsewhere in MeshMapper; see [The Rules](duplicaterepeaterid.md#the-rules).
</div>

<div id="no-neighbours" markdown>
??? question "I'm not seeing repeater neighbours, or the associations are old (orange)."
    MeshMapper works out a repeater's neighbours from the paths of packets its observers hear. A packet needs to travel between two or more repeaters before reaching an observer.  For example, an advert that goes directly from repeater to observer has no hops, therefore no neighbour information is available.  However, if that same advert hops to a different repeater first and then to the observer, one neighbour association can be made.  The more observers and repeaters a region has, the more neighbour information is recorded.

    Neighbour lines are **green** when seen in the last 3 days and **orange** when older; they disappear once the region's retention window closes. Repeaters can also report their neighbours directly (**blue**), or a wardriver's app can upload them (**purple**). Links to Ambiguous repeaters aren't drawn. See [Links Between Repeaters](visuals.md#links-between-repeaters).
</div>

---

## Mobile App

<div id="app-wont-connect" markdown>
??? question "The app won't connect to my MeshCore device."
    Bluetooth connections can be finicky. Try the following:

    1. Ensure Bluetooth is enabled on your phone.
    2. Make sure your MeshCore device is powered on and not connected to another app.
    3. Try toggling Bluetooth off and on again.
    4. Restart the MeshMapper app.
    5. If pairing fails repeatedly, remove the device from your phone's Bluetooth settings and re-pair.

    See the [Connection Guide](app_connection_guide.md) for detailed pairing instructions.
</div>

<div id="outside-region" markdown>
??? question "The app says I'm outside of a region."
    You need to be within a registered MeshMapper region to start a wardriving session. If there isn't a region near you, you can [request one](onboarding.md).
</div>

<div id="gps-accuracy" markdown>
??? question "GPS isn't locking or accuracy is poor."
    GPS accuracy depends on your device and environment. Try the following:

    - Ensure location permissions are granted to the MeshMapper app.
    - Move to an area with a clear view of the sky (away from tall buildings or dense tree cover).
    - Wait a minute or two for the GPS to get a solid fix before starting a session. Fixes less accurate than 50 m are rejected.
    - On Android, ensure location mode is set to "High accuracy."
</div>

---

## Administration

<div id="cant-access-admin" markdown>
??? question "I can't access the admin portal."
    The admin panel (**Region → Admin Panel** on the map) is only available to region administrators. Sign in with your My MeshMapper account, or with **Sign in with Discord**. Forgot your password? Use **Forgot password?** to reset it yourself.

    If you believe you should have access, confirm with the person who set up the region or contact a Moderator on Discord. See the [Administrator List](administratorlist.md) to find your region's admin.
</div>

<div id="observer-not-working" markdown>
??? question "Observer data isn't coming through."
    If your observer isn't forwarding data:

    1. Check that the observer device is running and connected to the MQTT broker.
    2. Verify the MQTT topic and credentials in your observer configuration.
    3. Open **Region → Observers** on the map to see if the observer is listed and when it last reported.

    See [MeshMapper MQTT Setup](mqtt-main.md) for configuration details.
</div>

---

## Getting More Help

If you can't find the answer here, there are several ways to get support:

- **Wiki**: Browse the full wiki documentation.
- **AI Bot (@MeshMapper)**: The MeshMapper AI bot on Discord can answer many questions. Send it a DM, tag it in a public message, or reply to a message and tag it.
- **Discord Community**: The MeshMapper community on Discord is knowledgeable and very helpful. Post your question in the appropriate channel and someone will be able to help you out.
- **Region Administrator**: For issues specific to your region (settings, configuration, etc.), reach out to your [region's administrator](administratorlist.md). If they're unavailable, tag a `@Moderator` in the MeshMapper Discord server. Moderators (also known as Global Administrators) have access to assist any region.

### Reporting Bugs

Notice a bug? You can submit a ticket using the guided form on the [Report Bugs & Features](reportbugs.md) page, or tag the MeshMapper AI bot on Discord with **`!bug`** followed by a description.

### Feature Requests

MeshMapper was built using suggestions from the community. If you have an idea, tag the AI bot with **`!feature`** followed by your suggestion, or submit it through the website or mobile app.

> Due to the size and activity of the community, these are the **only methods** to submit tickets. The developers may miss the request if sent any other way.
