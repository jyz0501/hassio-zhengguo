Zinguo Bathroom Fan Home Assistant Integration

https://img.shields.io/badge/HACS-Custom-41BDF5.svg
https://img.shields.io/github/release/jyz0501/hassio-zinguo.svg
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/Home%20Assistant-2023.8%2B-blue

A complete integration for Zinguo Smart Bathroom Fan (浴霸) for Home Assistant. This integration provides full control of your Zinguo bathroom fan through a user-friendly interface with secure credential storage.

✨ Features

🎛️ Complete Device Control

· Fan Entity with preset modes: Off, Cool, Heat Low, Heat High
· Individual Switches: Light, Ventilation, Wind, Heater 1, Heater 2
· Temperature Sensor: Real-time temperature monitoring
· Online Status: Device connection status monitoring

🔒 Security & Privacy

· Secure credential storage using Home Assistant's encrypted storage
· Automatic token management and refresh
· No third-party servers - direct communication with Zinguo API
· No tracking or analytics

🚀 Easy to Use

· Config Flow UI: No YAML editing required
· Auto-discovery: Automatic device status polling
· Error Handling: Automatic reconnection and error recovery
· Mobile Friendly: Works perfectly in Home Assistant mobile app

🔄 API Functions Mapping

Chinese Function Integration Feature Description
吹风 (Chuifeng) Cool Mode Wind only
换气 (Huanqi) Ventilation Switch Ventilation only
暖风1 (Nuanfeng1) Heat Low Mode Heater 1 + Wind
暖风2 (Nuanfeng2) Heat High Mode Heater 2 + Wind
全关 (Quanguan) Turn Off All All functions off

📦 Installation

Method 1: HACS (Recommended)

1. Open HACS in your Home Assistant
2. Go to Integrations
3. Click the three dots menu (⋮) → Custom repositories
4. Add repository URL: https://github.com/jyz0501/hassio-zinguo
5. Category: Integration
6. Search for "Zinguo Bathroom Fan" and click Download
7. Restart Home Assistant

Method 2: Home Assistant Add-on

1. Go to Supervisor → Add-on Store
2. Click three dots menu → Repositories
3. Add: https://github.com/jyz0501/hassio-zinguo
4. Install "Zinguo Bathroom Fan" add-on
5. Start the add-on
6. Restart Home Assistant

Method 3: Manual Installation

1. Download the latest release from Releases
2. Extract the custom_components/zinguo folder
3. Copy it to your Home Assistant config/custom_components/ directory
4. Restart Home Assistant

⚙️ Configuration

Step 1: Add Integration

1. After installation, go to Settings → Devices & Services
2. Click + ADD INTEGRATION (bottom right)
3. Search for "Zinguo Bathroom Fan"
4. Click to start setup

Step 2: Enter Credentials

Enter the following information in the setup wizard:

Field Description Example
Account Your Zinguo account phone number 18663531366
Password Your Zinguo account password Your password
MAC Address Device MAC address (12 uppercase chars) C44F33D86409
Name Custom name for your device Bathroom Fan

Note: The MAC address should be 12 characters, uppercase, no colons or dashes.

🏠 Entities Created

After successful configuration, the following entities will be created:

Fan Entity

· fan.[device_name]_fan - Main fan control with preset modes

Switch Entities

· switch.[device_name]_light - Bathroom light control
· switch.[device_name]_ventilation - Ventilation mode
· switch.[device_name]_wind - Wind only mode
· switch.[device_name]_heater_1 - Heater 1 control
· switch.[device_name]_heater_2 - Heater 2 control

Sensor Entities

· sensor.[device_name]_temperature - Current temperature
· sensor.[device_name]_online_status - Device connection status

🤖 Automation Examples

Example 1: Morning Shower Routine

```yaml
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
          entity_id: fan.bathroom_fan_fan
        data:
          preset_mode: "heat_low"
      - delay:
          minutes: 30
      - service: fan.set_preset_mode
        target:
          entity_id: fan.bathroom_fan_fan
        data:
          preset_mode: "off"
```

Example 2: Humidity Control

```yaml
automation:
  - alias: "Bathroom Humidity Control"
    trigger:
      platform: numeric_state
      entity_id: sensor.bathroom_humidity
      above: 75
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.bathroom_fan_ventilation
      - delay:
          minutes: 20
      - service: switch.turn_off
        target:
          entity_id: switch.bathroom_fan_ventilation
```

Example 3: Motion-Activated Light

