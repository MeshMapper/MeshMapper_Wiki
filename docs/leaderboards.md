# Leaderboards & Statistics

The Leaderboard page provides a real-time statistical overview of a regions performance, user contributions, and repeater capabilities.

## Region Statistics

At the top of the page, you will find high-level metrics for the current region. Leaderboard data is cached and regenerated about **once a day**, so recent contributions can take up to 24 hours to appear.

  - **Total Data Points**: The aggregate number of valid pings collected in the database.
  - **Ping Breakdown**:
    - **Bidirectional (Green)**: Confirmed two-way links.
    - **TX Only (Orange)**: Packets sent by the user and heard by the mesh, but no confirmation was received back.
    - **RX Only (Purple)**: Packets heard by the user (e.g., telemetry), but the user did not transmit.
    - **Discovery (Cyan)**: Node discovery packets.
    - **Dead/Dropped**: Failed packets or those that hit a repeater but did not route further.
  - **Active Repeaters**: The count of repeaters currently online and trusted. **Note:** Repeaters flagged as "Duplicate" or "Excluded" are not counted here.
  - **Estimated Coverage**: A percentage representing how much of the mapped grid contains valid coverage (BIDIR, TX, DISC, RX).
  - **Contributors**: The number of unique users who have contributed data to the region.
  - **Total Grid Squares**: The total number of unique ~300m grid squares that have been mapped by at least one user. This metric always uses the 300m grid regardless of the user's Grid Mode setting.

## User Leaderboards

User rankings are based on the number of valid data points contributed. 1 Ping = 1 Point.

  - **Top Contributors (7 Days)**: A rolling window of activity over the last week. This is useful for seeing who is currently active in the community.
  - **All Time Legends**: The total accumulation of contributions since the region was onboarded.

### Top Explorers
This leaderboard rewards **exploration** — covering new ground rather than re-driving the same routes. It counts the number of unique ~300m grid squares where each user placed the **first-ever ping**. This metric always uses the 300m grid regardless of the user's Grid Mode setting. If a grid square has been pinged 100 times by 10 different users, only the user who mapped it first gets credit. All coverage types count (BIDIR, TX, RX, DISC, DEAD, DROP).

| Ranking | Indicator |
| --- | --- |
| **1st** | **Gold** Number |
| **2nd** | **Silver** Number |
| **3rd** | **Bronze** Number |

## Repeater Leaderboards

These tables highlight the performance of the infrastructure itself.

### Best Repeaters (Ping Count)
This ranks repeaters by how much traffic they have handled. The table shows both the **total ping count** and the number of **unique grid squares** the repeater has been heard from — click either column header to sort by that metric.

### Best Repeaters (Max Range)
This ranks repeaters by the furthest distance (in km/m) they have achieved a link. The table is broken down by signal type to show different propagation characteristics:

  - **BIDIR (Green)**: Max distance where a solid **two-way** link was established.
  - **TX (Orange)**: Max distance where the repeater heard the user (but the user didn't hear the confirmation). This often indicates the repeater has a better "ear" (receive sensitivity) than the user.
  - **RX (Purple)**: Max distance where the user heard the repeater (but didn't transmit). This indicates the repeater has a strong transmit signal.

*Tip: You can click the headers (BIDIR, TX, RX) to sort the table by that specific metric.*

## Global Leaderboard

The [Global Leaderboard](https://meshmapper.net/global_leaderboard.php) aggregates data from all active regions into a single view. It is regenerated daily by a scheduled task and includes:

  - **Global Stats**: Combined totals across all regions — data points, ping breakdowns, repeater count, contributors, total grid squares, active regions, and observer counts (with a per-broker breakdown).
  - **Top Contributors (7 Days)** and **All Time Legends**: Cross-region user rankings with each user's primary region shown.
  - **Top Explorers**: Aggregated first-mapper grid square counts across all regions.
  - **Region Rankings**: **Most Repeaters**, **Most Grid Squares**, **Most Data Points**, and **Most Contributors** — regions ranked against each other.
  - **Best Repeaters (Ping Count)** and **Best Repeaters (Max Range)**: Repeater rankings drawn from every region, with links back to the originating regional map. The Ping Count table includes unique grid square counts alongside total ping counts — click the column headers to sort by either metric.

Each user's **primary region** is determined by where they have contributed the most data points. Contributors are de-duplicated by device public key, so the same node heard in several regions counts as one entry.

## Contests

During special events (e.g., **Holiday Wardrive Contest**), a special leaderboard card will appear at the top of the page.

  - **Time-Limited**: Only pings collected within the specific contest start and end dates are counted.
  - **Exclusions**: Developers, administrators, and contest organizers are often excluded from these rankings to ensure fairness.
  - **Live Updates**: Like the other boards, this updates in near real-time as data is submitted.