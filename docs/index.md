# Welcome to MeshMapper!

**MeshMapper** is a community-driven visualization and analytics platform designed for the **MeshCore** LoRa mesh network. It provides real-time mapping of network coverage and repeater performance, helping communities build more robust and efficient mesh networks.

## What is MeshMapper?

At its core, MeshMapper is a web-based map that aggregates data collected by users "wardriving" (or "warwalking", etc.) their local area. Unlike simple node maps that just show where a device is, MeshMapper visualizes **actual RF coverage**.

It answers critical questions for mesh operators:

  - *"Can I reach the mesh from here?"*
  - *"Which repeater is providing the best coverage?"*
  - *"Where are the dead zones in our city?"*

## Administration

Powerful administration options allow regions (or multiregion groups) to manage their own map and its data. [See more about administration here.](admins.md)

## Core Principles

MeshMapper was designed to provide realistically reliable data without making assumptions.

  - **Duplicate Repeaters:** If a repeater with a [duplicate ID](duplicaterepeaterid.md) is detected on the mesh, coverage data is never directly associated with it. Mapping tools will suggest which repeater was actually involved, but no concrete link will ever be made.
  - **Association:** For every data point, repeaters involved in its transmission are associated based on their GPS coordinates. **If a repeater is ever relocated, all links to its coverage data are broken** to ensure actual coverage is not skewed.
  - **Authentication:** Every wardriving session is validated against known mesh nodes.
  - **Privacy:** Wardriving pings do not broadcast your GPS position over the air by default — coordinates travel only to the MeshMapper server. Wardrivers can also view and delete the data they've contributed at any time through the [My MeshMapper portal](portal.md).

MeshMapper believes each region should own and control how its data is presented. If a region chooses to bypass the logic that limits false or misleading data, that's their choice, and visitors to their map will be warned. Repeater owners can easily [opt out of being publicly listed](layers.md#private-repeaters) on the map.

## The Wardriving App

Data is collected using the **MeshMapper Wardriver** app, available for both iOS and Android.

[Download on the App Store](https://apps.apple.com/us/app/meshmapper/id6758073991) | [Get it on Google Play](https://play.google.com/store/apps/details?id=net.meshmapper.app)

See the [Privacy Policy](privacy.md) for what the app collects and how it's used.

## The Basics

  - **The Session**: Before collecting data, the app authenticates with the region and acquires a **Wardriving Session**. Each region has a limited number of transmit slots, set by its administrators, to keep wardriving from overwhelming the mesh. Once those slots are full, new users can still wardrive in passive mode (listening only).
  - **The Ping**: Once a session is active, the app sends automated messages (pings) through your radio into the mesh at set intervals as you drive, walk, etc.
  - **The Mesh**: Repeaters in the area receive and re-broadcast your packet.
  - **The Ingest**: Specialized "Observer" nodes connected to the map server (via MQTT) listen for these packets and report them to MeshMapper.
  - **The Map**: Data from the app is compared with what was heard on the mesh, and the results are displayed on the map in near-real-time. [See the different levels of coverage MeshMapper can detect.](visuals.md#ping-types-defined)

[Check out the YOW - Ottawa map](https://yow.meshmapper.net) and adjust the map layers to see just how powerful MeshMapper is!

## Purpose & Goals

### 1. Network Optimization
By visualizing signal paths and dead zones, repeater operators can adjust antenna placement, upgrade hardware, or deploy new repeaters in areas that actually need them.

### 2. Hardware Validation
The map provides objective data on hardware performance. You can see exactly how far a specific repeater can be heard, or compare the performance of different antennas in real-world conditions.

### 3. Community
Every wardriver helps fill in the picture for their local mesh. You can see your own contributions on the map and manage your profile and data through the [My MeshMapper portal](portal.md). [Leaderboards](leaderboards.md) and [awards](awards.md) recognize contributors along the way.

## Developers

MeshMapper is developed by **MrAlders0n** of the Greater Ottawa Mesh Radio Enthusiasts. The backend was started together with **CSP-Tom**, who has since moved on, and MrAlders0n continues that work. While MeshMapper is 100% free to use, your support helps cover the backend resources and development time needed to keep up with the rapid global growth. If MeshMapper has helped you, [feel free to buy us a coffee](https://buymeacoffee.com/meshmapper)!
