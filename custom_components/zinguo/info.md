# Zinguo Bathroom Fan

![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)

Integration for Zinguo Smart Bathroom Fan for Home Assistant.

## Features
- 🔧 **Config Flow**: Easy setup through UI
- 🔒 **Secure Storage**: Account credentials stored securely
- 🌀 **Fan Entity**: With preset modes (Off, Cool, Heat Low, Heat High)
- 💡 **Multiple Switches**: Light, Ventilation, Wind, Heater 1, Heater 2
- 🌡️ **Temperature Sensor**: Real-time temperature monitoring
- 📡 **Online Status**: Device connection status
- 🔄 **Auto Token Refresh**: Handles login automatically

## Installation

### Via HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the three dots menu → **Custom repositories**
4. Add: `https://github.com/jyz0501/hassio-zinguo`
5. Category: **Integration**
6. Search for "Zinguo Bathroom Fan" and install
7. Restart Home Assistant

### Manual Installation
1. Download the latest release
2. Copy `custom_components/zinguo` to your Home Assistant `custom_components` folder
3. Restart Home Assistant

## Configuration
1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Zinguo Bathroom Fan**
4. Enter your credentials:
   - Account: Your Zinguo account phone number
   - Password: Your Zinguo account password  
   - MAC Address: Your device MAC address (12 characters)
   - Name: Custom name for your device

## API Functions Mapped
- 吹风 (Chuifeng) → Cool mode
- 换气 (Huanqi) → Ventilation switch
- 暖风1 (Nuanfeng1) → Heat Low mode
- 暖风2 (Nuanfeng2) → Heat High mode
- 全关 (Quanguan) → Turn off all

## Automation Examples

```yaml
# Turn on heat when bathroom is cold
automation:
  - alias: "Bathroom Heat"
    trigger:
      platform: numeric_state
      entity_id: sensor.bathroom_temperature
      below: 20
    action:
      service: fan.set_preset_mode
      target:
        entity_id: fan.zinguo_bathroom_fan_fan
      data:
        preset_mode: "heat_low"

# Turn on ventilation after shower
automation:
  - alias: "Post-Shower Ventilation"
    trigger:
      platform: state
      entity_id: binary_sensor.bathroom_motion
      to: "off"
    condition:
      condition: template
      value_template: >
        {{ is_state('input_boolean.shower_active', 'on') }}
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.zinguo_bathroom_fan_ventilation
      - delay:
          minutes: 30
      - service: switch.turn_off
        target:
          entity_id: switch.zinguo_bathroom_fan_ventilation