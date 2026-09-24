# Multilingual STT / TTS Module

> **Team BRAVITS** · SIH 2026 · Problem Statement SIH26088  
> *Speech-to-Text & Text-to-Speech module for the Multilingual Cooperative AI Assistant*

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Your Code (Teammates)                    │
│                                                              │
│   result = speech_to_text("audio.wav")                       │
│   result = text_to_speech("नमस्ते", "hi", play_audio=True)   │
└──────────────┬───────────────────────────┬───────────────────┘
               │                           │
       ┌───────▼────────┐         ┌────────▼────────┐
       │  STTBackend     │         │  TTSBackend      │
       │  (ABC)          │         │  (ABC)           │
       └───────┬────────┘         └────────┬────────┘
               │                           │
   ┌───────────┼──────────┐    ┌───────────┼──────────┐
   │           │          │    │           │          │
   ▼           ▼          ▼    ▼           ▼          ▼
┌──────┐  ┌────────┐  ┌────┐ ┌──────┐ ┌──────┐ ┌────────┐
│Whisper│  │Bhashini│  │ …  │ │Piper │ │ gTTS │ │Bhashini│
│(local)│  │ (stub) │  │    │ │(local│ │(online│ │ (stub) │
└──────┘  └────────┘  └────┘ │ ONNX)│ │ fall- │ └────────┘
                              └──────┘ │ back) │
                                       └──────┘
```

## Setup

### 1. System Dependencies

**Windows:**
```bash
# No extra system deps needed — sounddevice bundles PortAudio
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install libportaudio2 espeak-ng ffmpeg
```

**macOS:**
```bash
brew install portaudio espeak ffmpeg
```

### 2. Python Dependencies

```bash
cd ai_engine/language
pip install -r requirements.txt
```

### 3. Download Models (one-time)

```bash
# Download both STT (Whisper) and TTS (Piper) models
python -m ai_engine.language.download_models

# Or separately:
python -m ai_engine.language.download_models --stt
python -m ai_engine.language.download_models --tts

# Use a bigger Whisper model for better accuracy (needs ~1.5 GB)
python -m ai_engine.language.download_models --whisper-size large-v3
```

## One-Command Demo

```bash
# Live mic demo (record 5s → transcribe → reply → speak)
python -m ai_engine.language.demo

# From a file
python -m ai_engine.language.demo --file path/to/audio.wav

# Longer recording
python -m ai_engine.language.demo --duration 10

# Skip audio playback (CI / headless)
python -m ai_engine.language.demo --file audio.wav --no-play
```

## Usage (for Teammates)

### Speech-to-Text

```python
from ai_engine.language import speech_to_text

# From a file
result = speech_to_text("recording.wav")
print(result.text)                # "PM Kisan scheme ke baare mein batao"
print(result.detected_language)   # "hi"
print(result.confidence)          # 0.97

# From live mic (records 5 seconds)
result = speech_to_text("mic")

# From raw audio bytes
result = speech_to_text(audio_bytes)

# Check for errors
if not result.ok:
    print(f"Error: {result.error}")
```

### Text-to-Speech

```python
from ai_engine.language import text_to_speech

# Synthesize and play through speakers
result = text_to_speech("नमस्ते!", "hi", play_audio=True)

# Just get audio bytes (no playback)
result = text_to_speech("Hello!", "en")
wav_data = result.audio_bytes

# Save to file
result = text_to_speech("வணக்கம்!", "ta", save_path="output.wav")

# Check for errors
if not result.ok:
    print(f"Error: {result.error}")
```

### Custom Backend (Bhashini)

```python
from ai_engine.language import speech_to_text, BhashiniSTTBackend

# Use Bhashini instead of Whisper (requires credentials in .env)
bhashini = BhashiniSTTBackend()
result = speech_to_text("audio.wav", backend=bhashini)
```

## Adding a New Language

Edit **`config.py`** — just add one entry to `SUPPORTED_LANGUAGES`:

```python
"te": {
    "name": "Telugu",
    "native_name": "తెలుగు",
    "whisper_code": "te",
    "bhashini_code": "te",
    "piper_voice": PIPER_VOICES.get("te"),
    "gtts_tld": "co.in",
},
```

If Piper has a voice model for it, also add to `PIPER_VOICES`:

```python
"te": {
    "model_name": "te_IN-somevoice-medium",
    "description": "Telugu — medium quality",
},
```

## Model Size Guide

| Model | Size | Speed (CPU) | Best For |
|:------|:-----|:------------|:---------|
| `tiny` | 39 MB | Very fast | Quick testing |
| `base` | 74 MB | Fast | Raspberry Pi |
| `small` | 244 MB | Moderate | **Default — good balance** |
| `medium` | 769 MB | Slow | Better accuracy |
| `large-v3` | 1.5 GB | Slowest | **Best accuracy (demo laptop)** |

Change the default in `config.py`:
```python
WHISPER_MODEL_SIZE = "large-v3"  # or "small" for Pi
```

## Running Tests

```bash
pytest ai_engine/language/tests/ -v
```

## File Structure

```
ai_engine/language/
├── __init__.py           # Package exports
├── interfaces.py         # ABC contracts + dataclasses
├── config.py             # Language registry, model paths, audio params
├── speech_to_text.py     # Whisper STT backend + convenience function
├── text_to_speech.py     # Piper TTS + gTTS fallback
├── bhashini_adapter.py   # Bhashini ULCA API stub
├── audio_utils.py        # Mic recording, file loading, playback
├── demo.py               # End-to-end demo script
├── download_models.py    # Model downloader
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── models/               # Downloaded model files (gitignored)
│   └── piper/            # Piper ONNX voice models
├── language_detector.py  # (Existing) Unicode script-based text detector
├── translation.py        # (Existing) Translation engine (teammate scope)
└── tests/
    ├── test_stt.py       # STT test cases
    ├── test_tts.py       # TTS test cases
    └── test_interfaces.py # Interface + adapter tests
```
