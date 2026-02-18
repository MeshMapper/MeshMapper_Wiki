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

Data is collected using the **MeshMapper Wardriver** app, available for both iOS and Android.

[Download on the App Store](https://apps.apple.com/us/app/meshmapper/id6758073991) | [Get it on Google Play](https://play.google.com/store/apps/details?id=net.meshmapper.app)

## The Basics

  - **The Session**: Before collecting data, the app authenticates with the region and acquires a **Wardriving Session**. Regions have a limited number of active slots (set by that regions administrators) to prevent mesh congestion.
  - **The Ping**: Once a session is active, the app sends automated messages (pings) through your radio into the mesh at set intervals as you drive, walk, etc.
  - **The Mesh**: Repeaters in the area receive and re-broadcast your packet.
  - **The Ingest**: Specialized "Observer" nodes connected to the map server (via MQTT) listen for these packets and reports them to MeshMapper.
  - **The Map**: Data from the app and data from what was heard on the mesh get compared on the backend and display on the map in near-real-time.  [See the different levels of coverage MeshMapper can detect.](https://meshmapper.net/img/pingtypes.png)

[Check out the YOW - Ottawa map](https://yow.meshmapper.net) and adjust the map layers to see just how powerful MeshMapper is!

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