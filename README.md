```markdown
# Zinguo Bathroom Fan Home Assistant Add-on

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A custom integration for Zinguo Smart Bathroom Fan for Home Assistant.

## Features
- **Config Flow**: Easy setup through UI
- **Secure Storage**: Account credentials stored securely in Home Assistant
- **Multiple Entities**:
  - Fan entity with preset modes (Off, Cool, Heat Low, Heat High)
  - Individual switches for Light, Ventilation, Wind, Heater 1, Heater 2
  - Temperature sensor
  - Online status sensor
- **Automatic Token Management**: Handles login and token refresh automatically
- **Privacy Focused**: No data sent to third-party servers

## Installation

### Method 1: Home Assistant Add-on Store
1. Add this repository to your Home Assistant Add-on Store:
```

https://github.com/jyz0501/hassio-zinguo

```
2. Install the "Zinguo Bathroom Fan" add-on
3. Start the add-on
4. Restart Home Assistant

### Method 2: HACS (Custom Repository)
1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots in top right → Custom repositories
4. Add repository: `https://github.com/jyz0501/hassio-zinguo`
5. Category: Integration
6. Search for "Zinguo Bathroom Fan" and install
7. Restart Home Assistant

### Method 3: Manual Installation
1. Copy the `custom_components/zinguo` folder to your Home Assistant `custom_components` folder
2. Restart Home Assistant

## Configuration
1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Zinguo Bathroom Fan**
4. Enter your credentials:
- Account: Your Zinguo account phone number
- Password: Your Zinguo account password  
- MAC Address: Your device MAC address (12 characters, e.g., C44F33D86409)
- Name: Custom name for your device

## Entities Created
- `fan.zinguo_fan` - Main fan control with preset modes
- `switch.zinguo_light` - Light control
- `switch.zinguo_ventilation` - Ventilation mode
- `switch.zinguo_wind` - Wind only mode
- `switch.zinguo_heater_1` - Heater 1
- `switch.zinguo_heater_2` - Heater 2
- `sensor.zinguo_temperature` - Temperature reading
- `sensor.zinguo_online_status` - Device connection status

## API Functions
- 吹风 (Chuifeng) - Wind only (Cool mode)
- 换气 (Huanqi) - Ventilation only
- 暖风1 (Nuanfeng1) - Heater 1 + Wind (Heat Low mode)
- 暖风2 (Nuanfeng2) - Heater 2 + Wind (Heat High mode)
- 全关 (Quanguan) - Turn off all

## Automation Examples

```yaml
# Turn on heat when bathroom gets cold
automation:
- alias: "Bathroom Heat On"
 trigger:
   platform: numeric_state
   entity_id: sensor.bathroom_temperature
   below: 20
 action:
   service: fan.set_preset_mode
   target:
     entity_id: fan.zinguo_fan
   data:
     preset_mode: "heat_low"

# Turn on ventilation when humidity is high
automation:
- alias: "Bathroom Ventilation"
 trigger:
   platform: numeric_state
   entity_id: sensor.bathroom_humidity
   above: 70
 action:
   service: switch.turn_on
   target:
     entity_id: switch.zinguo_ventilation

# Morning routine - turn on heat before shower
automation:
- alias: "Morning Shower Heat"
 trigger:
   platform: time
   at: "07:00:00"
 condition:
   condition: time
   weekday:
     - mon
     - tue
     - wed
     - thu
     - fri
 action:
   - service: fan.set_preset_mode
     target:
       entity_id: fan.zinguo_fan
     data:
       preset_mode: "heat_low"
   - delay:
       hours: 0
       minutes: 30
       seconds: 0
   - service: fan.set_preset_mode
     target:
       entity_id: fan.zinguo_fan
     data:
       preset_mode: "off"
```

Privacy and Security

· 🔒 Account credentials are stored securely in Home Assistant's encrypted storage
· 🔐 No data is sent to third-party servers
· 🌐 All communication is directly with Zinguo's official API
· 🚫 No tracking or analytics

Troubleshooting

Integration doesn't appear in the list

1. Ensure the add-on is running (if using add-on version)
2. Restart Home Assistant
3. Check Home Assistant logs for any errors

Can't connect to device

1. Verify your device is online in the Zinguo mobile app
2. Check the MAC address format (12 uppercase characters, no colons)
3. Confirm your account credentials are correct
4. Check network connectivity from your Home Assistant instance

Entities not updating

1. Check device online status
2. Verify token is valid (integration handles this automatically)
3. Check Home Assistant logs for API errors

Development

Project Structure

```
hassio-zinguo/
├── config.yaml          # Add-on configuration
├── Dockerfile          # Docker container definition
├── run.sh             # Installation script
├── repository.json    # Add-on store repository info
└── custom_components/
    └── zinguo/        # Custom integration
        ├── __init__.py
        ├── manifest.json
        ├── config_flow.py
        ├── const.py
        ├── coordinator.py
        ├── switch.py
        ├── fan.py
        └── sensor.py
```

Building the Add-on

```bash
# Clone the repository
git clone https://github.com/jyz0501/hassio-zinguo.git
cd hassio-zinguo

# Build for your architecture
docker build -t ghcr.io/jyz0501/hassio-zinguo-amd64 .
```

Support

· GitHub Issues
· Home Assistant Community

License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments

· Thanks to Zinguo for their bathroom fan products
· Home Assistant community for the excellent platform
· All contributors and testers

```