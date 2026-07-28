"""Connection status diagnostic sensor for Azure Speech integration."""

from __future__ import annotations

from custom_components.azure_speech.coordinator import AzureSpeechDataUpdateCoordinator
from custom_components.azure_speech.entity import AzureSpeechEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory


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
