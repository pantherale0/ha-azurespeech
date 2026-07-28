"""Service actions package for azure_speech."""

from custom_components.azure_speech.const import DOMAIN, LOGGER
from homeassistant.core import HomeAssistant

from .refresh_voices import SERVICE_REFRESH_VOICES_SCHEMA, async_refresh_voices_handler


async def async_setup_services(hass: HomeAssistant) -> None:
    """Register custom service actions for azure_speech in async_setup."""
    if hass.services.has_service(DOMAIN, "refresh_voices"):
        return

    LOGGER.debug("Registering service action %s.refresh_voices", DOMAIN)
    hass.services.async_register(
        DOMAIN,
        "refresh_voices",
        lambda call: async_refresh_voices_handler(hass, call),
        schema=SERVICE_REFRESH_VOICES_SCHEMA,
    )
