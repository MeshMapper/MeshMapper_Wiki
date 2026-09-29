# meshcoretomqtt (Python)

These instructions cover setting up the community [meshcoretomqtt](https://github.com/Cisien/meshcoretomqtt) project from Cisien as a MeshMapper observer. It runs on an always-on computer connected to a MeshCore repeater by USB, and has a built-in **MeshMapper** broker preset.

## Prerequisites

  - A Raspberry Pi (Zero 2, 3 or 4 recommended) or similar always-on Linux or macOS computer
  - A MeshCore repeater connected by USB, flashed with packet logging enabled (build flag `-D MESH_PACKET_LOGGING=1`) and firmware v1.8.0 or later
  - The repeater configured with a unique name
  - Internet access

## Installation

### 1. Run the Installer

```bash
curl -fsSL https://raw.githubusercontent.com/Cisien/meshcoretomqtt/main/install.sh | sudo bash
```

The installer sets up everything (Python environment, a system service, and config at `/etc/mctomqtt/`) and walks you through configuration. When a prompt shows a value in brackets, pressing Enter uses it.

### 2. Answer the Prompts

  - **Installation method**: choose **1) System service** (recommended).
  - **Serial device**: pick the USB port your repeater is connected to.
  - **IATA code**: enter your **MeshMapper region code** (e.g. `YOW`). This must match your region, or your observer won't show up.
  - **MQTT Broker Configuration**: choose **1) Select bundled broker presets**, then select **meshmapper**. Choose **5) Finish** when done.

### 3. Check It's Running

```bash
sudo systemctl status mctomqtt     # Check status
sudo journalctl -u mctomqtt -f     # View live logs
```

## Changing the Configuration

Your settings are in `/etc/mctomqtt/config.d/99-user.toml` and the MeshMapper preset in `/etc/mctomqtt/config.d/10-meshmapper.toml`. Don't edit `/etc/mctomqtt/config.toml`, as it's overwritten on updates.

```bash
sudo nano /etc/mctomqtt/config.d/99-user.toml
sudo systemctl restart mctomqtt
```

## Updating

```bash
curl -fsSL https://raw.githubusercontent.com/Cisien/meshcoretomqtt/main/scripts/update.sh | sudo bash
```

## Verifying Your Observer

Once your observer is running and connected, it appears in your region's admin panel under the [Observers tab](admins.md#observers) after packets have been received (repeater or companion adverts, or wardriving pings). Its **Brokers** column shows a coloured MeshMapper badge once the broker has heard it.

If nothing shows up, check the logs (`sudo journalctl -u mctomqtt -f`) for MQTT errors, and confirm the IATA code matches your region.
