"""Entity utilities package for Azure Speech."""

from .audio import wrap_pcm_in_wav
from .ssml import generate_ssml

__all__ = ["generate_ssml", "wrap_pcm_in_wav"]
