"""Custom types for azure_speech.

This module defines the runtime data structure attached to each config entry.
Access pattern: entry.runtime_data.client / entry.runtime_data.coordinator
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import AzureSpeechApiClient
    from .coordinator import AzureSpeechDataUpdateCoordinator


type AzureSpeechConfigEntry = ConfigEntry[AzureSpeechData]


@dataclass
class AzureSpeechData:
    """Runtime data for azure_speech config entries.

    Stored as entry.runtime_data after successful setup.
    Provides typed access to the API client and coordinator instances.
    """

    client: AzureSpeechApiClient
    coordinator: AzureSpeechDataUpdateCoordinator
    integration: Integration
