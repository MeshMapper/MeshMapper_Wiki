# MeshCore Home Assistant Setup

These instructions cover adding the MeshMapper MQTT broker to an existing [MeshCore-HA](https://meshcore-dev.github.io/meshcore-ha/) integration. If you haven't installed MeshCore-HA yet, follow the [official installation guide](https://meshcore-dev.github.io/meshcore-ha/docs/ha/installation) first.

## Prerequisites

  - A working Home Assistant instance with the MeshCore-HA integration installed and connected to your radio

## Adding the MeshMapper Broker

### 1. Open the MeshCore Integration

Navigate to **Settings > Devices & Services > MeshCore**. Click the **gear icon** beside your **MeshCore Node** entry.

### 2. Manage MQTT Brokers

Select **Manage MQTT Brokers** and click **Submit**.

### 3. Add the MeshMapper Broker

Click **Add Broker** and set the following. Leave everything else at its default.

| Setting | Value |
| --- | --- |
| **Enabled** | Checked |
| **Server** | `mqtt.meshmapper.net` |
| **Port** | `443` |
| **Transport** | WebSocket |
| **Use TLS** | Checked |
| **Verify TLS Certificate** | Checked |
| **Use MeshCore Auth Token** | Checked |
| **Token Audience** | `mqtt.meshmapper.net` |
| **Broker IATA Code** | Your **MeshMapper region code** (e.g. `YOW`). This must match your region, or your observer won't show up. |

### 4. Save and Exit

Click **Submit**, then click **Exit** to return to the integration page.

## Verifying Your Observer

Once your observer is running and connected, it appears in your region's admin panel under the [Observers tab](admins.md#observers) after packets have been received (repeater or companion adverts, or wardriving pings). You should see a checkmark under the MeshMapper broker.

If nothing shows up, check the Home Assistant logs for MQTT errors, and confirm the Broker IATA Code matches your region.
