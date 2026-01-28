# Map Layers & Filters

The MeshMapper map interface offers various layers and filtering options to customize how data is visualized. This allows users to switch between different map styles, toggle specific data types, and drill down into the data based on time, power, or equipment.

## Base Layers

You can switch between different underlying map styles using the **Layer Control** (stack icon) in the top-right corner of the map.

  - **Standard**: The default view. Best for general navigation and street names.
  - **Topographic**: Displays terrain features, elevation lines, and hill shading. Extremely useful for understanding line-of-sight (LOS) obstructions between repeaters.
  - **Dark Mode**: A high-contrast dark theme. Ideal for low-light viewing or when you want the colored data points to stand out clearly.
  - **Satellite**: Aerial imagery. Useful for verifying physical locations, tree cover, and landmarks.

*Note: Your selected base layer is saved in your browser and will be remembered the next time you visit.*

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
| **Repeater Neighbours** | Draws lines between repeaters that have heard each other directly. <br> - **Green Dashed**: Heard recently (< 2 weeks). <br> - **Orange Dashed**: Heard 2-4 weeks ago. <br> - **Red Solid**: Stale link (> 4 weeks). |
| **Noise Heatmap** | A visual heatmap representing the noise floor reported by radios. **Red** areas indicate high interference, while **Blue** areas are quieter. |
| **Neighbor Zones** | Small pins showing the location of nearby MeshMapper regions. Clicking them will take you to that map. |
| **Region Boundary** | A black outline showing the official area covered by the current map zone. |

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