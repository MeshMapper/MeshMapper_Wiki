# Onboarding a New Region

This guide walks through requesting a new MeshMapper region for your local mesh.

*All region approvals are at the discretion of the MeshMapper administration team. Sometimes working with an existing region is a better fit than creating a new one.*

## Before You Start

  - **No existing region**: Your area must not already be substantially covered by another region. Regions within regions are not allowed.
  - **No nearby neighbor that could expand**: If a nearby region could reasonably be expanded to cover your area, that's preferred. A new region makes sense when your mesh is clearly separate (e.g. distance or terrain that blocks RF). If that's your case, explain why in **Additional Notes**.
  - **An MQTT observer**: You need at least one (preferably 2-3) observer nodes online in your area, connected to the **MeshMapper MQTT broker**. Observers are the "ears" of the map. See [MeshMapper MQTT Setup](mqtt-main.md).

## Starting a Request

Open the onboarding form from [meshmapper.net](https://meshmapper.net):

  - **Switch Region** menu → **Onboard Region**, or
  - **About** menu → **Onboard Your Region**, or
  - go directly to [meshmapper.net/?onboarding](https://meshmapper.net/?onboarding).

The form walks you through five steps: **Code → Region → Boundary → Mesh → Submit**.

## 1. Code

Search for your city, airport, or code and pick your region's **IATA airport code**. It becomes your region's address (e.g. `yow.meshmapper.net`). Codes already in use are greyed out, and nearby available codes are suggested.

*Having an IATA code doesn't by itself make it suitable for a region. International and regional commercial airports are strongly preferred over military or general aviation airfields. The airport must also be reasonably close to your region.*

## 2. Region

Confirm the **Country** and **Region Name** (filled in from the airport you picked). The name is what people see in the region list, e.g. "Ottawa, CA".

## 3. Boundary

MeshMapper builds your boundary from OpenStreetMap borders.

  1. **Drag the pin** onto your region. Picking a code moves the map, but not the pin, so make sure you drag it.
  2. The borders around the pin load automatically (or press **Load Boundary**). Choose a level: **State/Prov**, **County** (default), or **Local** (municipality, where available).
  3. **Click the green areas** you want to include. Use the arrow buttons around the pin to load more areas.
  4. Press **Continue** to merge your selection into one boundary.

On the map, **purple** is existing regions, **green** is areas you can pick, and **cyan** is your selection. Areas that belong to another region can't be picked, and your boundary can't overlap an existing region.

*Keep the boundary reasonable and coordinate with neighboring regions. It can be changed later as your network grows.*

!!! note "Custom boundaries"
    Drawing or importing your own GeoJSON (under **Advanced Mapping**) is only accepted in special circumstances. If you think you need one, explain why in **Additional Notes**. See [Region Boundaries](region_boundaries.md).

## 4. Mesh

**Public Channels**: List any public channels your mesh uses besides `#public` (e.g. `Chat`, `Emergency`). The app listens on these channels while wardriving, so more channels means more packets get decoded and verified.

**Regions/Scopes**: We highly recommend your area scope its wardriving traffic. However, if scopes aren't set up on the repeaters in your mesh, every ping will show as a drop.

## 5. Submit

  - **E-Mail Address** (required).
  - **Link Discord** (optional, recommended): get status updates and region alerts by Discord DM.
  - **Volunteer as Region Administrator** (optional, recommended): see [below](#volunteer-as-region-administrator).
  - **Additional Notes**: anything the team should know, including why an exception to the [prerequisites](#before-you-start) should be made.

## Volunteer as Region Administrator

Tick **Volunteer as Region Administrator** to become your region's admin. Admins:

  - manage their region's data and settings,
  - support local wardrivers and answer questions about the map,
  - are an active point of contact for their mesh community.

You must be genuinely active in your local mesh community. Once you accept, you're listed publicly as an admin on your region's map.

When your region is approved, you'll get an invite by email, or by Discord DM if you linked Discord. Sign in or create a MeshMapper account and accept it. That one account signs you in to both the [portal](portal.md) and your region's admin panel.

!!! warning "Stay active"
    Admins who don't sign in to the admin panel for more than 90 days may be marked inactive or have their access removed. Inactive admins aren't consulted on changes to their region, and new admins may be added if a region has no active admins.

## After You Submit

  1. **Observer check**: MeshMapper checks that an observer is reporting from your region's code. This takes up to 5 minutes once your observer is online.
  2. **Review**: The MeshMapper team reviews the request (name, boundary, conflicts with other regions, your notes).
  3. **Go live**: Once approved, your region is live. Repeaters and pings can take up to 5 minutes to appear on the map.

While your request is pending, `https://<code>.meshmapper.net` shows its status, including whether an observer has been detected. You can also ask the Discord bot: `@MeshMapper !status <code>`. If you linked Discord, you'll get DMs as your request moves along.

!!! warning
    Requests with no detected observer after 3 days are automatically deleted. You'll get reminders by email (and Discord, if linked) until then.
