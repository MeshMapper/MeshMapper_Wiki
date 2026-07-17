# Map Layers & Filters

The MeshMapper map interface offers various layers and filtering options to customize how data is visualized. This allows users to switch between different map styles, toggle specific data types, and drill down into the data based on time, power, or equipment.

## Base Layers

You can switch between different underlying map styles using the **Layer Control** (stack icon) in the top-right corner of the map, under **Map Mode**.

  - **Standard**: The default view (OpenFreeMap "Liberty" vector style). Best for general navigation and street names.
  - **Bright**: A brighter vector style variant.
  - **Dark Mode**: A high-contrast dark theme. Ideal for low-light viewing or when you want the coloured data points to stand out clearly.
  - **Topographic**: Displays terrain features, elevation lines, and hill shading. Extremely useful for understanding line-of-sight (LOS) obstructions between repeaters.
  - **Satellite** / **Google Satellite** / **Google Hybrid**: Aerial imagery (with street labels in Hybrid). Useful for verifying physical locations, tree cover, and landmarks.

*Note: Your selected base layer is saved in your browser and will be remembered the next time you visit. Selecting a dark or satellite base automatically switches the interface to dark mode.*

## Settings & Preferences

The **Settings** menu (gear icon in the navigation bar) provides global options for the interface:

*   **Theme**: Toggle between **Light Mode** and **Dark Mode**.
    *   *Note: Switching to Dark Mode will automatically change the Base Layer to the "Dark Mode" map style.*
*   **Units**: Switch between **Metric** (m/km) and **Imperial** (ft/mi). This setting applies to:
    *   Distance measurements on connection lines.
    *   Maximum range calculation.
    *   Leaderboard statistics.
    *   Filter panel distance filters.
*   **Grid Mode**: Switch between **Simplified** and **Detailed** modes. **Simplified** (default) uses **300m** grid squares, merges cells, and clusters repeaters at wide zoom levels — it loads faster. **Detailed** uses **100m** grid squares with finer coverage detail and non-grouped repeaters. The coverage grid is rendered from cached vector tiles, so the cell size is fixed by the chosen mode at every zoom level.
*   **Info Panel**: Switch between **Sidebar** and **Popup** mode for viewing ping details.
*   **Hide Data from Missing Repeaters**: When enabled, hides coverage grid squares that reference repeaters no longer present on the map, reducing visual noise from outdated or removed infrastructure.
*   **Follow My Location**: When enabled, the map continuously tracks your GPS position and re-centres on it every 5 seconds. Your current zoom level is preserved — only the centre point updates. A blue dot and accuracy circle show your position. Useful for wardriving or moving through a coverage area. Toggle it off to stop tracking; the marker stays at your last known position.
*   **Default Zoom**: Set a preferred zoom level that the map loads at. Options range from Street (14) to Region (8).

### My Location

The **My Location** button (crosshair icon on the right side of the map) performs a one-time GPS lookup and centres the map on your current position. This works independently of the Follow My Location setting — it's a quick "where am I?" without continuous tracking.

### Accessibility

*   **Colour Vision**: Choose a colour palette optimised for your vision type. The setting is found under **Settings > Accessibility > Colour Vision**. Available options:
    *   **Default** — Standard colours (unchanged).
    *   **Protanopia** (Red-blind) — Optimised for red-green colour vision deficiency.
    *   **Deuteranopia** (Green-blind) — Same palette as Protanopia (both are red-green CVD).
    *   **Tritanopia** (Blue-blind) — Optimised for blue-yellow colour vision deficiency.
    *   **Achromatopsia** (Monochrome) — Greyscale palette for total colour blindness.

    Palettes are based on Wong 2011 colourblind-safe colours. When a palette is selected, all coverage grid squares, repeater markers, signal strength indicators, legend colours, summary stats, charts, and gradient layers (Effective Coverage, Signal Strength, Ping Age) update automatically. The setting is saved in your browser and persists across sessions.

### Effective Coverage

