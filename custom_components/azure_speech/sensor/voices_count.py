"""Voices count diagnostic sensor for Azure Speech integration."""

from __future__ import annotations

from typing import Any

from custom_components.azure_speech.coordinator import AzureSpeechDataUpdateCoordinator
from custom_components.azure_speech.entity import AzureSpeechEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory


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
        voices_by_locale: dict[str, list[str]] = {}
        for v in voices:
            locale = str(v.get("Locale", "unknown"))
            name = v.get("ShortName")
            if name:
                voices_by_locale.setdefault(locale, []).append(name)

        return {
            "voices": [v.get("ShortName") for v in voices if v.get("ShortName")],
            "voices_by_locale": voices_by_locale,
        }
