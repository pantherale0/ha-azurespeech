# Architecture Overview - Azure Speech Custom Integration

This document describes the technical architecture of the Azure Speech custom component (`azure_speech`) for Home Assistant.

## Directory Structure

```text
custom_components/azure_speech/
├── __init__.py              # Integration setup, unload, and CONFIG_SCHEMA
├── api/                     # External Azure Speech API communication
│   ├── __init__.py          # API exports
│   ├── client.py            # AzureSpeechApiClient (aiohttp REST/WebSocket implementation)
│   └── exceptions.py        # Custom API exception hierarchy
├── brand/                   # Integration brand logo and icon images
│   ├── dark_icon.png
│   ├── dark_logo.png
│   ├── icon.png
│   └── logo.png
├── config_flow.py           # Config flow entry point (for hassfest)
├── config_flow_handler/     # Config flow implementation
│   ├── __init__.py          # Package exports
│   ├── config_flow.py       # AzureSpeechConfigFlow & AzureSpeechOptionsFlowHandler
│   ├── schemas/             # Voluptuous form schemas
│   │   ├── __init__.py
│   │   ├── options.py       # Options flow schema with dynamic voice dropdown
│   │   └── user.py          # User step setup schema
│   └── validators/          # Input validation
│       ├── __init__.py
│       └── auth.py          # Azure API key and region validator
├── const.py                 # Constants, Azure regions list, output format mappings
├── coordinator/             # Data update coordinator package
│   └── __init__.py          # AzureSpeechDataUpdateCoordinator (voice cache & health check)
├── data.py                  # Data classes and runtime types (AzureSpeechData & AzureSpeechConfigEntry)
├── diagnostics.py           # Redacted diagnostic data (async_redact_data)
├── entity/                  # Base entity package
│   ├── __init__.py          # Exports AzureSpeechEntity
│   └── base.py              # Base AzureSpeechEntity implementation with DeviceInfo
├── entity_utils/            # Helper utilities
│   ├── __init__.py
│   ├── audio.py             # Audio conversion & WAV header generator
│   └── ssml.py              # W3C SSML XML generator
├── icons.json               # Icon definitions for custom service actions
├── manifest.json            # Integration metadata
├── sensor/                  # Diagnostic sensor platform
│   ├── __init__.py          # Platform setup
│   ├── connection.py        # AzureSpeechConnectionSensor
│   └── voices_count.py      # AzureSpeechVoicesCountSensor
├── service_actions/         # Service action implementations
│   ├── __init__.py          # Service action registration
│   └── refresh_voices.py    # azure_speech.refresh_voices action handler
├── services.yaml            # Service action metadata definitions
├── stt/                     # Speech-To-Text platform
│   ├── __init__.py          # Platform setup
│   └── engine.py            # AzureSpeechSTTEntity (HA Assist stream consumer)
├── translations/            # Localization files
│   └── en.json              # English translations
└── tts/                     # Text-To-Speech platform
    ├── __init__.py          # Platform setup
    └── engine.py            # AzureSpeechTTSEntity (SSML synthesis engine)
```

---

## Core Components

### Data Update Coordinator (`coordinator/`)

The coordinator manages periodic voice list caching and API health checks:

- **Class:** `AzureSpeechDataUpdateCoordinator`
- **Update Interval:** 12 hours (with manual refresh support via `azure_speech.refresh_voices`).
- **Functionality:** Fetches `GET /cognitiveservices/voices/list`, verifies API key validity, and populates voice lists for options flow dropdowns and diagnostic sensors.

### API Client (`api/`)

Handles all asynchronous HTTP communication with Microsoft Azure Speech REST APIs:

- **Class:** `AzureSpeechApiClient`
- **Transport:** Async HTTP via `aiohttp.ClientSession` (no native C binary dependencies, non-blocking on HA event loop).
- **Key Methods:**
  - `get_voices()`: Fetches list of available neural voices.
  - `generate_tts_audio()`: Requests TTS audio synthesis using SSML payloads.
  - `transcribe_stt_audio()`: Sends WAV 16kHz mono audio streams to Azure STT REST endpoint.

### Config Flow & Options Flow (`config_flow_handler/`)

- **Class:** `AzureSpeechConfigFlow` & `AzureSpeechOptionsFlowHandler`
- **Supported Flows:**
  - **User Setup:** Collects and validates `api_key`, `region`, and optional custom `endpoint`.
  - **Reauth Flow:** Triggered on API credential expiry (401/403).
  - **Reconfigure Flow:** Allows updating API key or region for an existing entry.
  - **Options Flow:** Configures default voice, language, pitch, rate, audio output format (`mp3`/`wav`/`ogg`), and profanity filtering (`masked`/`removed`/`raw`).

### Base Entity (`entity/`)

- **Class:** `AzureSpeechEntity` (in `entity/base.py`)
- **Functionality:** Provides unified `DeviceInfo` (`Microsoft Azure / Azure Speech Services`), unique ID formatting, and coordinator update listeners.

---

## Data Flow Architecture

```text
┌─────────────────────────┐
│   User / Assist Engine  │
└───────────┬─────────────┘
            │
            ├─────────────────────────────────────────┐
            ▼                                         ▼
┌─────────────────────────┐               ┌─────────────────────────┐
│  AzureSpeechTTSEntity   │               │  AzureSpeechSTTEntity   │
└───────────┬─────────────┘               └───────────┬─────────────┘
            │                                         │
            │ Generate SSML                           │ Wrap PCM in WAV
            ▼                                         ▼
┌───────────────────────────────────────────────────────────────────┐
│                      AzureSpeechApiClient                         │
└───────────────────────────┬───────────────────────────────────────┘
                            │
                            │ aiohttp REST Requests
                            ▼
┌───────────────────────────────────────────────────────────────────┐
│               Microsoft Azure Speech REST Services                │
└───────────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

See [DECISIONS.md](./DECISIONS.md) for detailed design rationale regarding pure async `aiohttp` transport, SSML formatting, and audio processing.
