# Architectural and Design Decisions - Azure Speech

This document records significant architectural and design decisions made during the development of the Azure Speech integration.

---

## Decision Log

### 1. Pure Async `aiohttp` REST Client Over Native Azure Speech C-SDK

**Date:** 2026-07-28

**Context:** Azure Speech provides both an official Python SDK (`azure-cognitiveservices-speech`) and standard REST/WebSocket HTTP endpoints.

**Decision:** Implement a lightweight, pure-Python async API client (`AzureSpeechApiClient`) using Home Assistant's shared `aiohttp.ClientSession` rather than including the C-extension binary SDK.

**Rationale:**

- **Zero Binary Dependencies:** Native C-extensions can fail to compile or wheel-install on custom Linux architectures (e.g. ARM, Alpine, Docker containers).
- **Home Assistant Event Loop Safety:** `aiohttp` is natively non-blocking and integrates cleanly with Home Assistant's asyncio event loop.
- **Lower Footprint:** Eliminates heavy C++ shared libraries from the integration dependencies.

**Consequences:**

- REST short audio endpoint (WAV PCM 16kHz mono) is used for STT.
- Lightweight and instantly compatible across all Home Assistant OS / Supervised / Container environments.

---

### 2. W3C SSML Generation Engine for Text-To-Speech

**Date:** 2026-07-28

**Context:** Azure TTS REST API accepts raw text or structured SSML (Speech Synthesis Markup Language).

**Decision:** Implement a dedicated SSML generator (`entity_utils/ssml.py`) that wraps plain text or accepts pre-formatted SSML documents.

**Rationale:**

- Enables rich speech controls (voice overrides, pitch adjustment, speaking rate, styles).
- Automatically escapes special XML characters (`&`, `<`, `>`).
- Full backward compatibility with plain text strings.

---

### 3. Dynamic Neural Voice Discovery and Caching

**Date:** 2026-07-28

**Context:** Azure Speech offers over 500 neural voices across 100+ languages and locales.

**Decision:** Cache voices via `AzureSpeechDataUpdateCoordinator` and populate them dynamically in UI Options Flow dropdowns and diagnostic sensor attributes.

**Rationale:**

- Gives users full UI access to all regional neural voices without requiring manual string typing.
- Caches voice lists periodically (every 12 hours) to avoid hitting Azure API rate limits.
- Supports manual cache invalidation via the `azure_speech.refresh_voices` service action.

---

### 4. Separate TTS and STT Platforms

**Date:** 2026-07-28

**Context:** Home Assistant Voice Assistant (Assist) requires Speech-to-Text (`stt`) and Text-to-Speech (`tts`) entity platforms.

**Decision:** Implement both `tts` and `stt` entity platforms under `custom_components/azure_speech/`.

**Rationale:**

- Allows Azure Speech to serve as a complete engine for Home Assistant voice pipelines.
- Supports custom automations using standard HA `tts.speak` and media player targets.
