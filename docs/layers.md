# Map Layers & Filters

The MeshMapper map interface offers various layers and filtering options to customize how data is visualized. This allows users to switch between different map styles, toggle specific data types, and drill down into the data based on time, power, or equipment.

## Base Layers

You can switch between different underlying map styles using the **Layer Control** (stack icon) in the top-right corner of the map.

  - **Standard**: The default view. Best for general navigation and street names.
  - **Topographic**: Displays terrain features, elevation lines, and hill shading. Extremely useful for understanding line-of-sight (LOS) obstructions between repeaters.
  - **Dark Mode**: A high-contrast dark theme. Ideal for low-light viewing or when you want the colored data points to stand out clearly.
  - **Satellite**: Aerial imagery. Useful for verifying physical locations, tree cover, and landmarks.

*Note: Your selected base layer is saved in your browser and will be remembered the next time you visit.*

## Settings & Preferences

The **Settings** menu (gear icon in the navigation bar) provides global options for the interface:

*   **Theme**: Toggle between **Light Mode** and **Dark Mode**.
    *   *Note: Switching to Dark Mode will automatically change the Base Layer to the "Dark Mode" map style.*
*   **Units**: Switch between **Metric** (m/km) and **Imperial** (ft/mi). This setting applies to:
    *   Distance measurements on connection lines.
    *   Maximum range calculation.
    *   Leaderboard statistics.
    *   Advanced Search distance filters.
*   **Detailed/Simnplified Mode**: Switch between **Detailed** and **Simplified** modes to display grid squares in more or less detail and show repeaters clustered at wide zoom levels.  Simplified mode greatly increases map loading time.

## Overlay Layers

These layers display the actual mesh network data. You can toggle them on or off individually to reduce clutter.

