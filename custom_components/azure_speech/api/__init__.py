"""API client package for Azure Speech."""

from .client import AzureSpeechApiClient
from .exceptions import (
    AzureSpeechApiClientAuthenticationError,
    AzureSpeechApiClientCommunicationError,
    AzureSpeechApiClientError,
    AzureSpeechApiClientRateLimitError,
)

__all__ = [
    "AzureSpeechApiClient",
    "AzureSpeechApiClientAuthenticationError",
    "AzureSpeechApiClientCommunicationError",
    "AzureSpeechApiClientError",
    "AzureSpeechApiClientRateLimitError",
]
