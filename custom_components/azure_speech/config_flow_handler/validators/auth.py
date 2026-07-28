"""Validation functions for Azure Speech config flow authentication."""

from __future__ import annotations

import aiohttp

from custom_components.azure_speech.api import AzureSpeechApiClient


async def validate_auth_input(
    session: aiohttp.ClientSession,
    api_key: str,
    region: str,
    endpoint: str | None = None,
) -> dict[str, str]:
    """Validate Azure Speech API key and region by calling the voices endpoint.

    :return: Dict containing title or metadata if successful.
    :raises AzureSpeechApiClientAuthenticationError: On 401/403.
    :raises AzureSpeechApiClientError: On other API errors.
    """
    client = AzureSpeechApiClient(
        api_key=api_key,
        region=region,
        session=session,
        endpoint=endpoint,
    )
    voices = await client.get_voices()
    return {"title": f"Azure Speech ({region})", "voice_count": str(len(voices))}
