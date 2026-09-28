# MeshMapper MQTT Setup

An **MQTT observer** is a MeshCore node that acts as the "ears" of MeshMapper. It listens for mesh traffic and publishes it to an MQTT broker, where MeshMapper picks it up for processing. A new region needs at least one online observer sending to either the **MeshMapper** or **LetsMesh** broker. MeshMapper recommends its own broker.

## MeshMapper Broker

| Host | Port | Transport | Authentication |
| --- | --- | --- | --- |
| `mqtt.meshmapper.net` | 443 | WebSockets + TLS | Device signing |

## MQTT Observer Methods

There are four ways to set up a MeshCore MQTT observer that collects packets and forwards them to MeshMapper.

### 1. MeshCore Packet Capture (Python)

This method uses a dedicated companion device (e.g., Raspberry Pi) connected to your MeshCore radio via USB, BLE, or TCP. A Python service runs continuously, capturing packets and publishing them to MQTT.

  - **Requires**: A Raspberry Pi or similar always-on Linux computer, plus a MeshCore radio connected via USB or BLE
  - **Best for**: Dedicated observer setups where you have a spare device to run the capture service
  - **Guide**: [MeshCore Packet Capture Setup](mqtt-python.md)

### 2. MeshCore Home Assistant Integration

If you already run Home Assistant, this is the easiest route. The MeshCore-HA integration connects to your radio via USB, Wi-Fi, or Bluetooth and forwards packets to MQTT, while also exposing mesh data as HA entities for monitoring and automation.

  - **Requires**: A Home Assistant instance with a MeshCore radio accessible via USB, Wi-Fi, or Bluetooth
  - **Best for**: Users who already have Home Assistant and want observer functionality alongside mesh monitoring and automation
  - **Guide**: [MeshCore Home Assistant Setup](mqtt-ha.md)

### 3. MeshCore MQTT Native Firmware

This method runs directly on a Heltec V3 or V4 board with no companion device needed. The firmware natively captures packets and publishes them to MQTT using the board's built-in Wi-Fi.

  - **Requires**: A Heltec V3 or V4 with the MQTT-enabled firmware flashed
  - **Best for**: The simplest hardware setup, since no secondary computer is needed

Flash the observer firmware from the [MeshCore observer flasher](https://observer.gessaman.com/), built by agessaman/HerculesMulligan. It runs in your browser and walks you through flashing and setup. The source is in [agessaman/MeshCore](https://github.com/agessaman/MeshCore/tree/mqtt-bridge-implementation).

### 4. PyMC

This method uses the PyMC software, which handles MQTT configuration directly from its own interface.

  - **Requires**: A Raspberry Pi running PyMC
  - **Best for**: Anyone already running a PyMC repeater
  - **Guide**: [PyMC Repeater MQTT Setup](mqtt-pymc.md)

## Common observer questions

**Should I send to MeshMapper, LetsMesh or both?** Either broker can supply reports for MeshMapper. You may publish to both; MeshMapper combines reports from its configured brokers. One working broker is enough for onboarding.

**Can I use a mobile observer?** It can submit reports while online, but a fixed, always-on observer is a better choice for a region's required listener. A mobile receiver cannot verify a new region while it is offline or away from that region.

**Why is my observer not listed?** A broker connection by itself is not an observer report. Check that it publishes `status` or `packets` on the `meshcore/<region code>/<observer key>/...` topic, using the region's code. Then check the region admin panel's **Observers** tab and the broker checkmarks. Allow time for the first report to arrive.

**Can I run a regional MQTT broker?** A region admin can register a broker in **Settings**. Provide a reachable host and port, WebSockets transport, and its required authentication credentials. MeshMapper subscribes only to that region's topics; see [Observer verification](mqtt-pymc.md#verifying-your-observer) after saving. Do not publish broker credentials in a public channel.
