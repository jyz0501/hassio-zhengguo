# switch.py
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_OFF, STATE_ON

from .const import DOMAIN
from .coordinator import ZinguoDataUpdateCoordinator
from .api import ZinguoAPI # 确保导入 API 类

_LOGGER = logging.getLogger(__name__)

class ZinguoWarmingSwitch1(SwitchEntity):
    """Representation of a Zinguo Warming Switch 1."""

    def __init__(self, coordinator: ZinguoDataUpdateCoordinator, device_info: dict, api: ZinguoAPI):
        """Initialize the switch."""
        self.coordinator = coordinator
        self._device_info = device_info
        self._api = api
        self._attr_unique_id = f"{DOMAIN}_{device_info['id']}_warming_switch_1"
        self._attr_name = f"{device_info.get('name', 'Zinguo Device')} Warming Switch 1"
        self._attr_available = True
        self._state = False # 初始状态

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # 根据协调器状态或设备在线状态判断
        return self.coordinator.last_update_success and self._device_info.get('online', True)

    @property
    def is_on(self) -> bool:
        """Return true if the entity is on."""
        return self._state

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # 从协调器数据中获取当前开关状态
        device_data = self.coordinator.data.get(self._device_info['id'])
        if device_data:
            # 假设 API 返回的设备状态中有 'warmingSwitch1'
            self._state = device_data.get('warmingSwitch1', STATE_OFF) == STATE_ON
            self.async_write_ha_state() # 通知 HA 状态已更新

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        _LOGGER.debug(f"Turning on Warming Switch 1 for device {self._device_info['id']}")
        # 直接调用 API 控制命令，不再强制关闭其他开关
        await self._api.send_control_command(
            device_id=self._device_info["id"],
            command="warmingSwitch1",
            value=STATE_ON
        )
        # 状态更新由协调器轮询完成

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        _LOGGER.debug(f"Turning off Warming Switch 1 for device {self._device_info['id']}")
        # 直接调用 API 控制命令
        await self._api.send_control_command(
            device_id=self._device_info["id"],
            command="warmingSwitch1",
            value=STATE_OFF
        )
        # 状态更新由协调器轮询完成


class ZinguoWarmingSwitch2(SwitchEntity):
    """Representation of a Zinguo Warming Switch 2."""

    def __init__(self, coordinator: ZinguoDataUpdateCoordinator, device_info: dict, api: ZinguoAPI):
        """Initialize the switch."""
        self.coordinator = coordinator
        self._device_info = device_info
        self._api = api
        self._attr_unique_id = f"{DOMAIN}_{device_info['id']}_warming_switch_2"
        self._attr_name = f"{device_info.get('name', 'Zinguo Device')} Warming Switch 2"
        self._attr_available = True
        self._state = False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self._device_info.get('online', True)

    @property
    def is_on(self) -> bool:
        """Return true if the entity is on."""
        return self._state

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device_data = self.coordinator.data.get(self._device_info['id'])
        if device_data:
            self._state = device_data.get('warmingSwitch2', STATE_OFF) == STATE_ON
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        _LOGGER.debug(f"Turning on Warming Switch 2 for device {self._device_info['id']}")
        # 直接调用 API 控制命令，不再强制关闭其他开关
        await self._api.send_control_command(
            device_id=self._device_info["id"],
            command="warmingSwitch2",
            value=STATE_ON
        )

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        _LOGGER.debug(f"Turning off Warming Switch 2 for device {self._device_info['id']}")
        await self._api.send_control_command(
            device_id=self._device_info["id"],
            command="warmingSwitch2",
            value=STATE_OFF
        )


class ZinguoWindSwitch(SwitchEntity):
    """Representation of a Zinguo Wind Switch."""

    def __init__(self, coordinator: ZinguoDataUpdateCoordinator, device_info: dict, api: ZinguoAPI):
        """Initialize the switch."""
        self.coordinator = coordinator
        self._device_info = device_info
        self._api = api
        self._attr_unique_id = f"{DOMAIN}_{device_info['id']}_wind_switch"
        self._attr_name = f"{device_info.get('name', 'Zinguo Device')} Wind Switch"
        self._attr_available = True
        self._state = False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self._device_info.get('online', True)

    @property
    def is_on(self) -> bool:
        """Return true if the entity is on."""
        return self._state

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device_data = self.coordinator.data.get(self._device_info['id'])
        if device_data:
            self._state = device_data.get('wind', STATE_OFF) == STATE_ON
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        _LOGGER.debug(f"Turning on Wind Switch for device {self._device_info['id']}")
        # 直接调用 API 控制命令
        await self._api.send_control_command(
            device_id=self._device_info["id"],
            command="wind",
            value=STATE_ON
        )

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        _LOGGER.debug(f"Turning off Wind Switch for device {self._device_info['id']}")
        await self._api.send_control_command(
            device_id=self._device_info["id"],
            command="wind",
            value=STATE_OFF
        )

# ... 其他开关类 ...

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> bool:
    """Set up the Zinguo switch platform."""
    coordinator: ZinguoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api: ZinguoAPI = hass.data[DOMAIN][entry.entry_id]["api"]

    entities = []
    for device_info in coordinator.data.values():
        # 确保这里添加了你想要的开关实体
        entities.append(ZinguoWarmingSwitch1(coordinator, device_info, api))
        entities.append(ZinguoWarmingSwitch2(coordinator, device_info, api))
        entities.append(ZinguoWindSwitch(coordinator, device_info, api))
        # ... 添加其他开关 ...

    async_add_entities(entities)
    return True
