# Leaderboards & Statistics

Each region has a Leaderboard page (**Region → Leaderboard**) with statistics about the region, its wardrivers and its repeaters. There's also a [Global Leaderboard](#global-leaderboard) across every region.

Leaderboards are refreshed **once a day**, so recent pings can take up to 24 hours to show up. The page shows when it was last updated.

## Region Statistics

The **Stats** card at the top of the page:

  - **Total Data Points**: every ping collected in the region (all types).
  - **Ping breakdown**: **Bidirectional** (green), **TX Only** (orange), **RX Only** (purple), **Discovery** (cyan, including TRACE), **Dead** (grey) and **Dropped** (red). See [Ping Types](visuals.md#ping-types-defined).
  - **Active Repeaters**: repeaters on the map, including Ambiguous ones. Disabled and Inactive repeaters aren't counted.
  - **Estimated Coverage**: the share of mapped grid squares with working coverage (BIDIR, TX, RX, DISC or TRACE). Squares with only DEAD or DROP pings count as not covered.
  - **Contributors**: how many different wardrivers have contributed.
  - **Total Grid Squares**: how many 300 m squares have at least one ping. This always uses the 300 m grid, whatever your Grid Mode setting.

## Wardriver Leaderboards

Each board shows the top 10.

**Points**: 1 point per ping, plus **1.5 points** for each square where the app's Smart Pinging saved a ping (see [Top Airtime Savers](#top-airtime-savers)).

  - **Top Contributors (7 Days)**: points from the last 7 days.
  - **All Time Legends**: every point ever earned in the region.
  - **Top Explorers**: how many different 300 m squares you've pinged in. Being first doesn't matter.
  - **Top Pioneers**: squares you pinged **before anyone else**. One person per square, forever.
  - **Top Airtime Savers**: see below.
  - **Most Repeaters Administered**: active repeaters this person has logged in to as admin from the app.

The top three places show their rank in **gold**, **silver** and **bronze**.

Wardrivers are listed by device, or by their **My MeshMapper** account if they've linked one (all of an account's devices are combined into one row, with a 🔗 badge). Wardrivers without a name show as **Anonymous** and aren't ranked. Click **Profiles** to look up a wardriver's stats and [awards](awards.md).

### Top Airtime Savers

When the app's [Smart Pinging](app_wardriving_modes.md#smart-pinging) skips a ping because a square already has recent good coverage, that square earns **1.5 points** once it's verified against the region's coverage. Each square counts once per session. This board ranks wardrivers by those points alone; they're also included in the totals above.

## Repeater Leaderboards

### Best Repeaters (Ping Count)

Repeaters heard directly the most times. Sort by **Pings** (total) or **Grids** (different squares heard from). RX-only pings aren't counted.

### Best Repeaters (Max Range)

The single longest confirmed contact for each repeater, by ping type: **BIDIR**, **TX**, **RX**, **DISC** and **DEAD**. Click a column to sort by it. Distances over 500 km are ignored.

### Notes

  - **Ambiguous repeaters** stay listed, marked with a red **\*** ("Ambiguous ID"). Pings where their ID was ambiguous don't count towards them. See [Duplicate Repeater IDs](duplicaterepeaterid.md).
  - **Private repeaters** (🚫 in the name) show as "(private repeater)".
  - Regions that hide repeater detail don't show the repeater boards.
  - Regions that [turn off duplicate detection](overrideduplicates.md) show a warning that repeater statistics may be inaccurate.

## Global Leaderboard

The [Global Leaderboard](https://meshmapper.net/global_leaderboard.php) combines every region and is also refreshed daily.

  - **Global Stats**:
    - **Network**: Active Regions, Countries, Repeaters, Multibyte (%), Observers and Companions.
    - **Packets**: the same ping breakdown as a region.
    - **Activity**: Data Points, Grid Squares, Wardrivers, Live Now, Users (24h) and Sessions (24h).
  - **Wardriver boards**: **Top Wardrivers (7 Days)**, **All Time Legends**, **Top Explorers**, **Top Pioneers**, **Top Airtime Savers** and **Most Repeaters Administered**, each showing the wardriver's **primary region** (where they've earned the most points).
  - **Region boards**: **Most Repeaters**, **Most Grid Squares**, **Most Data Points** and **Most Wardrivers**.
  - **Repeater boards**: **Best Repeaters (Ping Count)** and **Best Repeaters (Max Range)** from every region, linking back to each repeater on its region's map.
  - **Multibyte Upgrade Board**: regions ranked by how many of their repeaters are [multi-byte](multibyte.md) capable.
  - **Scope Onboarding**: how many of each region's repeaters carry a mesh scope, with a 90-day trend.

Regions that hide repeater detail or [turn off duplicate detection](overrideduplicates.md) don't send their repeaters to the global board. Their wardrivers and coverage still count.
