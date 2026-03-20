# MeshMapper MQTT Setup

An **MQTT observer** is a MeshCore node that acts as the "ears" of MeshMapper — it listens for mesh traffic and publishes it to an MQTT broker, where MeshMapper picks it up for processing. Each region requires at least one observer connected to either the **LetsMesh** or **MeshMapper** broker (or both for redundancy).

## Available Brokers

An observer can connect to one or both of the following brokers:

| Broker | Host | Port | Transport | Authentication |
| --- | --- | --- | --- | --- |
| **LetsMesh** | `mqtt-us-v1.letsmesh.net` / `mqtt-eu-v1.letsmesh.net` | 443 | WebSockets + TLS | Device signing |
| **MeshMapper** | `mqtt.meshmapper.cc` | 443 | WebSockets + TLS | Device signing |

!!! tip "Redundancy"
    Connecting to both brokers is recommended but not required. Data received from multiple brokers is automatically deduplicated by MeshMapper.

## MQTT Observer Methods

There are four ways to set up a MeshCore MQTT observer that collects packets and forwards them to LetsMesh or MeshMapper.

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

!!! note "Coming Soon"
    Documentation for native MQTT firmware setup is in progress.

### 4. PyMC

This method uses the PyMC software, which handles MQTT configuration directly from its own interface.

  - **Requires**: A Raspberry Pi running PyMC
  - **Best for**: Anyone already running a PyMC repeater

!!! note "Coming Soon"
    Documentation for PyMC MQTT setup is in progress.
