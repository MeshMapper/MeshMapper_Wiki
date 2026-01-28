# Welcome to MeshMapper!

# Introduction

**MeshMapper** is a community-driven visualization and analytics platform designed for the **MeshCore** LoRa mesh network. It provides real-time mapping of network coverage and repeater performance, helping communities build more robust and efficient mesh networks.

## What is MeshMapper?

At its core, MeshMapper is a web-based map that aggregates data collected by users "wardriving" (or "warwalking", etc.) their local area. Unlike simple node maps that just show where a device is, MeshMapper visualizes **actual RF coverage**.

It answers critical questions for mesh operators:

  - *"Can I reach the mesh from here?"*
  - *"Which repeater is providing the best coverage?"*
  - *"Where are the dead zones in our city?"*

## Core Principals

MeshMapper was desiged to provide realistically reliable data without making assumptions

  - **Duplicate Repeaters:** If a repeater with duplicate ID is detected on the mesh (see "Duplicate Repeater IDs" on the left), coverage data is never directly associated with these repeaters.  Mapping tools will make suggestions on which repeater was actually involved, but no concrete link will ever be made.
  - **Association:** For every data point, repeaters involved in its transmission are associated based on their GPS coordinates.  **If a repeater is ever relocated, all links to its coverage data are broken** to ensure actual coverage is not skewed.
  - **Authentication:** Every wardriving session is validated against known mesh nodes.

MeshMapper believes in the ownership and control of how a regions data is presented lies with the region itself.  If a region chooses to bypass logic to limit false or misleading data, that is their choice, and visitors to their map will be warned as such.

## The Wardriving App

Data is collected using the **MeshMapper Wardriver** app (currently available as a webapp with native iOS and Android apps in beta testing).

  - **Companion Mode**: The app connects to your Meshtastic radio via Bluetooth (BLE).
  - **Passive Collection**: As you drive, walk, or cycle, the app periodically sends "pings" through your radio into the mesh network.
  - **Telemetry**: It records GPS coordinates, signal strength (SNR/RSSI), and the path the message took (which repeaters heard it).
  - **Upload**: When an internet connection is available, the app uploads this data to the MeshMapper server for comparison.  The combination of data received through the mesh and sent by the wardriving app determines the level of coverage an area has.

## How It Works

  - **The Ping**: The wardriving app connected to your companion sends automated messages out to your mesh at set intervals.
  - **The Mesh**: Repeaters in the area receive and re-broadcast your packet.
  - **The Ingest**: Specialized "Observer" nodes connected to the map server (via MQTT) listen for these packets.
  - **The Map**: If an Observer hears your packet, it confirms that a link exists between your location and the mesh. The map updates a **100m x 100m grid square** at your location to show the connection type.

## Purpose & Goals

### 1. Network Optimization
By visualizing signal paths and dead zones, repeater operators can adjust antenna placement, upgrade hardware, or deploy new repeaters in areas that actually need them.

### 2. Community Building
MeshMapper fosters a sense of shared ownership. Users can see their contributions on the map and compete on **Leaderboards** for the most distance covered.

### 3. Hardware Validation
The map provides objective data on hardware performance. You can see exactly how far a specific repeater can be heard, or compare the performance of different antennas in real-world conditions.

## Developers

MeshMapper is developed by **MrAlders0n** and **CSP-Tom** of the Greater Ottawa Mesh Radio Enthusiasts.  While MeshMapper is 100% free to use, your support helps us cover the backend resources and development time needed to keep up with the rapid global growth. If MeshMapper has helped you, [feel free to buy us a coffee](https://buymeacoffee.com/meshmapper)!

## And More!
There's much more to learn and explore.  Click the links to the left to navigate to different articles.