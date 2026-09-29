# MeshMapper MQTT Setup

An **MQTT observer** is a MeshCore node that acts as the "ears" of MeshMapper. It listens for mesh traffic and publishes it to the MeshMapper MQTT broker, where MeshMapper picks it up for processing. A new region needs at least one online observer sending to the **MeshMapper broker**.

## MeshMapper Broker

| Host | Port | Transport | Authentication |
| --- | --- | --- | --- |
| `mqtt.meshmapper.net` | 443 | WebSockets + TLS | Device signing |

## MQTT Observer Methods

There are four ways to set up a MeshCore MQTT observer that sends packets to MeshMapper.

### 1. MeshCore MQTT Native Firmware

This method runs directly on the radio with no companion computer needed. The firmware captures packets and publishes them to MQTT over the board's built-in Wi-Fi. Most ESP-based devices with Wi-Fi are supported.

  - **Requires**: An ESP-based device with Wi-Fi
  - **Best for**: The simplest hardware setup, since no secondary computer is needed
  - **Guide**: [MeshCore MQTT Native Firmware Setup](mqtt-firmware.md)
  - **Built by**: HerculesMulligan

### 2. MeshCore Home Assistant Integration

The MeshCore-HA integration connects to your radio via USB, Wi-Fi, or Bluetooth and forwards packets to MQTT, while also exposing mesh data as HA entities for monitoring and automation.

  - **Requires**: A Home Assistant instance with a MeshCore radio accessible via USB, Wi-Fi, or Bluetooth
  - **Best for**: Users who already have Home Assistant and want observer functionality alongside mesh monitoring and automation
  - **Guide**: [MeshCore Home Assistant Setup](mqtt-ha.md)

### 3. meshcoretomqtt (Python)

This method uses an always-on computer (e.g., Raspberry Pi) connected to a MeshCore repeater by USB. A Python service runs continuously, capturing packets and publishing them to MQTT. It includes a built-in MeshMapper broker preset.

  - **Requires**: A Raspberry Pi or similar always-on Linux/macOS computer, plus a MeshCore repeater with packet logging enabled, connected by USB
  - **Best for**: Dedicated observer setups where you have a spare computer and repeater
  - **Guide**: [meshcoretomqtt Setup](mqtt-python.md)

### 4. PyMC

This method uses the PyMC software, which handles MQTT configuration directly from its own interface.

  - **Requires**: A Raspberry Pi running PyMC
  - **Best for**: Anyone already running a PyMC repeater
  - **Guide**: [PyMC Repeater MQTT Setup](mqtt-pymc.md)

## Common Observer Questions

**Which broker should I send to?** The MeshMapper broker. MeshMapper also collects from LetsMesh, but that isn't our infrastructure, so we can't guarantee we'll always have access to it.

**Can I use a mobile observer?** No, mobile observers are highly discouraged. MeshMapper's backend is designed for fixed observers, and a mobile one doesn't provide proper coverage data and gives misleading results in some mapping modes. KiekR mobile observers are dropped at MeshMapper's ingest point. Use a fixed, always-on observer.

**Why is my observer not listed?** A broker connection by itself is not an observer report. Check that it publishes `status` or `packets` on the `meshcore/<region code>/<observer key>/...` topic, using the region's code. Then check the region's **Region → Observers** popup on the map. Allow time for the first report to arrive.

**Can my region use its own MQTT broker?** Yes. After onboarding, region admins can configure MeshMapper to also pull from their own regional broker in the admin panel under **Settings → MQTT Brokers & Observers**. Provide a reachable host and port, WebSockets transport, and its authentication credentials. MeshMapper subscribes only to that region's topics. Do not publish broker credentials in a public channel.
