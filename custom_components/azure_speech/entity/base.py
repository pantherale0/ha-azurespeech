"""Base entity class for azure_speech.

This module provides the base entity class that all integration entities inherit from.
It handles common functionality like device info, unique IDs, and coordinator integration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.azure_speech.const import ATTRIBUTION, DOMAIN
from custom_components.azure_speech.coordinator import AzureSpeechDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class AzureSpeechEntity(CoordinatorEntity[AzureSpeechDataUpdateCoordinator]):
    """Base entity class for azure_speech.

    All entities in this integration inherit from this class, which provides:
    - Automatic coordinator updates
    - Device info management
    - Unique ID generation
    - Attribution and naming conventions
    """

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: AzureSpeechDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize the base entity.

        :param coordinator: The data update coordinator for this entity.
        :param entity_description: The entity description defining characteristics.
        """
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    coordinator.config_entry.entry_id,
                ),
            },
            name=coordinator.config_entry.title,
            manufacturer="Microsoft Azure",
            model="Azure Speech Services",
        )
