"""SSML builder utility for Azure Speech TTS."""

from typing import Any
from xml.sax import saxutils


def _escape_attr(value: str) -> str:
    """Escape XML attribute values for SSML."""
    return saxutils.escape(value, {"'": "&apos;", '"': "&quot;"})


def _normalize_optional_value(value: Any) -> str:
    """Normalize optional values to stripped strings."""
    if value is None:
        return ""
    return str(value).strip()


def _normalize_style_value(style: Any) -> str:
    """Normalize style value and map `default` to empty (no style tag)."""
    normalized_style = _normalize_optional_value(style)
    if normalized_style.casefold() == "default":
        return ""
    return normalized_style


def generate_ssml(
    text: str,
    voice: str,
    language: str = "en-US",
    style: str | None = None,
    style_degree: str | float | None = None,
    pitch: str = "default",
    rate: str = "default",
) -> str:
    """Generate valid SSML XML payload for Azure Speech TTS REST API.

    :param text: Text string or raw SSML to speak.
    :param voice: Voice short name (e.g. en-US-AvaMultilingualNeural).
    :param language: Language BCP-47 tag (e.g. en-US).
    :param style: Optional speaking style (e.g. assistant, friendly, angry). Use "default" for no style tag.
    :param style_degree: Optional style intensity from 0.01 to 2.
    :param pitch: Pitch string (e.g. default, +10%, -10%).
    :param rate: Rate string (e.g. default, 1.1, 0.9).
    :return: Formatted SSML XML string.
    """
    stripped = text.strip()
    if stripped.startswith("<speak") and stripped.endswith("</speak>"):
        return stripped

    escaped_text = saxutils.escape(text)
    escaped_voice = _escape_attr(voice)
    escaped_language = _escape_attr(language)
    escaped_pitch = _escape_attr(pitch)
    escaped_rate = _escape_attr(rate)

    style_value = _normalize_style_value(style)
    style_degree_value = _normalize_optional_value(style_degree)

    prosody_block = (
        f"    <prosody rate='{escaped_rate}' pitch='{escaped_pitch}'>\n"
        f"      {escaped_text}\n"
        "    </prosody>\n"
    )

    speech_block = prosody_block
    if style_value:
        express_as_attributes = f" style='{_escape_attr(style_value)}'"
        if style_degree_value:
            express_as_attributes += f" styledegree='{_escape_attr(style_degree_value)}'"
        speech_block = (
            f"    <mstts:express-as{express_as_attributes}>\n"
            f"{prosody_block}"
            "    </mstts:express-as>\n"
        )

    return (
        "<speak version='1.0' "
        f"xml:lang='{escaped_language}' "
        "xmlns='http://www.w3.org/2001/10/synthesis' "
        "xmlns:mstts='http://www.w3.org/2001/mstts'>\n"
        f"  <voice name='{escaped_voice}'>\n"
        f"{speech_block}"
        "  </voice>\n"
        "</speak>"
    )
