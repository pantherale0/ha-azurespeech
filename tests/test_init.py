"""Tests for Azure Speech integration setup and unload lifecycle."""

from unittest.mock import AsyncMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant


async def test_setup_and_unload_entry(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api_client: AsyncMock,
) -> None:
    """Test setting up and unloading Azure Speech config entry."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "custom_components.azure_speech.AzureSpeechApiClient",
        return_value=mock_api_client,
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        assert mock_config_entry.state.name == "LOADED"
        assert mock_config_entry.runtime_data is not None

        assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        assert mock_config_entry.state.name == "NOT_LOADED"
