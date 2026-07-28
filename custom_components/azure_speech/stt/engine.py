"""Speech-to-text platform entity for Azure Speech integration."""

from __future__ import annotations

from collections.abc import AsyncIterable

from custom_components.azure_speech.api import AzureSpeechApiClientError
from custom_components.azure_speech.const import (
    CONF_LANGUAGE,
    CONF_PROFANITY_MODE,
    DEFAULT_LANGUAGE,
    DEFAULT_PROFANITY_MODE,
)
from custom_components.azure_speech.data import AzureSpeechConfigEntry
from custom_components.azure_speech.entity import AzureSpeechEntity
from custom_components.azure_speech.entity_utils import wrap_pcm_in_wav
from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
    SpeechToTextEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback


class AzureSpeechSTTEntity(SpeechToTextEntity, AzureSpeechEntity):
    """Azure Speech Speech-to-Text entity implementation."""

    def __init__(
        self,
        entry: AzureSpeechConfigEntry,
    ) -> None:
        """Initialize Azure Speech STT entity."""
        coordinator = entry.runtime_data.coordinator
        description = EntityDescription(
            key="stt",
            name="Azure Speech STT",
        )
        super().__init__(coordinator, description)
        self._entry = entry

    @property
    def supported_languages(self) -> list[str]:
        """Return supported languages for STT transcription."""
        return [
            "en-US",
            "en-GB",
            "en-AU",
            "en-CA",
            "de-DE",
            "fr-FR",
            "es-ES",
            "it-IT",
            "ja-JP",
            "zh-CN",
            "nl-NL",
            "pt-BR",
            "ru-RU",
        ]

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return supported audio container formats."""
        return [AudioFormats.WAV, AudioFormats.OGG]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return supported audio codecs."""
        return [AudioCodecs.PCM, AudioCodecs.OPUS]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        """Return supported audio bit rates."""
        return [AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        """Return supported audio sample rates."""
        return [AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        """Return supported audio channels."""
        return [AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self,
        metadata: SpeechMetadata,
        stream: AsyncIterable[bytes],
    ) -> SpeechResult:
        """Process incoming audio stream and transcribe to text.

        :param metadata: SpeechMetadata specifying format, codec, sample rate, language.
        :param stream: AsyncIterable streaming audio byte chunks.
        :return: SpeechResult object.
        """
        audio_chunks: list[bytes] = [chunk async for chunk in stream]
        raw_audio = b"".join(audio_chunks)
        if not raw_audio:
            return SpeechResult(text="", result=SpeechResultState.ERROR)

        if raw_audio.startswith(b"RIFF"):
            wav_payload = raw_audio
        else:
            wav_payload = wrap_pcm_in_wav(
                pcm_bytes=raw_audio,
                sample_rate=metadata.sample_rate,
                channels=metadata.channel,
                bit_depth=metadata.bit_rate,
            )

        language = metadata.language or self._entry.options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE)
        profanity_mode = self._entry.options.get(CONF_PROFANITY_MODE, DEFAULT_PROFANITY_MODE)

        try:
            res = await self.coordinator.client.transcribe_stt_audio(
                wav_audio_bytes=wav_payload,
                language=language,
                profanity_mode=profanity_mode,
            )
            status = res.get("RecognitionStatus")
            display_text = res.get("DisplayText", "")

            if status == "Success":
                return SpeechResult(text=display_text, result=SpeechResultState.SUCCESS)
            if status in ("NoMatch", "InitialSilenceTimeout"):
                return SpeechResult(text="", result=SpeechResultState.SUCCESS)

            return SpeechResult(text="", result=SpeechResultState.ERROR)
        except AzureSpeechApiClientError, TimeoutError:
            return SpeechResult(text="", result=SpeechResultState.ERROR)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AzureSpeechConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Azure Speech STT platform."""
    async_add_entities([AzureSpeechSTTEntity(entry)])
