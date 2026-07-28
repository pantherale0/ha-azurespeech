"""Audio utility functions for Azure Speech integration."""

import struct


def wrap_pcm_in_wav(pcm_bytes: bytes, sample_rate: int = 16000, channels: int = 1, bit_depth: int = 16) -> bytes:
    """Wrap raw PCM audio bytes with a RIFF WAV header.

    :param pcm_bytes: Raw PCM audio data.
    :param sample_rate: Audio sampling rate in Hz (default 16000).
    :param channels: Number of audio channels (default 1 mono).
    :param bit_depth: Bits per sample (default 16-bit).
    :return: Full WAV byte string including 44-byte RIFF header.
    """
    byte_rate = sample_rate * channels * (bit_depth // 8)
    block_align = channels * (bit_depth // 8)
    data_size = len(pcm_bytes)
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        chunk_size,
        b"WAVE",
        b"fmt ",
        16,  # Subchunk1Size for PCM
        1,  # AudioFormat 1 = PCM
        channels,
        sample_rate,
        byte_rate,
        block_align,
        bit_depth,
        b"data",
        data_size,
    )
    return header + pcm_bytes
