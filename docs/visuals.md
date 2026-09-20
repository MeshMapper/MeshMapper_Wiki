# Understanding Visuals

MeshMapper visualizes mesh coverage using a grid system, repeater chips, connecting lines, and detailed popups. This guide explains every mark on the map, in the same order as the **Legend** card in the bottom right corner.

!!! note "Colours on this page are the Default palette"
    Every colour named below is the Default one. MeshMapper also ships four colour vision palettes (Protanopia, Deuteranopia, Tritanopia and Achromatopsia) under **Settings > Accessibility > Colour Vision**, and each of them remaps these colours. Backbone gold, for example, becomes white in all four. See the [colour vision accessibility options](layers.md#accessibility) for the full list. Where a mark also has a distinctive shape or position, this page says so, so you can find it whichever palette you use.

## The Grid System

The map is divided into small grid squares. The grid size is **300m x 300m** in Simplified mode and **100m x 100m** in Detailed mode — switch between the two via the **Grid Mode** option in the Settings panel.

Since a single grid square may contain multiple pings from different times or users, MeshMapper uses a **Priority System** to determine which colour to display. The map will always show the "best" result available for that location.

| Priority | Colour | Meaning |
| --- | --- | --- |
| **1 (Highest)** | **Green** | **BIDIR** (Bidirectional) - Confirmed two-way coverage. |
| **2** | **Cyan** | **DISC** (Discovery) - Discovery packet sent and reply heard. |
| **3** | **Orange** | **TX** (Transmit) - Message sent, but no repeat was heard. |
| **4** | **Purple** | **RX** (Receive) - Heard traffic while in RX mode. |
| **5** | **Grey** | **DEAD** - Repeater heard the ping, but it did not make it into the wider mesh |
| **6 (Lowest)** | **Red** | **DROP** - Failed ping. No repeats heard, did not make it into the wider mesh. |

*Example:* If a grid square contains 10 failed pings (Red) and 1 successful ping (Green), the square will appear **Green** to indicate that coverage is possible at that location.

## Ping Types Defined

Here is a detailed breakdown of the different coverage statuses:

  - **BIDIRECTIONAL (BIDIR)** - *Green*
    - You sent a message, it was received by a repeater, and your radio heard the repeater send it back.
    - This confirms a solid two-way link.

  - **DISCOVERY (DISC)** - *Cyan*
    - Your radio sent a specialized "Discovery" packet, and a node responded.
    - **TRACE** packets are shown as DISC as well.

  - **TRANSMIT (TX)** - *Orange*
    - Your message was successfully sent into the mesh (it reached a repeater), but your radio did not hear the confirmation repeat.
    - This often happens when you have a high-power transmitter but a lower-gain antenna for receiving, or if the repeater is far away.

  - **RECEIVE (RX)** - *Purple*
    - Your radio heard packets from the mesh (e.g., other users, telemetry), but you did not transmit.
    - Useful for mapping where the mesh can be heard, even if you cannot reach it.

  - **DEAD** - *Grey*
    - A repeater heard your signal, but the message didn't go anywhere (it wasn't repeated to the rest of the mesh).
    - This usually indicates a "Zombie" repeater, a misconfigured repeater that is receiving but not routing, or the repeater does not have a reliable connection into the wider mesh.

  - **DROP** - *Red*
    - You sent a message, but no repeaters heard it, and no route was established.
    - Indicates a dead zone or lack of coverage.

One more square colour is not a ping type at all:

  - **Selected** - *Bright Blue* (`#007bff`)
    - The grid square or ping you have clicked. It replaces that square's normal colour for as long as it is selected.

