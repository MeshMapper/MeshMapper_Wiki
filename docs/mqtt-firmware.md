# MeshCore MQTT Native Firmware

These instructions cover setting up the MeshCore observer firmware to send to MeshMapper. The firmware runs directly on an ESP-based radio with Wi-Fi, so no extra computer is needed. It has a built-in **MeshMapper** broker preset.

*The observer firmware is built by HerculesMulligan. For advanced options, see the [MeshCore Observer Setup Guide](https://observer.gessaman.com/docs).*

## Prerequisites

  - An ESP-based MeshCore device with Wi-Fi (e.g. Heltec V3/V4, Station G2)
  - A Wi-Fi network the observer can stay connected to
  - Chrome or Edge (for flashing from the browser)

## 1. Flash the Firmware

Open the [MeshCore Observer Flasher](https://observer.gessaman.com/), pick **MQTT Observer Firmware**, select your device, and flash it from the browser.

## 2. Configure the Observer

### Option 1. Setup Wizard

On first boot, the observer creates a Wi-Fi network named **MeshCore-Setup-XXXX**.

1. Connect to it from your phone or computer. The setup page opens automatically (or browse to `http://192.168.4.1/`).
2. Walk through the wizard: **WiFi → radio → MQTT → review**.
    - **Radio**: must match the other nodes in your mesh.
    - **MQTT**: set the IATA code to your **MeshMapper region code** (e.g. `YOW`), and set slot 1 to the **meshmapper** preset.
3. Click **Save & reboot**. The observer joins your Wi-Fi and connects to MeshMapper.

### Option 2. Command Line

Connect to the device console over USB serial (115200 baud) or by repeater login from the companion app, then run:

```bash
set radio 910.525,62.5,7,5     # must match your mesh: <freq>,<bw>,<sf>,<cr>
set name MyObserver
set mqtt.iata YOW              # your MeshMapper region code
set wifi.ssid YourWiFiNetwork
set wifi.pwd YourWiFiPassword
set mqtt1.preset meshmapper
reboot
```

The IATA code must match your MeshMapper region, or your observer won't show up. After it reboots, check the connection with `get mqtt.status`.

## Verifying Your Observer

Once your observer is running and connected, it appears in your region's admin panel under the [Observers tab](admins.md#observers) after packets have been received (repeater or companion adverts, or wardriving pings). You should see a checkmark under the MeshMapper broker.

If nothing shows up, run `get wifi.status` and `get mqtt.status` on the device console, and confirm `mqtt.iata` matches your region.
