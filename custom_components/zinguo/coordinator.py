"""DataUpdateCoordinator for Zinguo integration."""
import logging
from datetime import timedelta

import aiohttp
import async_timeout # Added missing import
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryAuthFailed # Added for better auth handling

from .const import (
    LOGIN_URL,
    DEVICES_URL,
    CONTROL_URL
)

_LOGGER = logging.getLogger(__name__)

class ZinguoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Zinguo data."""

    def __init__(self, hass, account, password, mac, name):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=30), # Changed back from 300 to 30 for more frequent updates, adjust as needed
        )
        self.account = account
        self.password = password
        self.mac = mac
        self.token = None
        self._session = aiohttp.ClientSession() # Create a shared session

    async def _async_update_data(self):
        """Update data via API."""
        try:
            async with async_timeout.timeout(30):
                # Login if needed
                if not self.token:
                    await self._login()

                # Get device status
                device_data = await self._get_device_status()
                # Process the raw data into a format suitable for entities
                processed_data = self._process_device_data(device_data)
                return processed_data

        except ConfigEntryAuthFailed as err:
            # If authentication fails during an update, clear the token and re-raise
            _LOGGER.error("Authentication failed during update: %s", err)
            self.token = None
            raise
        except Exception as err:
            _LOGGER.error("Error updating Zinguo data: %s", err)
            # Try to re-login on error, especially for 401
            if isinstance(err, aiohttp.ClientResponseError) and err.status == 401:
                 _LOGGER.debug("Got 401 during update, clearing token for re-login.")
                 self.token = None
            raise UpdateFailed(f"Error communicating with API: {err}")

    def _process_device_data(self, raw_data: dict) -> dict:
        """Process raw device data into a standardized format for entities."""
        # Define mapping for switch states: Adjust these values based on your actual API response meaning.
        # From your sample: warmingSwitch1: 2, windSwitch: 2, etc.
        # Assuming 2 = ON, 1 = OFF (or maybe 0 = OFF). Confirm this.
        status_map = {2: True, 1: False} # Modify if 0 means OFF instead of 1
        # status_map = {2: True, 0: False} # Use this if 0 means OFF

        processed = {
            "id": raw_data.get("_id"),
            "mac": raw_data.get("mac"),
            "name": raw_data.get("name"),
            "online": raw_data.get("online"),
            "temperature": raw_data.get("temperature"),
            "light_switch": status_map.get(raw_data.get("lightSwitch"), False), # Default to False if unknown state
            "warming_switch_1": status_map.get(raw_data.get("warmingSwitch1"), False),
            "warming_switch_2": status_map.get(raw_data.get("warmingSwitch2"), False),
            "wind_switch": status_map.get(raw_data.get("windSwitch"), False),
            "ventilation_switch": status_map.get(raw_data.get("ventilationSwitch"), False),
            "comovement": raw_data.get("comovement"), # Might need processing if it controls modes
            "hardware_version": raw_data.get("hardwareVersion"),
            "software_version": raw_data.get("softwareVersion"),
            # Add other relevant fields you might want to expose as sensors
        }
        _LOGGER.debug("Processed device data: %s", processed)
        return processed

    async def _login(self):
        """Login to Zinguo API."""
        payload = {
            "account": self.account,
            "password": self.password
        }

        # Use the shared session
        async with self._session.post(LOGIN_URL, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                self.token = data.get("token")
                if not self.token:
                    _LOGGER.error("Login failed: No token received in response: %s", data)
                    raise ConfigEntryAuthFailed("Login failed: No token received")
                _LOGGER.debug("Login successful for account: %s", self.account)
            elif response.status == 401:
                 _LOGGER.error("Login failed: Invalid credentials for account: %s", self.account)
                 raise ConfigEntryAuthFailed("Invalid credentials")
            else:
                text_response = await response.text() # Capture response body for error details
                _LOGGER.error("Login failed with status %d: %s", response.status, text_response)
                raise ConfigEntryAuthFailed(f"Login failed with status {response.status}: {text_response}")

    async def _get_device_status(self):
        """Get device status from API."""
        if not self.token:
            raise UpdateFailed("Cannot fetch status: Not logged in")

        headers = {"x-access-token": self.token}

        # Use the shared session
        async with self._session.get(DEVICES_URL, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # Find our device by MAC
                for device in data:
                    if device.get("mac") == self.mac:
                        _LOGGER.debug("Fetched raw device status for MAC %s: %s", self.mac, device)
                        return device
                _LOGGER.error("Device with MAC %s not found in API response.", self.mac)
                raise UpdateFailed(f"Device with MAC {self.mac} not found")
            elif response.status == 401:
                # Token expired, re-login
                _LOGGER.warning("Token expired while fetching device status, attempting re-login.")
                self.token = None
                await self._login()
                return await self._get_device_status() # Retry after re-login
            else:
                text_response = await response.text()
                _LOGGER.error("Failed to get device status for MAC %s, status %d: %s", self.mac, response.status, text_response)
                raise UpdateFailed(f"Failed to get device status: Status {response.status}, Response: {text_response}")

    async def send_control_command(self, payload):
        """Send control command to device."""
        if not self.token:
            await self._login()

        headers = {
            "x-access-token": self.token,
            "Content-Type": "application/json"
        }

        # Add common fields to payload using the stored MAC and account
        control_payload = {
            "mac": self.mac,
            "masterUser": self.account,
            "setParamter": False, # Verify if these defaults are correct for your API
            "action": False,      # Verify if these defaults are correct for your API
            **payload
        }

        _LOGGER.debug("Sending control command: %s", control_payload)

        # Use the shared session
        async with self._session.put(CONTROL_URL, json=control_payload, headers=headers) as response:
            if response.status == 200:
                _LOGGER.debug("Control command sent successfully.")
                # Force immediate update to reflect changes
                await self.async_request_refresh()
                return True
            elif response.status == 401:
                # Token expired, re-login and retry once
                _LOGGER.warning("Token expired while sending control command, attempting re-login and retry.")
                self.token = None
                await self._login()
                # Retry the command once after re-login
                # Recreate the payload just in case (though unlikely to change)
                control_payload_retry = {
                    "mac": self.mac,
                    "masterUser": self.account,
                    "setParamter": False,
                    "action": False,
                    **payload
                }
                async with self._session.put(CONTROL_URL, json=control_payload_retry, headers=headers) as retry_resp:
                    if retry_resp.status == 200:
                        _LOGGER.debug("Control command sent successfully after re-login.")
                        await self.async_request_refresh()
                        return True
                    else:
                        retry_text_response = await retry_resp.text()
                        _LOGGER.error("Control command failed after re-login, status %d: %s", retry_resp.status, retry_text_response)
                        return False
            else:
                text_response = await response.text()
                _LOGGER.error("Control command failed for MAC %s, status %d: %s", self.mac, response.status, text_response)
                return False

    async def async_shutdown(self):
        """Close the shared aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
        await super().async_shutdown()
