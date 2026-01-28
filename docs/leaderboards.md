# Leaderboards & Statistics

The Leaderboard page provides a real-time statistical overview of a regions performance, user contributions, and repeater capabilities.

## Region Statistics

At the top of the page, you will find high-level metrics for the current region. These numbers update automatically as new data comes in.

  - **Total Data Points**: The aggregate number of valid pings collected in the database.
  - **Active Drivers**: The number of users currently running an active Wardriving session.
  - **Ping Breakdown**:
    - **Bidirectional (Green)**: Confirmed two-way links.
    - **TX Only (Orange)**: Packets sent by the user and heard by the mesh, but no confirmation was received back.
    - **RX Only (Purple)**: Packets heard by the user (e.g., telemetry), but the user did not transmit.
    - **Discovery (Cyan)**: Node discovery packets.
    - **Dead/Dropped**: Failed packets or those that hit a repeater but did not route further.
  - **Active Repeaters**: The count of repeaters currently online and trusted. **Note:** Repeaters flagged as "Duplicate" or "Excluded" are not counted here.
  - **Estimated Coverage**: A percentage representing how much of the mapped grid contains valid coverage (BIDIR, TX, DISC, RX).

## User Leaderboards

User rankings are based on the number of valid data points contributed. 1 Ping = 1 Point.

  - **Top Contributors (7 Days)**: A rolling window of activity over the last week. This is useful for seeing who is currently active in the community.
  - **All Time Legends**: The total accumulation of contributions since the region was onboarded.

| Ranking | Indicator |
| --- | --- |
| **1st** | **Gold** Number |
| **2nd** | **Silver** Number |
| **3rd** | **Bronze** Number |

## Repeater Leaderboards

These tables highlight the performance of the infrastructure itself.

### Best Repeaters (Max Range)
This ranks repeaters by the furthest distance (in km/m) they have achieved a link. The table is broken down by signal type to show different propagation characteristics:

  - **BIDIR (Green)**: Max distance where a solid **two-way** link was established.
  - **TX (Orange)**: Max distance where the repeater heard the user (but the user didn't hear the confirmation). This often indicates the repeater has a better "ear" (receive sensitivity) than the user.
  - **RX (Purple)**: Max distance where the user heard the repeater (but didn't transmit). This indicates the repeater has a strong transmit signal.

*Tip: You can click the headers (BIDIR, TX, RX) to sort the table by that specific metric.*

## Contests

During special events (e.g., **Holiday Wardrive Contest**), a special leaderboard card will appear at the top of the page.

  - **Time-Limited**: Only pings collected within the specific contest start and end dates are counted.
  - **Exclusions**: Developers, administrators, and contest organizers are often excluded from these rankings to ensure fairness.
  - **Live Updates**: Like the other boards, this updates in near real-time as data is submitted.