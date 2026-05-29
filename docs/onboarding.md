# Onboarding a New Region

MeshMapper is designed to be scalable, allowing new geographic regions to be added to the network. This guide outlines the process for community members to request a new map zone for their local mesh.

## Prerequisites

Before requesting a new region, you must ensure the local infrastructure is ready to support it.

  - **Active Mesh Community**: There should be an active group of users in the area.
  - **MQTT Observers**: You need at least one (preferably 2-3) nodes configured as **MQTT Clients** connected to the **LetsMesh** broker, the **MeshMapper** broker, or both.
    - These nodes act as the "ears" of the map, reporting traffic to MeshMapper.
    - See [MeshMapper MQTT Setup](mqtt-main.md) for detailed instructions.

## The Onboarding Form

To start the process, navigate to the **Region Onboarding** form (accessed via the About page).

The form collects the following critical information:

| Field | Description |
| --- | --- |
| **IATA Code** | The 3-letter code that will identify your region in the database and URL (e.g., `yow.meshmapper.net`). |
| **Region Name** | The display name for the map (e.g., "Ottawa, CA", "London, UK"). |
| **Region Radius** | A rough estimate (in km) of the area you intend to cover. |
| **Contact Info** | Your Discord username or Email address. This is required for administrators to contact you during the setup process. |
| **Public Channels** | A list of public channels used in your mesh (e.g., `Chat`, `Emergency`). This helps the wardriving app correctly identify valid traffic. |
| **Observer IDs** | The **Public ID** (e.g., `12345678XXXXXX...`) of the nodes acting as MQTT gateways. |
| **Volunteer as Administrator** | Optional. Tick this to volunteer as your region's administrator. Requires Discord to be linked. See [below](#volunteer-as-region-administrator) for details. |

## Volunteer as Region Administrator

The onboarding form includes an optional **Volunteer as Region Administrator** checkbox.

Enabling this option signals to the MeshMapper team that you are willing to take on the administrator role for your new region. As a region administrator, you would be responsible for:

  - Monitoring and managing your region's data and settings.
  - Supporting local wardrivers and answering questions about the map.
  - Being an active and available point of contact for your mesh community.

**Requirements:**

  - You must **link your Discord account** before this option becomes available. The checkbox is disabled until Discord is connected.
  - You must be genuinely active in your local mesh community.

**What happens if you volunteer:**

When your region is approved and deployed, an administrator account will be automatically created for you. Your credentials (username and a generated key) will be sent to you via Discord DM. You should log in to your region's admin panel and change your key immediately after first login.

*If you already have an administrator account on another MeshMapper region, access to the new region will simply be added to your existing account.*

## Defining the Boundary

One of the most important steps is defining the geographic boundary of your region. For a more detailed look into creating region boundaries (particularly if using geoJSON files), please see [Region Boundaries](https://wiki.meshmapper.net/region_boundaries.md).

  - **The Map Tool**: The form includes an interactive map with drawing tools.
  - **Draw Polygon**: Use the **Polygon Tool** (pentagon icon) to draw a precise shape around your mesh's coverage area if a circle  doesn't accurately describe it.  Alternatively, click the "Auto Generate Boundry" button to have AI attempt to draw the boundry for you.
  - **Import GeoJSON**: Alternatively, click the **Import GeoJSON** button to paste GeoJSON data directly. This is useful if you already have a boundary defined in another tool (e.g., [geojson.io](https://geojson.io)). Supported formats include `Polygon`, `MultiPolygon`, `Feature`, and `FeatureCollection`.
  - **Region Center**: The center pin automatically moves to the center of the polygon when one is drawn or imported. You can also drag the pin manually if needed. This determines where your region appears on the global map.
  - **Purpose**: This polygon is used to:
    - Define where wardriving activities in your region can occur.
    - Determine if a user is "In Zone" for authentication purposes.
    - Render the region border on the global map.

*Note: Keep the boundary reasonable. You can always expand it later as your network grows.*

## Submission & Approval

Once you submit the form:

  - 1. **MQTT Verification**: MeshMapper servers will verify if MQTT-connected observers are sending data to the brokers at either letsmesh.net or MeshMapper (or both).
  - 2. **Review**: If the servers are able to verify active observers, the region is presented to MeshMapper administrators for review.  Administrators will ensure the region isn't a duplicate, is named correctly, notes entered during onboarding are reviewed, etc.
  - 3. **Activation**: Once reviewed, the region is approved and will become available for wardriving.  It can take up to 5 minutes after deployment for the MeshMapper MQTT engine to start pulling in local data.

If you associated your Discord account during the onboarding process, you will receive automatic messages from MeshMapper with onboarding status.

!!! info "Request Deletion"
    Pending onboarding requests that have not passed MQTT verification in 3 days will automatically be deleted.

## Legacy Data

If you have historical coverage data from other systems, it can be imported into MeshMapper. This data will appear on a separate layer and is not included in leaderboard statistics. See [Data Upload](https://wiki.meshmapper.net/dataupload/) for format requirements.
