"""Switch platform for Zinguo."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ZinguoDataUpdateCoordinator # 导入协调器类型

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Zinguo switch based on a config entry."""
    # 从 hass.data 中获取协调器实例
    coordinator: ZinguoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # 从协调器的 data 中获取设备信息
    device_info = coordinator.data # 根据 coordinator.py 的实现，这里应该是单个设备的字典

    entities = []
    # 创建开关实体，传入协调器对象
    entities.append(ZinguoWarmingSwitch1(coordinator, device_info))
    entities.append(ZinguoWarmingSwitch2(coordinator, device_info))
    entities.append(ZinguoWindSwitch(coordinator, device_info))

    async_add_entities(entities)


class ZinguoSwitchBase(CoordinatorEntity, SwitchEntity):
    """Base class for Zinguo switches."""

    def __init__(self, coordinator: ZinguoDataUpdateCoordinator, device_info: dict[str, Any], control_key: str, name_suffix: str):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device_info = device_info
        self._control_key = control_key
        self._attr_unique_id = f"{device_info['id']}_{control_key}" # Construct unique_id
        self._attr_name = f"Zinguo {name_suffix}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_info["id"])},
            "name": coordinator.name, # Use coordinator's determined name
            "manufacturer": "Zinguo",
            "model": device_info.get("device_model", "Unknown Model"), # Use model from device_info
            "sw_version": device_info.get("firmware_version", "Unknown Version"), # Use firmware version if available
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # 根据协调器的最新数据更新开关状态
        device_status = self.coordinator.data # Get fresh data
        # Assuming device_status has a 'status' key with control details
        status_details = device_status.get('status', {})
        # Map control_key to actual state in status_details if structure differs
        # Example: if status_details['warming_switch_1'] exists and is boolean
        self._attr_is_on = status_details.get(self._control_key, False)
        self.async_write_ha_state() # Notify HA of state change

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # 直接使用协调器发送控制命令
        await self.coordinator.send_control_command({self._control_key: True})
        # 状态更新由协调器的强制刷新处理

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
         # 直接使用协调器发送控制命令
        await self.coordinator.send_control_command({self._control_key: False})
        # 状态更新由协调器的强制刷新处理


class ZinguoWarmingSwitch1(ZinguoSwitchBase):
    def __init__(self, coordinator: ZinguoDataUpdateCoordinator, device_info: dict[str, Any]):
        super().__init__(coordinator, device_info, "warming_switch_1", "Warming Switch 1")


class ZinguoWarmingSwitch2(ZinguoSwitchBase):
    def __init__(self, coordinator: ZinguoDataUpdateCoordinator, device_info: dict[str, Any]):
        super().__init__(coordinator, device_info, "warming_switch_2", "Warming Switch 2")


class ZinguoWindSwitch(ZinguoSwitchBase):
    def __init__(self, coordinator: ZinguoDataUpdateCoordinator, device_info: dict[str, Any]):
        # --- 修正 unique_id ---
        super().__init__(coordinator, device_info, "wind_switch", "Wind Switch") # Changed control_key to "wind_switch"
        # The unique_id is now correctly f"{device_info['id']}_wind_switch"
