"""Speech-to-Text platform for azure_speech."""

from .engine import AzureSpeechSTTEntity, async_setup_entry

__all__ = ["AzureSpeechSTTEntity", "async_setup_entry"]
