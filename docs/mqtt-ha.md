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

Click **Add Broker** and fill in the following settings:

| Setting | Value |
| --- | --- |
| **Enabled** | Checked |
| **Server** | `mqtt.meshmapper.net` |
| **Port** | `443` |
| **Transport** | WebSocket |
| **Use TLS** | Checked |
| **Verify TLS Certificate** | Checked |
| **Keep Alive** | `60` |
| **Username** | *(leave blank)* |
| **Password** | *(leave blank)* |
| **Use MeshCore Auth Token** | Checked |
| **Token Audience** | `mqtt.meshmapper.net` |
| **Owner Pub Key** | *(leave blank)* |
| **Owner Email** | *(leave blank)* |
| **Payload Mode** | LetsMesh-Compatible |
| **Auth Token TTL** | `3600` |
| **Status Topic** | *(leave default)* |
| **Packet Topic** | *(leave default)* |
| **Broker IATA Code** | Your region's 3-letter IATA code (e.g., `YOW`, `SEA`, `LON`) |

### 4. Save and Exit

Click **Submit**, then click **Exit** to return to the integration page.

## Verifying Your Observer

Once your observer is running and connected, it will appear in your region's **Admin Portal** under the [Observers tab](admins.md#observers) once packets have been received (repeater or companion adverts, or wardriving pings) You should see a checkmark under the broker(s) your observer is connected to.