*   **Colour Spectrum**: Toggle between **Red → Green** (default) and **Red → Blue** (full spectrum) for the Effective Coverage layer.
*   **Min Sample Size**: Set the minimum number of pings required in a grid square before it is displayed on the map (default: 1). Increasing this value filters out grid squares with limited data, giving a cleaner view of well-sampled areas.

### Grid Transparency

*   **Normal Opacity**: Adjust the fill opacity of coverage grid squares (default: 60%).
*   **Faded Opacity**: Adjust the opacity of grid squares that are faded into the background, such as when the Repeater Neighbours layer is active (default: 15%).

### Line Transparency

*   **Line Opacity**: Adjust the opacity of all lines drawn on the map — including repeater neighbour lines, repeater-to-grid-square lines, and ping-to-repeater lines (default: 100%).

## Overlay Layers

These layers display the actual mesh network data. You can toggle them on or off individually to reduce clutter.

| Layer Name | Description |
| --- | --- |
| **BIDIR** | **Green** grid squares showing confirmed two-way coverage (the sender heard a repeat AND the packet was also heard by at least one observer after being repeated). |
| **TX** | **Orange** grid squares where packets were sent but no confirmation was received (no repeat heard by the sender but the packet was repeated and heard by at least one observer). |
| **RX** | **Purple** grid squares where other repeated mesh traffic was heard by the meshmapper companion. |
| **DISC / TRACE** | **Cyan** grid squares showing Node Discovery and Trace packets. |
| **DEAD** | **Grey** grid squares where a repeater heard the ping, but it didn't route further (sender heard a repeat but no observer did). |
| **DROP** | **Red** grid squares showing failed pings (neither the sender nor any observers heard repeats of the packet). |
| **Repeaters** | The icons representing repeater nodes. |
| **Repeater Coverage** | When a repeater is clicked, this layer draws dashed blue lines to all locations where that repeater was heard. Useful for visualizing the effective footprint of a specific repeater. |
| **Adv. Repeater Coverage** | Similar to standard Repeater Coverage, but colour-codes the lines and grid squares based on the connection type (Green=BIDIR, Orange=TX, etc.) instead of using a uniform blue. Lines are labelled as **In** or **Out** to indicate whether the ping originated inside or outside the region boundary. |
| **Repeater Neighbours** | Draws lines between repeaters that have heard each other directly, with full support for multi-byte repeater identification. When enabled, coverage pings fade into the background to make the neighbour lines easier to trace. Lines older than 7 days are automatically hidden. <br> - **Green Dashed**: Heard recently (&le; 3 days). <br> - **Orange Solid**: Heard 4-7 days ago. |
| **Effective Coverage** | Filters the map to show only locations with confirmed reliable connectivity, removing noise and edge-case pings for a cleaner view of where the mesh truly delivers. Each ping type is given a numerical value (BIDIR being the highest and DROP being the lowest) and these values are averaged across each grid square.|
| **Signal Strength** | Colour-codes coverage grid squares by signal strength (SNR), making it easy to identify strong and weak zones across the map at a glance. ≤ -1 dB displays in red and ≥ 5 dB in green, with everything else in between. |
| **Ping Age** | Colour-codes grid squares based on how recently they were last pinged. Green indicates recent activity and red indicates stale coverage. The green and red age thresholds are adjustable from the Settings panel, making it easy to identify areas that may need remapping. |
| **Noise Floor** | A coverage mode that colour-codes grid squares by RF noise level. **Green** = quiet, **Red** = loud. Select it from the **Coverage Mode** section. See [Noise Floor](#noise-floor) below for details. |
| **Neighbor Zones** | Small pins showing the location of nearby MeshMapper regions. Clicking them will take you to that map. |
| **Neighbour Zone Boundaries** | Draws a dashed outline showing the official boundary (polygon or radius) of each neighbouring region. Requires **Neighbor Zones** to be enabled — it will be automatically turned off when Neighbor Zones is disabled, and restored when it is re-enabled. |
| **Region Boundary** | A black outline showing the official area covered by the current map zone. |

### Noise Floor

The **Noise Floor** coverage mode visualizes the RF noise environment across the map by colour-coding grid squares. It helps identify areas with high interference versus quiet areas with clean signal conditions.

#### What It Shows

Every companion reports a **noise floor** reading (in dBm) with each ping it submits. The noise floor represents the level of background RF interference the radio is experiencing at that location. A reading closer to 0 dBm is "loud" (lots of interference), while a very negative value like -120 dBm is "quiet."

Because different radios and antennas report different absolute noise values, MeshMapper doesn't display the raw readings directly. Instead, it calculates a **noise delta** — how much louder or quieter a location is compared to that device's baseline.

#### How Calibration Works

MeshMapper automatically calibrates each companion's baseline:

1. After enough data has been collected (at least 5 readings), MeshMapper calculates the companion's **10th percentile** noise floor — essentially the quietest conditions that companion typically experiences.
2. This becomes the companion's **baseline**.
3. Every data point is then scored as a **delta** (difference) from that baseline.
4. Every day a new calibration is done to update that companion's noise delta.

For example, if your companion's baseline is **-110 dBm** and you submit a reading of **-90 dBm**, the delta is **+20** — meaning that location is 20 dB (100X) noisier than your device sees under typical quiet conditions.

This per-companion calibration ensures that readings from different hardware/setups are comparable on the same map. All readings for a single location are averaged and displayed accordingly.

#### Reading the Colours

Grid squares are colour-coded on a gradient from green to red:

| Colour | Meaning |
| --- | --- |
| **Green** | Quiet — at or near the companion's baseline noise level. |
| **Yellow** | Moderate — some elevated noise above baseline. |
| **Red** | Loud — significantly above baseline, indicating high interference. |

A **Noise Floor** legend appears in the bottom-right of the map when this mode is active, showing the gradient scale from Quiet to Loud.

Like the other coverage modes, Noise Floor fully supports the [colour vision accessibility options](#accessibility), so all colour blindness palettes apply to noise grid squares and the legend.

!!! tip
    To enable, select **Noise Floor** from the **Coverage Mode** section in the Layer Control (stack icon) in the top-right corner of the map.

### Legacy Data Layer

Regions with imported historical data will have a **Legacy** layer available. This layer displays data points uploaded via CSV but does not show connection lines or contribute to repeater statistics due to the lack of verifiable repeater association. See [Data Upload](https://wiki.meshmapper.net/dataupload/) for more details.

## Map Tools

### Line of Sight

The **Line of Sight** tool is available from the map toolbar and allows you to check terrain clearance between any number of points on the map. Click to place two (or more) points (or click directly on repeaters) and MeshMapper will fetch the elevation profile and show whether the path is clear or obstructed. When a repeater is selected as one of the endpoints, you can adjust its elevation above ground for more accurate results.

### Coverage Timeline

The **Coverage Timeline** tool provides an animated playback of how a region's coverage has grown over time, from the region's earliest data to the present day. It is available from the **Map Tools** (wrench icon) control.

When activated, a playback bar appears at the bottom of the screen with controls to:

- **Play/Pause** — automatically advance the timeline
- **Scrub** — drag the slider to jump to a specific point in time
- **Speed** — click the speed label to cycle through playback speeds (0.5x, 1x, 2x, 4x)

The playback runs on the live vector coverage data, so you can watch coverage fill in as wardrivers contributed data over weeks and months.

### 3D Terrain

The **3D Terrain** control (landscape icon at the top of the map controls) drapes the map — including all coverage data — over real elevation terrain:

- **Enable 3D** — Toggles the terrain on or off
- **Hillshade relief** — Adds shaded relief for depth
- **Exaggeration** — A slider (0.5×–2.5×) to emphasize elevation differences
- **Tilt/rotate** the view by right-dragging (or ctrl-dragging) the map

3D terrain makes it much easier to see how hills and valleys shape your region's RF coverage.

### Packet Analyzer

The **Packet Analyzer** provides a real-time view of raw MeshCore packets flowing through the region's MQTT observers. It is accessible from the map toolbar. The analyzer can be opened in a new tab for a full-screen experience using the pop-out button.

The **Live Visualization** mode (accessed via the "Visualize Live" button in the analyzer) draws animated lines on the map showing how packets are moving through the region's repeaters in real time.

## Linking to a Specific Location

You can open a region's map pre-centred on an exact spot by adding `lat`, `lon`, and (optionally) `zoom` query parameters to its URL. This is useful for sharing a precise location — a specific repeater site, a coverage gap, or a spot you want someone else to look at — without them having to pan and zoom to find it.

```
https://[IATA].meshmapper.net/?lat=45.4034&lon=-75.7258&zoom=15
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `lat` | float | Region centre | Latitude to centre the map on (−90 to 90). |
| `lon` | float | Region centre | Longitude to centre the map on (−180 to 180). |
| `zoom` | integer | `13` | Map zoom level. Clamped to the 3–19 range. |

**Example — open the YOW map centred on Parliament Hill at zoom 16:**

```
https://yow.meshmapper.net/?lat=45.4236&lon=-75.7009&zoom=16
```

!!! note
    - Both `lat` and `lon` must be present and valid for the deep link to take effect. If either is missing or out of range, the map ignores it and loads normally at the region's default view.
    - The deep-link position is preserved even after the coverage data finishes loading — the map will not snap back to the region's default extent.
    - A `lat`/`lon` deep link takes precedence over the `location` place-name search (below).

!!! tip
    To share a read-only, embeddable version of the map at a fixed location instead, see [Map Embedding](embedding.md) — it accepts the same `lat`/`lon`/`zoom` parameters on the `embed.php` view.

### Searching by Place Name

If you don't have exact coordinates, append `location=` with a place name or address instead. The map geocodes it and centres there on load:

```
https://yow.meshmapper.net/?location=Parliament%20Hill,%20Ottawa
```

If both are supplied, an explicit `lat`/`lon` deep link always wins over `location`.

## Search & Filters

The search functionality combines quick lookups with powerful filtering options.

### Filter Map Data
Clicking the **Filter** pill (tune icon) in the navigation bar opens the **Filter Map Data** panel. Filters are applied server-side — the coverage grid, click popups, charts, and ping history all reflect the same filtered dataset. Active filters appear as removable chips, and the Filter pill shows a count and lights up cyan while filters are active.

  - **Time**:
    - **Show data from**: All time, Last 30 days, Last 90 days, or Last year.
    - **From date / To date**: Specify a custom date range.
  - **Signal**:
    - **Transmit power**: Any power, 0.3 W, 0.6 W, or 1.0 W.
    - **Radio config**: Filter by the radio preset (frequency / bandwidth / SF / CR) the wardriver's device reported — useful in regions where multiple radio configurations are in use.
    - **Min / Max signal**: Filter pings by Signal-to-Noise Ratio (dB).
  - **Location**:
    - **Min / Max distance**: Filter pings by distance from the heard repeater (in your selected units).
  - **Repeaters**:
    - **Repeater name or ID**: Show only specific repeaters by name or hex ID.
    - **Hops away**: Filter by hop count (1, 2, or 3 hops).
    - **Ping mentions repeater**: Find pings that routed through or were heard from a specific repeater by its name or ID. This filter automatically excludes pings associated with duplicate repeater IDs or known collisions and displays a warning message when this occurs.
    - **Only external antennas**: Show only data points collected with an external antenna.
    - **Only repeaters with the wrong time**: Show only repeaters whose embedded clock is off by more than 120 seconds. Useful for identifying repeaters that need their time set correctly.
  - **User**:
    - **User name**: Filter pings by the (full or partial) username of the wardriver (if enabled for the region).

!!! tip "Filters preserve your map position"
    Applying, resetting, or changing filters no longer resets the map to its default centre and zoom. Your current view is preserved so you can refine filters while staying focused on a specific area.

## Coverage Only Mode

For users on older hardware, mobile devices with limited resources, or slow internet connections, MeshMapper offers a **Coverage Only Mode**.

  - **How it works**: Instead of the full interactive interface, this mode loads just the coverage grid as lightweight map tiles from the server, skipping repeaters, popups, and all the interactive machinery.
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
