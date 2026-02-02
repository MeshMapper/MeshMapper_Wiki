# Onboarding a New Region

MeshMapper is designed to be scalable, allowing new geographic regions to be added to the network. This guide outlines the process for community members to request a new map zone for their local mesh.

## Prerequisites

Before requesting a new region, you must ensure the local infrastructure is ready to support it.

  - **Active Mesh Community**: There should be an active group of users in the area.
  - **MQTT Observers**: You need at least one (preferably 2-3) nodes configured as **MQTT Clients** connected to the `letsmesh.net` broker.
    - These nodes act as the "ears" of the map, reporting traffic to MeshMapper.

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

## Defining the Boundary

One of the most important steps is defining the geographic boundary of your region.

  - **The Map Tool**: The form includes an interactive map with drawing tools.
  - **Draw Polygon**: You must use the **Polygon Tool** (pentagon icon) to draw a precise shape around your coverage area.
  - **Purpose**: This polygon is used to:
    - Filter out stray pings from outside the region.
    - Determine if a user is "In Zone" for authentication purposes.
    - Render the region border on the global map.

*Note: Keep the boundary reasonable. You can always request an expansion later as your network grows.*

## Submission & Approval

Once you submit the form:

  - 1. **Notification**: A webhook immediately notifies the MeshMapper administrators of the new request.
  - 2. **Review**: Admins will verify the Observer IDs and ensure they are successfully transmitting data to the MQTT broker.
  - 3. **Activation**: Once verified, the region is approved. A new subdomain (e.g., `new.meshmapper.net`) is provisioned, and the database structures are automatically generated.

You will be contacted via the provided method (Discord/Email) once the map is live or if further configuration is needed.

## Legacy Data

If you have historical coverage data from other systems, it can be imported into MeshMapper. This data will appear on a separate layer and is not included in leaderboard statistics. See [Data Upload](https://wiki.meshmapper.net/dataupload/) for format requirements.