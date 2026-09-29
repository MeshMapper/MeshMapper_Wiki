# Overriding Duplicate ID Detection

By default, MeshMapper won't link pings to repeaters it can't tell apart, and marks those repeaters **Ambiguous** (see [Duplicate Repeater IDs](duplicaterepeaterid.md)). Some regions would rather see every possible repeater and connection, even when it's not certain which one was involved.

The **Disable Duplicate ID Detection Logic** setting turns these checks off.

!!! danger "Data Integrity Warning"
    Turning this on makes the map less accurate. When two repeaters share an ID (e.g. `A1`), MeshMapper can't tell them apart, so lines may be drawn to the wrong repeater and **Max Range** may be inflated.

    As the admin panel warns: *"The MeshMapper administration team will not be available to assist with data validation or cleanup. Proceed at your own risk."*

## How to Enable

1. Sign in to your region's admin panel.
2. Open **Settings → Repeaters, Neighbours & Scopes**.
3. Tick **Disable Duplicate ID Detection Logic**.
4. Save your settings.

*For a region in a [multiregion group](multiregions.md), this is set by the group admin under **Group Defaults**.*

## What Changes

### On the Map

  - **Repeaters**: no repeater is marked Ambiguous. Colliding repeaters show in their normal colours (green, pink or grey).
  - **Ping lines**: lines are drawn from pings to **every** repeater matching an ambiguous hop.
  - **Neighbour and backbone links**: drawn and counted for colliding repeaters too.
  - **Public warning**: an orange **warning** button (**Data Accuracy Warning**) appears at the top right of the map, telling visitors the region has turned off duplicate detection.

### When Data Comes In

  - **No automatic Ambiguous status**: new adverts no longer trigger the check, so colliding repeaters, including new ones, stay as they are.
  - **Pings**: a hop that matches more than one repeater is stored against all of them instead of being left unlinked.

### Leaderboards

  - **Region leaderboard**: colliding repeaters are included, and ambiguous pings count towards every matching repeater.
  - **Global leaderboard**: the region's repeaters aren't included. Its wardrivers still count.

## Summary of Differences

| Feature | Standard | Override |
| :--- | :--- | :--- |
| **Colliding repeaters** | Marked Ambiguous (red) automatically | Never marked Ambiguous |
| **Ambiguous pings** | Left unlinked; Duplicate lines only on a single selected ping | Linked and drawn to every matching repeater |
| **Neighbour and backbone links** | Only between repeaters that aren't Ambiguous | Include colliding repeaters |
| **Max Range** | Only from pings where the repeater's ID was clear | From every matching ping (may be inflated) |
| **Global leaderboard** | Repeaters included | Repeaters **not** included |
| **Public map** | No warning | **Data Accuracy Warning** shown |
