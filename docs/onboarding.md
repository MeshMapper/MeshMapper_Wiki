# Onboarding a New Region

MeshMapper is designed to be scalable, allowing new geographic regions to be added to the network. This guide outlines the process for community members to request a new map zone for their local mesh.

*Please note that all region approvals are granted at the discretion of the master and global administration team. Some circumstances may better be served by working with an existing region rather than creating a new one.*

## Prerequisites

Before requesting a new region, you must ensure the local infrastructure is ready to support it and that the new region would not be redundant or better served by making modifications to an existing region's boundaries.

  - **No Existing Region**: There must not be an existing region covering a substantial portion of the area desired for any new region. Regions within regions will not be allowed.
  - **No Nearby Neighbors**: No nearby neighboring regions should exist that could reasonably be expanded to include your desired area. The details matter. If your mesh is and will likely remain distinct from a nearby neighbor (e.g. due to extreme distance or natural terrain features that block RF), then a new region would be reasonable. If your desired new region falls in this category, please explain how it is justified vs modifying a nearby existing region's boundaries in the "Additional Notes" field.
  - **MQTT Observers**: You need at least one (preferably 2-3) nodes configured as **MQTT Clients** connected to the **MeshMapper** broker, the **LetsMesh** broker, or both.
    - These nodes act as the "ears" of the map, reporting traffic to MeshMapper.
    - See [MeshMapper MQTT Setup](mqtt-main.md) for detailed instructions.

## The Onboarding Form

To start the process, open the **Region Onboarding** form — available from the [meshmapper.net](https://meshmapper.net) homepage, or from any region map via the **About** menu → **Onboard Your Region**.

The form collects the following critical information:

| Field | Description |
| --- | --- |
| **IATA Code** | The 3-letter code that will identify your region in the database and URL (e.g., `yow.meshmapper.net`). *Please note that the mere existence of an IATA code does not, in and of itself, imply suitability for a MeshMapper region to be created using that code. International and regional commercial airports are strongly preferred over military or general aviation airfields.*|
| **Region Name** | The display name for the map (e.g., "Ottawa, CA", "London, UK"). |
| **Region Radius** | A rough estimate (in km) of the area you intend to cover. |
| **Region Boundary** | This is where you define your desired region boundary. We strongly encourage region admins to use geoJSON files and coordinate with neighboring regions when defining a region's boundaries. More information and geoJSON resources are available at [Region Boundaries](region_boundaries.md). |
| **Email Address / Discord Notifications** | Enter your email address (required) and optionally - though encouraged - link your Discord account to receive notifications on the status of your application. |
| **Additional Notes** | Use this field to provide additional details or context about your application.  If your desired region doesn't meet the [prerequisites](#Prerequisites) above and you believe an exception should be made, justify it in detail here. |
| **Public Channels** | A list of public channels used in your mesh (e.g., `Chat`, `Emergency`). This helps the wardriving app correctly identify valid traffic. |
| **Volunteer as Administrator** | Optional but recommended. Tick this to volunteer as your region's administrator. Requires Discord to be linked. See [below](#volunteer-as-region-administrator) for details. |

## Volunteer as Region Administrator

The onboarding form includes an optional **Volunteer as Region Administrator** checkbox.

Enabling this option signals to the MeshMapper team that you are willing to take on the administrator role for your new region. As a region administrator, you would be responsible for:

  - Monitoring and managing your region's data and settings.
  - Supporting local wardrivers and answering questions about the map.
  - Being an active and available point of contact for your mesh community.
    - **Please note: Admins are expected to maintain an ongoing, active presence beyond the initial onboarding process.  Admins who do not login to their account on the MeshMapper admin panel for more than 90 days are subject to being marked as inactive and/or having admin access removed.** Inactive accounts will not be consulted on changes to a region, and new admins may be added to a region at any time should no active admin accounts be present.

**Requirements:**

  - You must **link your Discord account** before this option becomes available. The checkbox is disabled until Discord is connected.
  - You must be genuinely active in your local mesh community.

**What happens if you volunteer:**

When your region is approved and deployed, an administrator account will be automatically created for you. Your credentials (username and a generated key) will be sent to you via Discord DM. You should log in to your region's admin panel and change your key immediately after first login.

*If you already have an administrator account on another MeshMapper region, access to the new region will simply be added to your existing account.*

## Defining the Boundary

One of the most important steps is defining the geographic boundary of your region. For a more detailed look into creating region boundaries (particularly if using geoJSON files), please see [Region Boundaries](region_boundaries.md). Regardless of which method is ultimately used, look at the other regions in your area and attempt to coordinate/align with area best practices.

  - **The Map Tool**: The form includes an interactive map with drawing tools.
  - **Import GeoJSON (strongly preferred)**: Click the **Import GeoJSON** button to paste GeoJSON data directly. This is useful if you already have a boundary defined in another tool (e.g., [geojson.io](https://geojson.io)). Supported formats include `Polygon`, `MultiPolygon`, `Feature`, and `FeatureCollection`. Drag the pin to your desired load-in view when loading the region on the web.
  - **Draw Polygon (alternate preferred)**: Use the **Polygon Tool** (pentagon icon) to draw a precise shape around your mesh's coverage area if a circle  doesn't accurately describe it.  Alternatively, click the "Auto Generate Boundry" button to have AI attempt to draw the boundry for you. Drag the pin to your desired load-in view when loading the region on the web.
  - **Radius Around Region Center (discouraged)**: Drag the pin or enter the GPS coordinates (degrees longitude west are negative numbers) and desired radius (in km) in the fields above the map, or drag the pin to your desired center point and then set the radius.  This will generate a circular region around the pin.
  - **Purpose**: This polygon is used to:
    - Define where wardriving activities in your region can occur.
    - Determine if a user is "In Zone" for authentication purposes.
    - Render the region border on the global map.

*Note: Keep the boundary reasonable. You can always modify it later, in coordination with your neighbors, as your network grows.*

## Submission & Approval

Once you submit the form:

  - 1. **MQTT Verification**: MeshMapper servers will verify if MQTT-connected observers are sending data to the brokers at either letsmesh.net or MeshMapper (or both).
  - 2. **Review**: If the servers are able to verify active observers, the region is presented to MeshMapper administrators for review.  Administrators will ensure the region isn't a duplicate, is named correctly, notes entered during onboarding are reviewed, etc.
  - 3. **Activation**: Once reviewed, the region is approved and will become available for wardriving.  It can take up to 5 minutes after deployment for the MeshMapper MQTT engine to start pulling in local data.

If you associated your Discord account during the onboarding process, you will receive automatic messages from MeshMapper with onboarding status.

While your request is pending, your region's subdomain (`https://<code>.meshmapper.net`) shows a status page for the application, including whether MQTT observer verification has passed. You can also ask the Discord bot: `@MeshMapper !status <code>`.

> [!WARNING]
> Pending onboarding requests that have not passed MQTT verification in 3 days will automatically be deleted.

## Legacy Data

If you have historical coverage data from other systems, it can be imported into MeshMapper. This data will appear on a separate layer and is not included in leaderboard statistics. See [Data Upload](https://wiki.meshmapper.net/dataupload/) for format requirements.
