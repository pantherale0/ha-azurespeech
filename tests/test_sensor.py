"""Tests for Azure Speech sensor platform."""

from unittest.mock import AsyncMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant


async def test_sensors_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api_client: AsyncMock,
) -> None:
    """Test Azure Speech connection and voices count diagnostic sensors."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "custom_components.azure_speech.AzureSpeechApiClient",
        return_value=mock_api_client,
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        connection_sensor = hass.states.get("sensor.azure_speech_eastus_api_connection_status")
        voices_count_sensor = hass.states.get("sensor.azure_speech_eastus_cached_voices_count")

        assert connection_sensor is not None
        assert connection_sensor.state == "online"

        assert voices_count_sensor is not None
        assert voices_count_sensor.state == "2"
