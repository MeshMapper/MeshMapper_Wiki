# Map Layers & Filters

This page walks through everything on a region map: the menus, map styles, coverage modes, overlays, tools, settings and filters.

## The Navigation Bar

| Item | What it does |
| --- | --- |
| **Switch Region** | Jump to another region or multiregion group. Type a city or code to search. |
| **Freq** | Show only pings, repeaters and links on one radio preset (frequency / bandwidth / SF). **All** is the default. Pings from before June 2026 carry no preset and only appear under **All**. |
| **Active Wardrivers** (car icon) | How many wardrivers had an active session when the page loaded. |
| **Filter** | Opens [Filter Map Data](#filters). Shows a count while filters are active. |
| **Region** | Region Info (admins, links, radio presets, settings), Contact Region, Repeater IDs, Repeater List, Observers, Leaderboard and Admin Panel. |
| **Insights** | The packet [Analyzer and Visualize Live](#insights). |
| **Settings** (gear) | Light / Dark Mode toggle, and **Settings** for the options under [Settings](#settings). |

## Base Layers

Switch map styles from the **Layer Control** (stack icon, top-right) under **Map Mode**:

  - **Standard**: The default (OpenFreeMap "Liberty"). Best for general navigation and street names.
  - **Bright**: A brighter variant.
  - **Dark Mode**: A high-contrast dark style that makes coverage stand out.
  - **Topographic**: Terrain, elevation lines and hill shading. Useful for spotting line-of-sight obstructions.
  - **Satellite** / **Google Satellite** / **Google Hybrid**: Aerial imagery (Hybrid adds street labels). Useful for checking sites, tree cover and landmarks.

Your choice is remembered in your browser. Turning on Dark Mode from the Settings menu also switches the map to the Dark Mode style.

## Coverage Modes

Under **Coverage Mode** in the Layer Control, pick how coverage grid squares are coloured:

| Mode | Colours grid squares by |
| --- | --- |
| **Standard** | Ping type (BIDIR, TX, RX, and so on). The default. |
| **Effective Coverage** | How reliable coverage is. Each ping type gets a score (BIDIR 3, TX / RX / DISC 2, DEAD 1, DROP 0), averaged per grid square. |
| **Signal Strength** | Signal-to-noise ratio (SNR): ≤ -1 dB is red, ≥ 5 dB is green. |
| **Ping Age** | How recently the square was pinged: green under 30 days, red over 90 days (adjustable in [Settings](#settings)). |
| **Noise Floor** | Background RF noise: green is quiet, red is loud. See [Noise Floor](#noise-floor). |

### Ping Types

In **Standard** mode, the **Coverage** group lets you turn each ping type on or off. It's greyed out in the other modes.

| Type | Colour | Meaning |
| --- | --- | --- |
| **BIDIR** | Green | Heard repeats from the mesh **and** successfully routed through it. |
| **TX** | Orange | Successfully routed through, but no repeats heard back. |
| **RX** | Purple | Heard mesh traffic but did not transmit. |
| **DISC/TRACE** | Cyan | A discovery or trace reply was heard. |
| **DEAD** | Grey | A repeater heard it, but no other radio received the repeat. |
| **DROP** | Red | No repeats heard **and** no successful route. |

See [Ping Types Defined](visuals.md#ping-types-defined) for more detail.

### Noise Floor

Every companion reports a **noise floor** reading (in dBm) with each ping: the level of background RF interference at that spot. Closer to 0 dBm is loud; very negative (e.g. -120 dBm) is quiet.

Different radios report different absolute values, so MeshMapper shows a **noise delta** instead: how much louder a spot is than that companion's usual baseline.

  1. Once a companion has at least 5 readings, its **baseline** is its 10th-percentile reading (roughly the quietest conditions it sees).
  2. Each reading is scored as the difference from that baseline.
  3. Baselines are recalculated regularly.

For example, with a baseline of **-110 dBm**, a reading of **-90 dBm** is **+20 dB**: 100× noisier than usual. Readings in the same grid square are averaged.

A **Noise Floor** legend (Quiet → Loud) appears in the bottom-right while this mode is on.

## Overlays

Toggle these in the Layer Control. Some may be greyed out as **Disabled by Administrator** in regions that hide them.

| Overlay | What it shows |
| --- | --- |
| **Repeaters** | Repeater chips, each with its hex ID and state. See [Repeaters](visuals.md#repeaters). |
| **Repeater Coverage** | Click a repeater to see where it was heard: grid squares and dashed lines coloured by ping type (DROP is left out). With this overlay off, the squares show in plain blue with no lines. |
| **Repeater Neighbours** | Lines between repeaters that reach each other. **Green**: seen in a packet path in the last 3 days. **Orange**: seen longer ago. **Blue**: reported by the repeater. **Purple**: uploaded from the app. Coverage fades while this is on. See [Links Between Repeaters](visuals.md#links-between-repeaters). |
| **Repeater Scopes** | Which repeaters carry a mesh scope, and the links between them. See [Repeater Scopes](#repeater-scopes). |
| **Backbone** | The repeaters and links that carry half of the region's traffic, in **gold**. Only backbone repeaters are shown while it's on. See [Backbone](backbone.md) for how it's calculated. |
| **Neighbour Zones** | Pins for nearby MeshMapper regions. Click one to open that map. |
| **Neighbour Zone Boundaries** | Dashed outlines of nearby regions. Needs **Neighbour Zones** on. |
| **Region Boundary** | This region's boundary (black, or white on dark and satellite maps). |

Only one of **Repeater Neighbours**, **Repeater Scopes** and **Backbone** can be on at a time. Turning one on turns the others off.

### Repeater Scopes

MeshCore repeaters can be set up with named **scopes** (e.g. `yow`). A message tagged with a scope is only forwarded by repeaters that carry that scope. **✱ Not set** means the repeater only passes messages with no scope.

Turn on **Repeater Scopes** and pick a scope from the bar at the bottom of the map. The map shows only the repeaters that carry it, and draws a link between two of them when both carry it. The bar shows how many repeaters and links match.

MeshMapper learns a repeater's scopes three ways:

  - **I** (Inferred): seen forwarding traffic in that scope.
  - **R** (Reported): the repeater listed it when an observer asked.
  - **U** (Uploaded): a wardriver's app asked the repeater and uploaded its answer.

A **★** marks the repeater's default scope (the one on its own adverts). Repeaters with firmware older than v1.12 can't answer scope queries.

To check whether a scope name is in use in your region, use the [Scope Finder](#scope-finder).

## Map Tools

Open **Map Tools** (the tools icon on the map). One tool is open at a time.

### Line of Sight

Check terrain clearance between two or more points.

  1. Click the map or a repeater to place points **A** and **B** (or type coordinates). Use **Add Point** for more.
  2. Set each point's **Height** above ground. Points placed on a repeater start at 3 m.
  3. Check the **Freq** (defaults to your region's most-used frequency).
  4. Click **Calculate**.

The result shows the elevation profile (with earth curvature) and the first Fresnel zone, and rates each leg: **Line of Sight CLEAR**, **Minor Fresnel Intrusion**, **Fresnel Zone Partially Blocked** (less than 60% clear) or **Line of Sight OBSTRUCTED**. On the map, green is clear and red is blocked.

### Antenna Coverage

Estimate how far a radio at a spot could reach, using terrain.

  1. Tap the map (or a repeater) to place the pin.
  2. Pick the transmit **power** (14–30 dBm, default 22) and set the **TX** and **RX heights** (defaults 6 m and 2 m). The frequency is set from your region's most-used band.
  3. Optionally open **Advanced** for sensitivity, spreading factor, antenna gains, cable loss, fade margin and environment. The defaults suit most setups.

The map shades **Strong** (red), **Likely** (orange) and **Fringe** (yellow) areas, and shows how far each reaches plus the approximate area covered.

!!! note
    This is an estimate from bare-ground terrain. Buildings, trees, antennas and weather all change real-world range. Treat it as a guide, not a guarantee.

### Coverage Timeline

An animated playback of how the region's coverage grew, from its earliest data to today. A playback bar at the bottom lets you **Play/Pause**, **drag** to jump to a date, and click the speed to cycle **1x → 2x → 4x → 0.5x**.

### Scope Finder

Test whether a scope name is used in your region. Type the name (e.g. `yow`) and click **Find**. MeshMapper checks it against the region's recent scoped traffic and tells you whether it's already tracked, found, only weakly matched, or not found. If a scope is found but not yet monitored, a region admin can add it under **Repeaters, Neighbours & Scopes** in the admin panel.

### 3D Terrain

The **3D Terrain** control (landscape icon, top of the map controls) drapes the map and coverage over real terrain.

  - **Enable 3D**: turn terrain on or off.
  - **Hillshade relief**: add shaded relief.
  - **Exaggeration**: 0.5× to 2.5× (default 1.4×).
  - Right-drag (or Ctrl-drag) to tilt and rotate.

### My Location

The **Show My Location** button (top-right) finds your position once and zooms to it. For continuous tracking, turn on **Follow My Location** in [Settings](#settings).

## Insights

The **Insights** menu has two packet tools:

  - **Analyzer**: opens the MeshMapper packet analyzer for this region in a new tab, showing raw packets heard by the region's observers.
  - **Visualize Live**: animates packets on the map in real time. Each packet is an orange dot that travels its actual path through the repeaters to the observer that heard it, and repeaters flash as it passes. Click **Exit Live Visualization** to stop.

## Settings

Open **Settings** from the gear menu. Settings are saved in your browser.

### Map Display

  - **Units**: **Metric** (m/km) or **Imperial** (ft/mi). Applies to distances on the map, filters and leaderboards.
  - **Grid Mode**: **Simplified** (default) uses 300 m grid squares, merges cells and groups repeaters at wide zoom, and loads faster. **Detailed** uses 100 m grid squares and shows every repeater. Changing it reloads the page.
  - **Default Zoom**: the zoom the map opens at, from **14 - Street** to **8 - Region**.
  - **Info Panel**: show details in a **Sidebar** or a **Popup**.

### Map Behaviour

  - **Hide Missing-Repeater Data**: hide pings from repeaters no longer on the network.
  - **Follow My Location**: keep the map centred on your GPS position (updated every 5 seconds, keeping your zoom). A blue dot and accuracy circle show where you are.

### Accessibility

**Colour Vision** changes the colours used across the map (grid squares, repeaters, lines, legends, charts and coverage modes):

  - **Default**
  - **Protanopia (Red-blind)**
  - **Deuteranopia (Green-blind)**: same palette as Protanopia.
  - **Tritanopia (Blue-blind)**
  - **Achromatopsia (Monochrome)**

### Effective Coverage

  - **Colour Spectrum**: **Red → Green** (default) or **Red → Blue**.
  - **Min Sample Size**: hide grid squares with fewer pings than this (1–20, default 1).

### Ping Age

  - **Green (under)**: squares pinged more recently than this are green (default 30 days).
  - **Red (over)**: squares older than this are red (default 90 days).

### Transparency

  - **Normal Opacity**: coverage grid squares (default 60%).
  - **Faded Opacity**: grid squares faded into the background, e.g. behind Repeater Neighbours (default 15%).
  - **Line Opacity**: all lines on the map (default 100%).

## Filters

Click **Filter** in the navigation bar to open **Filter Map Data**. Filters apply everywhere: grid squares, popups, charts and ping history. Active filters show as removable chips, and applying them keeps your current map view.

  - **Time**
    - **Show data from**: All time, Last 30 days, Last 90 days or Last year.
    - **From date / To date**: a custom date range.
  - **Signal**
    - **Transmit power**: Any power, 0.3 W, 0.6 W or 1.0 W.
    - **Min / Max signal**: signal-to-noise ratio (dB).
  - **Location**
    - **Min / Max distance**: distance between the ping and the repeater (in your units).
  - **Repeaters**
    - **Repeater name or ID**: show only matching repeaters.
    - **ID width**: pings whose path uses 1-, 2- or 3-byte repeater IDs. This is not the number of hops.
    - **Ping mentions repeater**: pings that went through or were heard from a repeater. Pings where that repeater's ID is ambiguous are left out.
    - **Repeater Scope**: repeaters carrying a scope (only shown when the region has scopes).
    - **Only external antennas**: pings collected with an external antenna.
    - **Only repeaters with the wrong time**: repeaters whose clock is off by more than 120 seconds.

To filter by radio preset, use **Freq** in the navigation bar.

## Sharing a Map View

The address bar updates as you move around and change layers, so copying the URL shares exactly what you see. Repeater and ping popups also have a **Copy Link** button.

You can also build links by hand:

```
https://yow.meshmapper.net/?lat=45.4236&lon=-75.7009&zoom=16&m=sat&l=rep.nbr.rb
```

| Parameter | What it does |
| --- | --- |
| `lat`, `lon` | Centre the map here. Both are needed. |
| `zoom` | Zoom level, 3–19 (default 13). Decimals work. |
| `location` | A place name or address to look up and centre on (zoom 15), e.g. `location=Parliament%20Hill,%20Ottawa`. `lat`/`lon` win if both are given. |
| `m` | Base map: `std`, `brt`, `dark`, `topo`, `sat`, `gsat` or `ghyb`. |
| `l` | Overlays to turn on, separated by dots: `rep` Repeaters, `rcov` Repeater Coverage, `nbr` Repeater Neighbours, `sc` Repeater Scopes, `bb` Backbone, `nz` Neighbour Zones, `nzb` Neighbour Zone Boundaries, `rb` Region Boundary. Anything left out is off. |
| `cm` | Coverage mode: `std`, `eff`, `sig`, `age` or `noise`. |
| `preset` | Radio preset: `all`, or `freq,bw,sf` (e.g. `910.525,62.5,7`). |
| `repeater` | Open a repeater by its ID or full public key. |
| `ping` | Open the grid square at `lat,lon`. |
| `repeater_list`, `repeater_ids`, `observers` | Open that list on load. |
| `live` | Start Visualize Live on load. |
| `coverage-only` | Open in [Coverage Only Mode](#coverage-only-mode). |

Settings from a link only apply to that visit; they don't change your saved preferences.

!!! tip
    To embed a read-only map in another site, see [Map Embedding](embedding.md).

## Coverage Only Mode

For older devices or slow connections, **Coverage Only Mode** loads just the coverage grid as lightweight tiles.

  - **How to open it**: click **Switch to Coverage Only** on the loading screen, or add `?coverage-only` to the map's URL.
  - **What you lose**: no overlays, no clicking on grid squares, no filters, and no Map Tools or 3D. Base maps and My Location still work.
  - **To leave**: click **Exit Coverage Only**.

## Private Repeaters

Repeater owners can hide a repeater's location by adding the "no entry" emoji (🚫) to the start or end of its name.

  - **Map**: the repeater isn't drawn. It's listed as **Hidden** in the Repeater IDs list, so its ID isn't reused by mistake.
  - **Pings**: coverage is kept, but the repeater shows as **(hidden)** with no lines or distances.
  - **Leaderboards**: the name shows as "(private repeater)", but its stats still count.
