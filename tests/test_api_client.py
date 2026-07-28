"""Tests for AzureSpeechApiClient."""

from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from custom_components.azure_speech.api import (
    AzureSpeechApiClient,
    AzureSpeechApiClientAuthenticationError,
    AzureSpeechApiClientRateLimitError,
)


@pytest.mark.asyncio
async def test_get_voices_success() -> None:
    """Test get_voices successfully returns voices list."""
    mock_session = MagicMock(spec=aiohttp.ClientSession)
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=[{"ShortName": "en-US-AvaMultilingualNeural"}])

    mock_get = AsyncMock(return_value=mock_response)
    mock_session.get = mock_get

    client = AzureSpeechApiClient(
        api_key="test_key",
        region="eastus",
        session=mock_session,
    )

    voices = await client.get_voices()
    assert len(voices) == 1
    assert voices[0]["ShortName"] == "en-US-AvaMultilingualNeural"


@pytest.mark.asyncio
async def test_get_voices_auth_error() -> None:
    """Test get_voices raises AzureSpeechApiClientAuthenticationError on HTTP 401."""
    mock_session = MagicMock(spec=aiohttp.ClientSession)
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 401
    mock_session.get = AsyncMock(return_value=mock_response)

    client = AzureSpeechApiClient(
        api_key="invalid_key",
        region="eastus",
        session=mock_session,
    )

    with pytest.raises(AzureSpeechApiClientAuthenticationError):
        await client.get_voices()


@pytest.mark.asyncio
async def test_get_voices_rate_limit() -> None:
    """Test get_voices raises AzureSpeechApiClientRateLimitError on HTTP 429."""
    mock_session = MagicMock(spec=aiohttp.ClientSession)
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 429
    mock_response.headers = {"Retry-After": "45"}
    mock_session.get = AsyncMock(return_value=mock_response)

    client = AzureSpeechApiClient(
        api_key="test_key",
        region="eastus",
        session=mock_session,
    )

    with pytest.raises(AzureSpeechApiClientRateLimitError) as exc_info:
        await client.get_voices()
    assert exc_info.value.retry_after == 45


@pytest.mark.asyncio
async def test_generate_tts_audio_success() -> None:
    """Test generate_tts_audio returns binary audio data."""
    mock_session = MagicMock(spec=aiohttp.ClientSession)
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 200
    mock_response.read = AsyncMock(return_value=b"audio_payload")
    mock_session.post = AsyncMock(return_value=mock_response)

    client = AzureSpeechApiClient(
        api_key="test_key",
        region="eastus",
        session=mock_session,
    )

    audio = await client.generate_tts_audio("<ssml></ssml>")
    assert audio == b"audio_payload"


@pytest.mark.asyncio
async def test_transcribe_stt_audio_success() -> None:
    """Test transcribe_stt_audio returns recognized text payload."""
    mock_session = MagicMock(spec=aiohttp.ClientSession)
    mock_response = AsyncMock(spec=aiohttp.ClientResponse)
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"RecognitionStatus": "Success", "DisplayText": "Hello World"})
    mock_session.post = AsyncMock(return_value=mock_response)

    client = AzureSpeechApiClient(
        api_key="test_key",
        region="eastus",
        session=mock_session,
    )

    res = await client.transcribe_stt_audio(b"wav_bytes")
    assert res["RecognitionStatus"] == "Success"
    assert res["DisplayText"] == "Hello World"
