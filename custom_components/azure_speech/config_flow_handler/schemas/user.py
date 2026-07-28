"""Schema definitions for user step in Azure Speech config flow."""

import voluptuous as vol

from custom_components.azure_speech.const import AZURE_REGIONS, CONF_API_KEY, CONF_ENDPOINT, CONF_REGION, DEFAULT_REGION
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)


def get_user_schema(
    default_region: str = DEFAULT_REGION,
    default_endpoint: str = "",
) -> vol.Schema:
    """Build the voluptuous schema for user setup step."""
    return vol.Schema(
        {
            vol.Required(CONF_API_KEY): TextSelector(
                TextSelectorConfig(
                    type=TextSelectorType.PASSWORD,
                    autocomplete="current-password",
                )
            ),
            vol.Required(CONF_REGION, default=default_region): SelectSelector(
                SelectSelectorConfig(
                    options=AZURE_REGIONS,
                    mode=SelectSelectorMode.DROPDOWN,
                    custom_value=True,
                )
            ),
            vol.Optional(CONF_ENDPOINT, default=default_endpoint): TextSelector(
                TextSelectorConfig(type=TextSelectorType.URL)
            ),
        }
    )
