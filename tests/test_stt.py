"""Tests for Azure Speech STT platform."""

from unittest.mock import AsyncMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.azure_speech.stt import AzureSpeechSTTEntity
from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechMetadata,
    SpeechResultState,
)
from homeassistant.core import HomeAssistant


async def mock_stream(chunks: list[bytes]):
    """Async generator yielding byte chunks."""
    for chunk in chunks:
        yield chunk


async def test_stt_transcribe(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api_client: AsyncMock,
) -> None:
    """Test STT entity audio processing and transcription."""
    mock_config_entry.add_to_hass(hass)

    with patch(
        "custom_components.azure_speech.AzureSpeechApiClient",
        return_value=mock_api_client,
    ):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        stt_entity = AzureSpeechSTTEntity(mock_config_entry)
        metadata = SpeechMetadata(
            language="en-US",
            format=AudioFormats.WAV,
            codec=AudioCodecs.PCM,
            bit_rate=AudioBitRates.BITRATE_16,
            sample_rate=AudioSampleRates.SAMPLERATE_16000,
            channel=AudioChannels.CHANNEL_MONO,
        )

        res = await stt_entity.async_process_audio_stream(
            metadata=metadata,
            stream=mock_stream([b"pcm_data_chunk_1", b"pcm_data_chunk_2"]),
        )

        assert res.result == SpeechResultState.SUCCESS
        assert res.text == "Hello Home Assistant"
