"""Shared fixtures for azure_speech tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.azure_speech.const import CONF_API_KEY, CONF_REGION, DOMAIN


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable custom integrations in Home Assistant test environment."""
    _ = enable_custom_integrations


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a mock config entry for Azure Speech."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Azure Speech (eastus)",
        data={
            CONF_API_KEY: "test_secret_api_key_12345",
            CONF_REGION: "eastus",
        },
        options={},
        entry_id="test_azure_speech_entry_id",
    )


@pytest.fixture
def mock_voices_list() -> list[dict]:
    """Return a mock list of Azure Speech neural voices."""
    return [
        {
            "Name": "en-US-AvaMultilingualNeural",
            "ShortName": "en-US-AvaMultilingualNeural",
            "Gender": "Female",
            "Locale": "en-US",
            "StyleList": ["cheerful", "sad"],
            "SampleRateHertz": "24000",
            "VoiceType": "Neural",
        },
        {
            "Name": "en-GB-SoniaNeural",
            "ShortName": "en-GB-SoniaNeural",
            "Gender": "Female",
            "Locale": "en-GB",
            "SampleRateHertz": "24000",
            "VoiceType": "Neural",
        },
    ]


@pytest.fixture
def mock_api_client(mock_voices_list: list[dict]) -> Generator[MagicMock]:
    """Return a mocked AzureSpeechApiClient instance."""
    with patch(
        "custom_components.azure_speech.AzureSpeechApiClient",
        autospec=True,
    ) as mock_client_cls:
        client = mock_client_cls.return_value
        client.get_voices = AsyncMock(return_value=mock_voices_list)
        client.generate_tts_audio = AsyncMock(return_value=b"mock_mp3_audio_bytes")
        client.transcribe_stt_audio = AsyncMock(
            return_value={"RecognitionStatus": "Success", "DisplayText": "Hello Home Assistant"}
        )
        yield client
