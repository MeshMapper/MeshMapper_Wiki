# Map Grid, Ping Types & Popups

MeshMapper visualizes mesh coverage using a grid system, colour-coded markers, and detailed popups. This guide explains how to interpret the map data.

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

![Diagram](https://meshmapper.net/img/pingtypes.png)

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

  - **Solid Coloured Line**: Represents the signal your radio **Heard** from a repeater. The colour indicates signal strength (Green = Good, Orange = Okay, Red = Weak).
  - **Blue Dashed Line**: Represents the one-way **Via** path.
  - **Red Dashed Line**: Indicates a connection to a **Duplicate/Excluded** repeater.

### 4. Sharing

Every popup includes a **Link Icon** (chain link) in the top-right corner. Clicking this copies a direct URL to that specific grid square or ping to your clipboard, allowing you to share exact locations with others.

## Repeater Icons

The icons representing repeaters on the map change colour based on their status:

  - **Pink**: **Active**. The repeater is active and online.
  - **Orange**: **New**. The repeater was discovered by MeshMapper within the last 14 days.
  - **Grey**: **Stale / Inactive**. The repeater has not sent an advert within the predetermined timeframe (set by the regional administrators).
  - **Red**: **Ambiguous / Disabled**. The repeater's ID collides with another repeater (a duplicate), or it has been manually disabled.

## Repeater Popups

Clicking on a repeater icon opens a popup with details:

  - **Status Indicators**:
    - **Repeater Online**: The repeater has been heard from recently.
    - **New Repeater (Orange)**: First seen within the last 14 days.
    - **Stale Repeater (Grey)**: Has not been heard from in a specific timeframe set by the region administrator (e.g., 24 hours).
    - **Ambiguous (Red)**: The repeater's ID collides with another repeater at its byte width.
    - A red warning row appears if the repeater's clock is off by more than 120 seconds ("Repeater time is not set correctly").
  - **Details**:
    - **ID**: The repeater's identifier (shown at its advertised byte width), plus its power and **Advert Bytes** (the ID width the repeater advertises).
    - **First Heard**: The date the repeater was first discovered by MeshMapper.
    - **Last Heard**: The exact time the repeater was last seen by the mesh.
    - **Max Range**: The furthest distance a user has successfully connected to this repeater from.
  - **Stats & Chart**: Per-type ping counts (BIDIR / TX / RX / DISC / DEAD) and a signal-vs-distance chart built from the repeater's coverage data.
  - **Neighbours**: A list of other repeaters this node has directly communicated with recently.
  - **Add Another**: Compare mode — select additional repeaters to view their coverage side by side.
  - **Copy Link**: A link icon in the top right allows you to copy a direct URL to this repeater.

While a repeater is selected, the rest of the coverage grid dims so the selected repeater's own coverage stands out.

## Private Repeaters

If a repeater's name ends with the "no entry" emoji (🚫), it is treated as a **Private Repeater**:

  - **Map**: The repeater's Name, Location, and ID are completely removed from the map.
  - **Pings**: Coverage data is still kept and displayed on the grid, but the repeater's identity in the popup is masked as `(hidden)`.
  - **Leaderboards**: The repeater's name is replaced with "(private repeater)", though its statistics are still calculated and ranked.