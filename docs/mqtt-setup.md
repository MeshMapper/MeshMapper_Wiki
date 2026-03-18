# MeshMapper MQTT Setup

An **MQTT observer** is a MeshCore node that acts as the "ears" of MeshMapper — it listens for mesh traffic and publishes it to an MQTT broker, where MeshMapper picks it up for processing. Each region requires at least one observer connected to either the **LetsMesh** or **MeshMapper** broker (or both for redundancy).

!!! info ""
    These instructions are for the community [meshcore-packet-capture](https://github.com/agessaman/meshcore-packet-capture) project from agessaman/HerculesMulligan.  A single observer can connect to both the LetsMesh and MeshMapper brokers.

## Prerequisites

  - A MeshCore-compatible device (e.g., T1000e, Heltec, T-Beam) to act as your observer node
  - A Raspberry Pi, Linux server, or similar always-on computer running a Debian-based OS (Raspberry Pi OS, Ubuntu, etc.)
  - A USB cable (for serial connection) or Bluetooth support (for BLE connection)
  - Internet access for packet forwarding

## Available Brokers

An observer can connect to one or both of the following brokers:

| Broker | Host | Port | Transport | Authentication |
| --- | --- | --- | --- | --- |
| **LetsMesh** | `mqtt-us-v1.letsmesh.net` / `mqtt-eu-v1.letsmesh.net` | 443 | WebSockets + TLS | Device signing |
| **MeshMapper** | `mqtt.meshmapper.cc` | 443 | WebSockets + TLS | Device signing |

!!! tip "Redundancy"
    Connecting to both brokers is recommended but not required. Data received from multiple brokers is automatically deduplicated by MeshMapper.

## Installation

### 1. Flash a Companion Device

Configure a Companion device using the [MeshCore Flasher Tool](https://flasher.meshcore.co.uk) and connect it to your Raspberry Pi or Linux server via USB.  Ensure radio settings are correct for your region.

### 2. Install Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3.12-venv curl git
```

### 3. Install the MeshCore Decoder

The MeshCore decoder is required for authentication when sending packets to the brokers:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install --lts
npm install -g @michaelhart/meshcore-decoder
```

Verify the installation:

```bash
which meshcore-decoder
```

### 4. Run the meshcore-packet-capture Installer

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/agessaman/meshcore-packet-capture/main/install.sh)
```

The interactive installer will walk you through the remaining configuration steps below.

### 5. Device Connection

You will be prompted to select a connection type:

| Method | Best For | Notes |
| --- | --- | --- |
| **Serial** (recommended) | USB-connected devices | Most reliable for continuous operation |
| **BLE** | T1000e and compatible devices | Wireless, no cable needed |
| **TCP** | Network-connected devices | For use with ser2net or TCP-to-serial bridges |

For serial connections, the script will automatically detect connected devices. Select your device from the list.

### 6. IATA Code

Enter your region's **3-letter IATA code** (e.g., `SEA`, `LAX`, `YOW`, `LON`). This identifies which MeshMapper region your observer belongs to.

### 7. JWT Token Configuration (Optional)

You may optionally configure:

  - **Owner Public Key**: The public key of the observer owner (64 hex characters)
  - **Owner Email**: Contact email for the LetsMesh Analyzer

These are optional, apply to LetsMesh only, and can be skipped.

### 8. MQTT Broker Configuration

#### LetsMesh Broker

The script will ask whether to enable the LetsMesh Packet Analyzer. This connects to both the US and EU LetsMesh servers for redundancy. Recommended to enable.

#### MeshMapper Broker

When prompted to configure additional brokers, select "1" additonal, and add the MeshMapper broker with the following settings:

| Setting | Value |
| --- | --- |
| Server hostname | `mqtt.meshmapper.cc` |
| Port | `443` |
| WebSockets transport | **Yes** |
| TLS/SSL encryption | **Yes** |
| Verify TLS certificates | **Yes** |
| Authentication method | **MeshCore Auth Token** |
| Token audience | `mqtt.meshmapper.cc` |

When prompted for topic configuration, select **Default pattern** (`meshcore/{IATA}/{PUBLIC_KEY}/status`, `meshcore/{IATA}/{PUBLIC_KEY}/packets`).

### 9. Installation Method

Choose how the capture software should run:

| Method | Description |
| --- | --- |
| **System Service** (recommended) | Runs on boot via systemd, auto-restarts on failure |
| **Docker Container** | Isolated environment, easy to update |
| **Manual** | No automatic startup, run when needed |

For the recommended **systemd service**, the script will:

  - Install and enable the service
  - Start it immediately
  - Verify a successful MQTT connection

## Managing the Service

Once installed as a systemd service, use these commands:

```bash
# Start / stop / restart
sudo systemctl start meshcore-capture
sudo systemctl stop meshcore-capture
sudo systemctl restart meshcore-capture

# Check status
sudo systemctl status meshcore-capture

# View live logs
sudo journalctl -u meshcore-capture -f
```

The configuration file is stored at:

```
~/.meshcore-packet-capture/.env.local
```

## Resource Limits

The systemd service includes built-in safeguards:

  - **Memory**: 512 MB limit
  - **CPU**: 50% limit
  - **Tasks**: 200 max
  - **Auto-restart**: Up to 3 failures within 5 minutes before stopping

## Verifying Your Observer

Once your observer is running and connected, it will appear in your region's **Admin Portal** under the [Observers tab](admins.md#observers) once packets have been received (repeater or companion adverts, or wardriving pings) You should see a checkmark under the broker(s) your observer is connected to.