"""Platform for switch integration."""
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SWITCH_TYPES
from . import ZinguoDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Zinguo switches based on a config entry."""
    coordinator: ZinguoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    switches = []
    for switch_type, switch_info in SWITCH_TYPES.items():
        switches.append(
            ZinguoSwitch(coordinator, switch_type, switch_info["name"], switch_info["key"], switch_info["icon"])
        )
    
    async_add_entities(switches, True)

class ZinguoSwitch(SwitchEntity):
    """Representation of a Zinguo switch."""
    
    def __init__(self, coordinator, switch_type, name, key, icon):
        """Initialize the switch."""
        self._coordinator = coordinator
        self._switch_type = switch_type
        self._attr_name = f"{coordinator.name} {name}"
        self._attr_unique_id = f"{coordinator.mac}_{switch_type}"
        self._attr_icon = icon
        self._key = key
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.mac)},
            "name": coordinator.name,
            "manufacturer": "Zinguo",
            "model": "Smart Bathroom Fan",
        }
    
    @property
    def is_on(self):
        """Return true if switch is on."""
        if self._coordinator.data:
            return self._coordinator.data.get(self._key) == 1
        return False
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        payload = {self._key: 1}
        
        # Special handling for different switch types
        if self._switch_type in ["heater1", "heater2"]:
            # Heaters need wind on
            payload["windSwitch"] = 1
        elif self._switch_type == "wind":
            # Turn off heaters when wind only
            payload["warmingSwitch1"] = 0
            payload["warmingSwitch2"] = 0
        
        await self._coordinator.send_control_command(payload)
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        payload = {self._key: 0}
        
        # Special handling for heaters
        if self._switch_type in ["heater1", "heater2"]:
            # Check if both heaters are off, then turn off wind
            current_data = self._coordinator.data
            if current_data:
                heater1_on = current_data.get("warmingSwitch1") == 1
                heater2_on = current_data.get("warmingSwitch2") == 1
                
                if self._switch_type == "heater1" and not heater2_on:
                    payload["windSwitch"] = 0
                elif self._switch_type == "heater2" and not heater1_on:
                    payload["windSwitch"] = 0
        
        await self._coordinator.send_control_command(payload)
    
    @property
    def available(self):
        """Return if entity is available."""
        return self._coordinator.data is not None
    
    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )
    
    async def async_update(self):
        """Update the entity."""
        await self._coordinator.async_request_refresh()
