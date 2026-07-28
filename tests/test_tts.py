"""Tests for Azure Speech TTS platform."""

from unittest.mock import AsyncMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.azure_speech.tts.engine import AzureSpeechTTSEntity
from homeassistant.core import HomeAssistant


async def test_tts_properties_and_audio(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api_client: AsyncMock,
) -> None:
    """Test TTS entity properties and async_get_tts_audio method."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "custom_components.azure_speech.AzureSpeechApiClient",
        return_value=mock_api_client,
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        tts_entity = AzureSpeechTTSEntity(mock_config_entry)
        assert tts_entity.default_language == "en-US"
        assert "en-US" in tts_entity.supported_languages

        audio_format, audio_bytes = await tts_entity.async_get_tts_audio(
            message="Hello world",
            language="en-US",
        )
        assert audio_format == "mp3"
        assert audio_bytes == b"mock_mp3_audio_bytes"