| Layer Name | Description |
| --- | --- |
| **BIDIR** | **Green** grid squares showing confirmed two-way coverage. |
| **TX** | **Orange** grid squares where packets were sent but no confirmation was received. |
| **RX** | **Purple** grid squares where packets were heard but no transmission occurred. |
| **DISC** | **Cyan** grid squares showing Node Discovery packets. |
| **DEAD** | **Grey** grid squares where a repeater heard the ping, but it didn't route further. |
| **DROP** | **Red** grid squares showing failed pings (no route, no repeats). |
| **Repeaters** | The icons representing repeater nodes. |
| **Repeater Coverage** | When a repeater is clicked, this layer draws dashed blue lines to all locations where that repeater was heard. Useful for visualizing the effective footprint of a specific repeater. |
| **Adv. Repeater Coverage** | Similar to standard Repeater Coverage, but color-codes the lines and grid squares based on the connection type (Green=BIDIR, Orange=TX, etc.) instead of using a uniform blue. |
| **Repeater Neighbours** | Draws lines between repeaters that have heard each other directly. <br> - **Green Dashed**: Heard recently (< 2 weeks). <br> - **Orange Dashed**: Heard 2-4 weeks ago. <br> - **Red Solid**: Stale link (> 4 weeks). |
| **Noise Heatmap** | A visual heatmap representing the RF noise environment. **Red** areas indicate high interference, while **Blue** areas are quieter. See [Noise Heatmap](#noise-heatmap) below for details. |
| **Neighbor Zones** | Small pins showing the location of nearby MeshMapper regions. Clicking them will take you to that map. |
| **Neighbour Zone Boundaries** | Draws a dashed outline showing the official boundary (polygon or radius) of each neighbouring region. Requires **Neighbor Zones** to be enabled — it will be automatically turned off when Neighbor Zones is disabled, and restored when it is re-enabled. |
| **Region Boundary** | A black outline showing the official area covered by the current map zone. |

### Noise Heatmap

The **Noise Heatmap** is an optional overlay that visualizes the RF noise environment across the map. It helps identify areas with high interference versus quiet areas with clean signal conditions.

#### What It Shows

Every companion reports a **noise floor** reading (in dBm) with each ping it submits. The noise floor represents the level of background RF interference the radio is experiencing at that location. A reading closer to 0 dBm is "loud" (lots of interference), while a very negative value like -120 dBm is "quiet."

Because different radios and antennas report different absolute noise values, MeshMapper doesn't display the raw readings directly. Instead, it calculates a **noise delta** — how much louder or quieter a location is compared to that user's personal baseline.

#### How Calibration Works

MeshMapper automatically calibrates each user's baseline:

1. After enough data has been collected (at least 5 readings), MeshMapper calculates the companions's **10th percentile** noise floor — essentially the quietest conditions that companion typically experiences.
2. This becomes the companions's personal **baseline**.
3. Every data point is then scored as a **delta** (difference) from that baseline.

For example, if your companion's baseline is **-110 dBm** and you submit a reading of **-90 dBm**, the delta is **+20** — meaning that location is 20 dB noisier than your typical quiet conditions.

This per-companion calibration ensures that readings from different hardware/setups are comparable on the same map.  All readings for a single location are averaged and displayed accordingly.

#### Reading the Colors

The heatmap uses a gradient from cool to warm colors:

| Color | Meaning |
| --- | --- |
| **Blue** | Quiet — at or near the companions's baseline noise level. |
| **Green / Lime** | Moderate — some elevated noise above baseline. |
| **Red** | Loud — significantly above baseline, indicating high interference. |

!!! tip
    The Noise Heatmap is **off by default**. Enable it from the Layer Control (stack icon) in the top-right corner of the map. It works best when zoomed in to a neighborhood or specific area of interest.

!!! note
    For privacy, heatmap coordinates are rounded to approximately 100-meter precision, so the heatmap shows general area trends rather than exact locations.

### Legacy Data Layer

Regions with imported historical data will have a **Legacy** layer available. This layer displays data points uploaded via CSV but does not show connection lines or contribute to repeater statistics due to the lack of verifiable repeater association. See [Data Upload](https://wiki.meshmapper.net/dataupload/) for more details.

## Search & Filters

The search functionality combines quick lookups with powerful filtering options.

### Advanced Search
Clicking the **Options** button (tune icon) next to the search bar opens the Advanced Search panel.

  - **Quick Time**: Filter data by age (Last 30 Days, 90 Days, 1 Year, or All Time).
  - **Tx Power**: Filter by transmit power (0.3W, 0.6W, 1.0W).
  - **Ext. Ant.**: Toggle to show only data points collected with an external antenna.
  - **User**: Filter pings by the username of the wardriver (if enabled for the region).
  - **Repeater Name / ID**: Search for specific repeaters by name or the first 2 characters of its Public ID.
  - **Ping contains repeater name or ID**: Find pings that routed through or were heard from a specific repeater by its name or ID. This filter automatically excludes pings associated with duplicate repeater IDs or known collisions and displays a warning message when this occurs.
  - **SNR Range**: Filter pings based on Signal-to-Noise Ratio (Min/Max).
  - **Distance Range**: Filter pings based on distance from the heard repeater (Min/Max meters).
  - **Date Range**: Specify a custom start and end date for the data.

## Coverage Only Mode

For users on older hardware, mobile devices with limited resources, or slow internet connections, MeshMapper offers a **Coverage Only Mode**.

  - **How it works**: Instead of loading thousands of individual data points and rendering them in the browser (which can be CPU intensive), this mode loads pre-rendered image tiles from the server.
  - **Performance**: This significantly reduces memory usage and load times, making the map usable on almost any device regardless of processing power.
  - **Limitations**:
    - **No interactivity**: You cannot click on grid squares to see pings or repeater paths.
    - **No filtering**: Advanced filters (Time, Power, User) are disabled.
    - **Simplified View**: Only the coverage grid is shown; repeaters and lines are hidden.
  - **How to access**:
    - A "Switch to Coverage Only" button will appear on the loading screen.

## Private Repeaters

Operators can opt-out of location sharing by appending the "no entry" emoji (🚫) to the end of their repeater's name.

  - **Map**: The Name, Location, and ID are removed from the map and the **Repeaters** layer.
  - **Pings**: Coverage pings are kept and visible in the grid layers, but the repeater details are masked.
  - **Leaderboards**: The name is replaced with "(private repeater)", but stats are still calculated.