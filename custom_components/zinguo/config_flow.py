"""Config flow for Zinguo integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .api import ZinguoAPI  # 假设原项目有 api.py 或类似认证逻辑

_LOGGER = logging.getLogger(__name__)

# 自定义异常类（必须在函数使用前定义）
class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

class InvalidMAC(HomeAssistantError):
    """Error to indicate MAC address is invalid."""

class DeviceNotFound(HomeAssistantError):
    """Error to indicate device not found in account."""

# 配置步骤的 Schema
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required("mac"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    username = data[CONF_USERNAME]
    password = data[CONF_PASSWORD]
    mac = data["mac"].strip().upper().replace(":", "").replace("-", "")

    if len(mac) != 12:
        raise InvalidMAC

    # 尝试登录并验证设备是否存在
    api = ZinguoAPI(username, password)
    try:
        await hass.async_add_executor_job(api.login)
        device = await hass.async_add_executor_job(api.get_device_info, mac)
        if not device:
            raise DeviceNotFound
    except Exception as ex:
        # 根据异常类型抛出特定错误
        if "auth" in str(ex).lower():
            raise InvalidAuth from ex
        elif "connect" in str(ex).lower() or "timeout" in str(ex).lower():
            raise CannotConnect from ex
        else:
            _LOGGER.error("Zinguo login or device fetch failed: %s", ex)
            raise CannotConnect from ex

    # 返回用于创建配置条目的信息
    return {"title": f"Zinguo {mac[-4:]}", "mac": mac}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zinguo."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except InvalidMAC:
                errors["base"] = "invalid_mac"
            except DeviceNotFound:
                errors["base"] = "device_not_found"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # 确保不会重复添加同一 MAC
                await self.async_set_unique_id(info["mac"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
