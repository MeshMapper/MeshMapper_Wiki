# Map Embedding

MeshMapper provides an embeddable, read-only version of the map that you can place on your own website, forum, or dashboard. The embed is a lightweight view with no controls or popups — just the map, coverage grid, and repeater markers.

## Embed URL

The base URL for any region's embed is:

```
https://[IATA].meshmapper.net/embed.php
```

For example, to embed the **YOW** region:

```
https://yow.meshmapper.net/embed.php
```

## Basic Usage

Add the embed to your site using an HTML `<iframe>`:

```html
<iframe
  src="https://yow.meshmapper.net/embed.php"
  width="100%"
  height="400"
  style="border: none;"
  loading="lazy">
</iframe>
```

## URL Parameters

All parameters are optional and appended as query strings (e.g., `?lat=45.4&lon=-75.7&zoom=14`).

### Map Position

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `lat` | float | Region center | Latitude to center the map on. |
| `lon` | float | Region center | Longitude to center the map on. |
| `zoom` | integer | `12` | Map zoom level (1–19). Ignored if `meters` is set. |
| `meters` | integer | — | Sets the zoom level so that the given number of meters fits across the map width. Overrides `zoom`. |

### Layer Visibility

Toggle layers on or off with `1` (show) or `0` (hide).

| Parameter | Layer | Default |
| --- | --- | --- |
| `cov_grid` | Bidirectional coverage (green) | `1` (on) |
| `part_grid` | TX Only coverage (orange) | `1` (on) |
| `rx_grid` | RX coverage (purple) | `1` (on) |
| `disc_grid` | Discovery coverage (cyan) | `1` (on) |
| `drop_grid` | Dead coverage (grey) | `1` (on) |
| `fail_grid` | Dropped packets (red) | `0` (off) |
| `repeaters` | Repeater markers | `1` (on) |
| `rep_coverage` | Repeater max-range circles | `0` (off) |
| `grid_lines` | Grid outline lines | `0` (off) |

### Other Options

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `geofence` | `0` or `1` | Auto | Limits loaded data to a 5 km radius. Turns on automatically when `lat`/`lon` are provided. `geofence=0` turns it off. `geofence=1` forces it on around the region centre. |
| `cvd` | string | `none` | Colour vision palette: `none`, `protanopia`, `deuteranopia`, `tritanopia` or `achromatopsia`. |
| `preset` | `freq,bw,sf` | all | Show only one radio preset, e.g. `?preset=910.525,62.5,7`. Leave it out, or use `all`, to show everything. |
| `dir` | any value | off | With `lat`/`lon`, shows a car icon at the centre of the map (e.g. `&dir=1`). |

## Examples

**Center on a specific location at zoom 14:**

```
https://yow.meshmapper.net/embed.php?lat=45.4034&lon=-75.7258&zoom=14
```

**Show a 2 km wide view with only bidirectional coverage:**

```
https://yow.meshmapper.net/embed.php?lat=45.4034&lon=-75.7258&meters=2000&part_grid=0&rx_grid=0&disc_grid=0&drop_grid=0
```

**Load all region data (no geofence) centered on a point:**

```
https://yow.meshmapper.net/embed.php?lat=45.4034&lon=-75.7258&geofence=0
```

## Notes

- The embed is **read-only** — there are no interactive popups, layer toggles, or controls.
- A small "Open on **MeshMapper**" link appears in the bottom-left corner, linking viewers to the full map.
- When `lat` and `lon` are provided, the embed automatically geofences data to a 5 km radius for faster loading. Use `geofence=0` to override this.
- The embed needs a browser with WebGL.

---

## Repeater ID Grid

Use this grid to check whether a repeater ID prefix is available, already deployed, in conflict, or reserved. Open a cell to inspect its current status before choosing a prefix for a new repeater.

You can also embed the Repeater ID Usage grid — a 16×16 visual showing which first-byte repeater IDs are available, deployed, in conflict, or reserved in a region.

### Embed URL

```
https://[IATA].meshmapper.net/embed_repeaters.php
```

### Basic Usage

```html
<iframe
  src="https://yow.meshmapper.net/embed_repeaters.php"
  width="100%"
  height="500"
  style="border: none;"
  loading="lazy">
</iframe>
```

### URL Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `mode` | `light` or `dark` | `light` | `mode=dark` starts in dark mode; anything else starts in light mode. Users can also switch modes with the button in the header. |
| `preset` | `freq,bw,sf` | all | Show only one radio preset, e.g. `?preset=910.525,62.5,7`. Leave it out, or use `all`, to show everything. |

### Example

**Embed the repeater grid in dark mode:**

```
https://yow.meshmapper.net/embed_repeaters.php?mode=dark
```

### What's in the Grid

The embed shows a **Repeater ID Usage** header, a search box, and filter chips: **All**, **MB**, **Ambiguous**, **2-Byte**, **3-Byte** and **No Location**.

Cell colours:

- **Green**: available
- **Blue**: deployed
- **Red**: conflict
- **Dark**: reserved

### Notes

- Clicking a grid cell opens a popup showing whether the ID prefix is available, deployed, in conflict, or reserved, along with the repeater(s) that occupy it.
- A "View on **MeshMapper**" link at the bottom opens the full repeater list on the region's map.
- The grid works in every region. Conflicts take into account whether each repeater supports multi-byte IDs.
