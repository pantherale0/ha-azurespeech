"""Sensor platform for azure_speech."""

from custom_components.azure_speech.data import AzureSpeechConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .connection import AzureSpeechConnectionSensor
from .voices_count import AzureSpeechVoicesCountSensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AzureSpeechConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Azure Speech sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            AzureSpeechConnectionSensor(coordinator),
            AzureSpeechVoicesCountSensor(coordinator),
        ]
    )
