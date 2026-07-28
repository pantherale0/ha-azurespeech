"""Sensor platform for azure_speech."""

from __future__ import annotations

from typing import Any

from custom_components.azure_speech.coordinator import AzureSpeechDataUpdateCoordinator
from custom_components.azure_speech.data import AzureSpeechConfigEntry
from custom_components.azure_speech.entity import AzureSpeechEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


class AzureSpeechConnectionSensor(SensorEntity, AzureSpeechEntity):
    """Sensor tracking Azure Speech API connection status."""

    def __init__(
        self,
        coordinator: AzureSpeechDataUpdateCoordinator,
    ) -> None:
        """Initialize connection status sensor."""
        description = SensorEntityDescription(
            key="connection_status",
            name="API Connection Status",
            entity_category=EntityCategory.DIAGNOSTIC,
            icon="mdi:cloud-check",
        )
        super().__init__(coordinator, description)

    @property
    def native_value(self) -> str:
        """Return the current connection status."""
        return str(self.coordinator.data.get("status", "unknown"))


class AzureSpeechVoicesCountSensor(SensorEntity, AzureSpeechEntity):
    """Sensor tracking cached voice count from Azure Speech API."""

    def __init__(
        self,
        coordinator: AzureSpeechDataUpdateCoordinator,
    ) -> None:
        """Initialize voices count sensor."""
        description = SensorEntityDescription(
            key="voices_count",
            name="Cached Voices Count",
            entity_category=EntityCategory.DIAGNOSTIC,
            icon="mdi:account-voice",
        )
        super().__init__(coordinator, description)

    @property
    def native_value(self) -> int:
        """Return the total cached voice count."""
        return int(self.coordinator.data.get("voices_count", 0))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return detailed voice list attributes and voices grouped by locale."""
        voices = self.coordinator.voices
        voices_by_locale_count: dict[str, int] = {}
        for v in voices:
            locale = str(v.get("Locale", "unknown"))
            voices_by_locale_count[locale] = voices_by_locale_count.get(locale, 0) + 1

        return {
            "locales_count": len(voices_by_locale_count),
            "voices_per_locale": voices_by_locale_count,
        }


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
