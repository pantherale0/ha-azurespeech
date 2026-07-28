"""Service action to refresh Azure Speech cached voices list."""

from __future__ import annotations

import voluptuous as vol

from custom_components.azure_speech.const import DOMAIN, LOGGER
from homeassistant.core import HomeAssistant, ServiceCall

SERVICE_REFRESH_VOICES_SCHEMA = vol.Schema({})


async def async_refresh_voices_handler(
    hass: HomeAssistant,
    call: ServiceCall,
) -> None:
    """Handle the azure_speech.refresh_voices service action."""
    LOGGER.debug("Triggering manual refresh of Azure Speech voices")
    entries = hass.config_entries.async_entries(DOMAIN)
    for entry in entries:
        if hasattr(entry, "runtime_data") and entry.runtime_data:
            coordinator = entry.runtime_data.coordinator
            await coordinator.async_refresh()
