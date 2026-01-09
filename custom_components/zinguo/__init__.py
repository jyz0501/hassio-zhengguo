"""The Zinguo integration."""
import asyncio
import logging
from datetime import timedelta

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ACCOUNT,
    CONF_MAC,
    CONF_NAME,
    DOMAIN,
    LOGIN_URL,
    DEVICES_URL,
    CONTROL_URL,
    SWITCH_TYPES
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch", "fan", "sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Zinguo from a config entry."""
    account = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    mac = entry.data[CONF_MAC]
    name = entry.data.get(CONF_NAME, "Zinguo Bathroom Fan")

    coordinator = ZinguoDataUpdateCoordinator(
        hass, account, password, mac, name
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

class ZinguoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Zinguo data."""

    def __init__(self, hass, account, password, mac, name):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=300),
        )
        self.account = account
        self.password = password
        self.mac = mac
        self.token = None

    async def _async_update_data(self):
        """Update data via API."""
        try:
            async with async_timeout.timeout(30):
                # Login if needed
                if not self.token:
                    await self._login()
                
                # Get device status
                return await self._get_device_status()
                
        except Exception as err:
            _LOGGER.error("Error updating Zinguo data: %s", err)
            # Try to re-login on error
            self.token = None
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def _login(self):
        """Login to Zinguo API."""
        payload = {
            "account": self.account,
            "password": self.password
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(LOGIN_URL, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    self.token = data.get("token")
                    if not self.token:
                        raise Exception("Login failed: No token received")
                    _LOGGER.debug("Login successful")
                else:
                    raise Exception(f"Login failed: {response.status}")
    
    async def _get_device_status(self):
        """Get device status from API."""
        headers = {"x-access-token": self.token}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(DEVICES_URL, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Find our device by MAC
                    for device in data:
                        if device.get("mac") == self.mac:
                            return device
                    raise Exception(f"Device with MAC {self.mac} not found")
                elif response.status == 401:
                    # Token expired, re-login
                    self.token = None
                    await self._login()
                    return await self._get_device_status()
                else:
                    raise Exception(f"Failed to get device status: {response.status}")
    
    async def send_control_command(self, payload):
        """Send control command to device."""
        if not self.token:
            await self._login()
        
        headers = {
            "x-access-token": self.token,
            "Content-Type": "application/json"
        }
        
        # Add common fields to payload
        control_payload = {
            "mac": self.mac,
            "masterUser": self.account,
            "setParamter": False,
            "action": False,
            **payload
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.put(CONTROL_URL, json=control_payload, headers=headers) as response:
                if response.status == 200:
                    # Force immediate update
                    await self.async_request_refresh()
                    return True
                elif response.status == 401:
                    # Token expired, re-login and retry
                    self.token = None
                    await self._login()
                    return await self.send_control_command(payload)
                else:
                    raise Exception(f"Control command failed: {response.status}")
