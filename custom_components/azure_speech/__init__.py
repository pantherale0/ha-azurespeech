"""Custom component integration for Azure Speech."""

from __future__ import annotations

from custom_components.azure_speech.api import AzureSpeechApiClient
from custom_components.azure_speech.const import (
    CONF_API_KEY,
    CONF_ENDPOINT,
    CONF_REGION,
    DEFAULT_REGION,
    DOMAIN,
    PLATFORMS,
)
from custom_components.azure_speech.coordinator import AzureSpeechDataUpdateCoordinator
from custom_components.azure_speech.data import AzureSpeechConfigEntry, AzureSpeechData
from custom_components.azure_speech.service_actions import async_setup_services
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_integration

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Azure Speech component."""
    await async_setup_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: AzureSpeechConfigEntry) -> bool:
    """Set up Azure Speech from a config entry."""
    api_key: str = entry.data[CONF_API_KEY]
    region: str = entry.data.get(CONF_REGION, DEFAULT_REGION)
    endpoint: str | None = entry.data.get(CONF_ENDPOINT)

    session = async_get_clientsession(hass)
    client = AzureSpeechApiClient(
        api_key=api_key,
        region=region,
        session=session,
        endpoint=endpoint,
    )

    coordinator = AzureSpeechDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    integration = await async_get_integration(hass, DOMAIN)
    entry.runtime_data = AzureSpeechData(
        client=client,
        coordinator=coordinator,
        integration=integration,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: AzureSpeechConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: AzureSpeechConfigEntry) -> None:
    """Reload a config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)