```yaml
automation:
  - alias: "Bathroom Motion Light"
    trigger:
      platform: state
      entity_id: binary_sensor.bathroom_motion
      to: "on"
    condition:
      condition: sun
      after: sunset
      before: sunrise
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.bathroom_fan_light
      - delay:
          minutes: 5
      - service: switch.turn_off
        target:
          entity_id: switch.bathroom_fan_light
```

Example 4: Temperature-Based Heating

```yaml
automation:
  - alias: "Auto Heat When Cold"
    trigger:
      platform: numeric_state
      entity_id: sensor.bathroom_temperature
      below: 18
    condition:
      condition: state
      entity_id: binary_sensor.bathroom_occupancy
      state: "on"
    action:
      service: fan.set_preset_mode
      target:
        entity_id: fan.bathroom_fan_fan
      data:
        preset_mode: "heat_low"
```

📱 Dashboard Cards

Lovelace Button Card Example

```yaml
type: vertical-stack
cards:
  - type: entity
    entity: fan.bathroom_fan_fan
    name: Bathroom Fan
  - type: horizontal-stack
    cards:
      - type: button
        tap_action:
          action: call-service
          service: fan.set_preset_mode
          service_data:
            preset_mode: cool
          target:
            entity_id: fan.bathroom_fan_fan
        icon: mdi:fan
        name: Cool
      - type: button
        tap_action:
          action: call-service
          service: fan.set_preset_mode
          service_data:
            preset_mode: heat_low
          target:
            entity_id: fan.bathroom_fan_fan
        icon: mdi:radiator
        name: Heat Low
      - type: button
        tap_action:
          action: call-service
          service: fan.set_preset_mode
          service_data:
            preset_mode: heat_high
          target:
            entity_id: fan.bathroom_fan_fan
        icon: mdi:radiator
        name: Heat High
```

Entity Card for All Controls

```yaml
type: entities
title: Bathroom Fan Controls
entities:
  - entity: fan.bathroom_fan_fan
  - entity: switch.bathroom_fan_light
  - entity: switch.bathroom_fan_ventilation
  - entity: sensor.bathroom_fan_temperature
  - entity: sensor.bathroom_fan_online_status
```

🔧 Troubleshooting

Integration Not Appearing

1. ✅ Restart Home Assistant after installation
2. ✅ Check that custom_components/zinguo folder exists
3. ✅ Verify all Python files are present
4. ✅ Check Home Assistant logs for errors

Cannot Connect to Device

1. ✅ Verify device is online in the Zinguo mobile app
2. ✅ Check MAC address format (12 uppercase characters, no separators)
3. ✅ Confirm account credentials are correct
4. ✅ Ensure your Home Assistant has internet access

Entities Not Updating

1. ✅ Check sensor.[device_name]_online_status
2. ✅ Verify network connectivity from Home Assistant
3. ✅ Check Home Assistant logs for API errors
4. ✅ Try restarting the integration

Error Messages in Logs

Common errors and solutions:

Error Message Solution
"Login failed" Check account/password
"Device not found" Verify MAC address
"Token expired" Integration will auto-retry
"Connection timeout" Check network connectivity

📊 Logging

To enable debug logging, add to your configuration.yaml:

```yaml
logger:
  default: info
  logs:
    custom_components.zinguo: debug
```

This will provide detailed information about API calls and device status.

🔄 Updating

Via HACS

1. Open HACS → Integrations
2. Find "Zinguo Bathroom Fan"
3. Click UPDATE if available
4. Restart Home Assistant

Manual Update

1. Download the new release
2. Replace custom_components/zinguo folder
3. Restart Home Assistant

🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Report Issues: Found a bug? Open an issue
2. Suggest Features: Have an idea? Share it in the issues
3. Pull Requests: Want to contribute code? Submit a PR
4. Testing: Help test new features and releases
5. Documentation: Improve documentation or translations

Development Setup

```bash
# Clone the repository
git clone https://github.com/jyz0501/hassio-zinguo.git
cd hassio-zinguo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

· Thanks to Zinguo for their smart bathroom fan products
· Home Assistant community for the amazing platform
· All contributors and testers who help improve this integration
· Special thanks to early adopters for feedback and bug reports

📞 Support

· 📖 Documentation: This README and Wiki
· 🐛 Bug Reports: GitHub Issues
· 💬 Community: Home Assistant Community
· ⭐ Star: If you like this project, please give it a star!

🔗 Useful Links

· Zinguo Official Website
· Home Assistant Documentation
· HACS Documentation
· Community Forum Thread

---

Enjoy your smart bathroom experience with Home Assistant! 🚿✨

If this integration has made your life easier, consider supporting the project by starring the repository or contributing to its development.