![Diagram](https://meshmapper.net/img/pingtypes.png)

## Repeaters

### Chip Anatomy

A repeater is drawn as a small dark rounded chip carrying its hex ID:

  - The **body** is always the same neutral dark slate (`#22303A`), on every state and in every colour vision palette.
  - The **state** is carried on a thick bar down the **left edge** of the chip, and on the chip's border.
  - The **ID label** is white on every state.

So the thing to scan for is the **edge colour**, not a coloured blob. There is no solid coloured dot on the map any more.

### Repeater States

| State | Edge Colour | Meaning |
| --- | --- | --- |
| **Active** | **Green** (`#2BB673`) | Heard from recently. This is the ordinary state. |
| **New** | **Pink** (`#FF4D9D`) | First seen by MeshMapper in the last 14 days. Drawn slightly larger, with a glow. |
| **Aged** | **Grey** (`#8A97A3`) | Has not sent an advert within the window its region administrator set (24 hours unless they changed it). |
| **Ambiguous ID** | **Red** (`#E0565B`) | Its ID overlaps another repeater at the width it advertises, so pings cannot be attributed to it with certainty. See [Duplicate Repeater IDs](duplicaterepeaterid.md). |
| **Backbone site** | **Gold** (`#E8B923`) | One of the repeaters carrying the most traffic. See [The Backbone](#the-backbone). |

### Observers

An **observer** is a repeater that also feeds packets to MeshMapper. Its chip carries an eye glyph (👁) in front of the ID.

The eye is a marker, not a state. It rides on top of whatever colour the chip already has, so an observer can be Active, New, Aged or Ambiguous at the same time.

### Groups

When repeaters are too close together to draw apart, they collapse into a round dark **badge**:

  - The **number** is how many repeaters are in the group. Past 1000 it is abbreviated, for example `1.4k`.
  - The **ring** around the badge is the colour of the state the most of them are in. It is whichever state is commonest, which is not necessarily more than half of them.
  - The **row of dots** underneath is one dot per state **present** in the group, so a badge with three dots holds repeaters in three different states. The dots are all the same size and say nothing about how many.

**A badge is clickable, which is not obvious.** Clicking it **fans the members out** on spider legs so you can reach a repeater buried in a stack. If the group is both large (more than 18 repeaters) and you are zoomed well out (below zoom 14), it **zooms in** instead. Either way a group can always be opened.

## Links Between Repeaters

The **Repeater Neighbours** overlay in the Layers control draws lines between repeaters that are known to reach each other. There are four kinds, and one more line that only appears when a popup is open. All of them are drawn solid, so the colour is what tells them apart.

| Line Colour | Kind | Meaning |
| --- | --- | --- |
| **Green** (`#28a745`) | Inferred, fresh | Seen next to each other in a packet path an observer heard, within the last 3 days. |
| **Orange** (`#fd7e14`) | Inferred, older | The same, but older than 3 days. The line disappears once the region's retention window closes, which is 7 days unless the region administrator changed it. |
| **Blue** (`#1e88e5`) | Reported | The repeater reported them as a direct neighbour over the air. |
| **Purple** (`#8e24aa`) | Uploaded | An admin pulled the repeater's neighbour table and uploaded it from the app. |
| **Dark Blue** (`#00008b`) | Route path | The one-way route a packet actually took. This one is drawn when you open a ping popup, not by the overlay. |

A **Reported** or **Uploaded** line takes over from an inferred one: if a pair of repeaters has a reported or uploaded link, the green or orange line for that same pair is not drawn.

!!! note "Orange means two different things"
    An orange **square** is a TX ping. An orange **line** is an older inferred neighbour link. They are unrelated.

## The Backbone

**Backbone** is an overlay you switch on in the Layers control. It answers one question: which handful of repeaters is this region actually leaning on?

The backbone is the **smallest set of repeaters whose links together carry half the region's traffic**. It is measured from inferred links, the ones observers heard, because those are the only links that carry a count. In most regions it comes out at a dozen or two sites.

### Reading the Percentages

Each backbone chip's label carries **its own share** of the region's traffic, for example `A1B2 7.4%`.

**Those shares add up.** Nine chips reading 12%, 9% and 7% are not slices of one bigger number, they sum to roughly the half that defines the backbone. This is the easiest thing on the map to misread.

The gold stamp and the percentage are shown whether or not the Backbone overlay is switched on.

### Gold Does Not Mean Healthy

Gold replaces **Active** and nothing else. A backbone repeater that is New, Aged or Ambiguous keeps its own colour and is still in the backbone set.

This is deliberate: importance must never hide health. It also means **"the gold repeaters are the backbone" is wrong**. Some backbone sites are pink, grey or red.

### Trunks

**Trunks** are the lines drawn between backbone sites. Each site keeps its three busiest links.

A trunk's colour is its **rank band** among all the trunks on the map, busiest to quietest, on a five step ramp:

| Band | Colour |
| --- | --- |
| Busiest | `#ff3b30` |
| | `#ff8c1a` |
| | `#f5b301` |
| | `#f5d06f` |
| Quietest | `#ffe9a8` |

It is a **rank, not a value**, so the colours say which trunks are busier than which, not how much traffic any of them carries. **The line width means nothing**, and the colours do not change as you pan or zoom.

### What the Overlay Does

Switching Backbone on hides every repeater that is not a backbone site, turns the Repeaters layer on if it was off, and switches Repeater Neighbours off. The two overlays cannot be on at once.

### On a Group Map

**A group is scored as one pool.** On a multi-region group map the whole group is treated like a single region, so a chip's share is its share of the group's combined traffic. A small member region ending up with two backbone sites, or none at all, is the correct answer rather than a bug.

## Signal (SNR)

Where the map colours something by signal quality, it uses three bands:

| Band | Colour | Quality |
| --- | --- | --- |
| **Over 5 dB** | **Green** (`#1e7e34`) | Strong |
| **-1 to 5 dB** | **Dark Yellow** (`#856404`) | Moderate |
| **Under -1 dB** | **Red** (`#bd2130`) | Weak |

If the signal value cannot be read, the mark is drawn in a neutral **Grey** (`#6c757d`) instead.

## Popups & Data

Clicking on a grid square opens a popup with detailed information.

### 1. Summary View

If a grid square contains multiple pings, the popup opens in **Summary View** first.
  - **Counts**: Shows the total number of pings for each type (BIDIR, TX, etc.) in that square.
  - **Averages**: Displays the Average SNR (Signal-to-Noise Ratio) and Average Noise Floor.
  - **Max Range**: Shows the furthest distance achieved from a repeater in this square.

### 2. Detail View
You can cycle through individual pings using the **<** and **>** buttons at the bottom of the popup, arranged by the newest data first.

  - **Identity**: Who sent the ping (if not hidden via region settings).
  - **Time**: Date and time of the ping.
  - **Telemetry**:
    - **Power**: Transmit power used (e.g., 0.6W).
    - **Ext. Ant**: Indicates if an external antenna was used.
  - **Path**:
    - **Heard Repeats**: A list of all repeaters your radio heard re-broadcasting your message, sorted by signal strength (SNR).
    - **Via**: The first repeaters responsible for transmitting your coverage data to MeshMapper.

### 3. Visual Lines
When a popup is open, MeshMapper draws lines on the map to visualize the connection:

  - **Solid Coloured Line**: Represents the signal your radio **Heard** from a repeater. The colour indicates signal strength (Green = Good, Dark Yellow = Okay, Red = Weak), using the [Signal (SNR)](#signal-snr) bands above.
  - **Dark Blue Line**: Represents the one-way **Via** path, also called the route path.
  - **Red Line**: Indicates a connection to a **Duplicate/Excluded** repeater. Its label reads `Duplicate` above the distance.

### 4. Sharing

Every popup includes a **Link Icon** (chain link) in the top-right corner. Clicking this copies a direct URL to that specific grid square or ping to your clipboard, allowing you to share exact locations with others.

## Repeater Popups

Clicking on a repeater chip opens a popup with details:

  - **Status Indicators**:
    - **Repeater Online**: The repeater has been heard from recently.
    - **New Repeater (Pink)**: First seen within the last 14 days.
    - **Aged Repeater (Grey)**: Has not been heard from in a specific timeframe set by the region administrator (e.g., 24 hours).
    - **Ambiguous (Red)**: The repeater's ID collides with another repeater at its byte width.
    - A red warning row appears if the repeater's clock is off by more than 120 seconds ("Repeater time is not set correctly").
  - **Details**:
    - **ID**: The repeater's identifier (shown at its advertised byte width), plus its power and **Advert Bytes** (the ID width the repeater advertises).
    - **First Heard**: The date the repeater was first discovered by MeshMapper.
    - **Last Heard**: The exact time the repeater was last seen by the mesh.
    - **Max Range**: The furthest distance a user has successfully connected to this repeater from.
  - **Stats & Chart**: Per-type ping counts (BIDIR / TX / RX / DISC / DEAD) and a signal-vs-distance chart built from the repeater's coverage data.
  - **Neighbours**: A list of other repeaters this node has been linked to, with the source of each link marked **I** (inferred), **R** (reported) or **U** (uploaded). See [Links Between Repeaters](#links-between-repeaters).
  - **Add Another**: Compare mode — select additional repeaters to view their coverage side by side.
  - **Copy Link**: A link icon in the top right allows you to copy a direct URL to this repeater.

While a repeater is selected, the rest of the coverage grid dims so the selected repeater's own coverage stands out.

## Private Repeaters

If a repeater's name ends with the "no entry" emoji (🚫), it is treated as a **Private Repeater**:

  - **Map**: The repeater's Name, Location, and ID are completely removed from the map.
  - **Pings**: Coverage data is still kept and displayed on the grid, but the repeater's identity in the popup is masked as `(hidden)`.
  - **Leaderboards**: The repeater's name is replaced with "(private repeater)", though its statistics are still calculated and ranked.
