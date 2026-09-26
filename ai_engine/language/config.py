"""
Central configuration for the STT / TTS language module.

**Adding a new language** is a config change, not a code change:
just add an entry to ``SUPPORTED_LANGUAGES`` below.
"""

from pathlib import Path
from typing import Dict, Any, Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_MODULE_DIR = Path(__file__).resolve().parent
MODELS_DIR = _MODULE_DIR / "models"
PIPER_MODELS_DIR = MODELS_DIR / "piper"
OUTPUT_DIR = _MODULE_DIR / "output"

# Ensure directories exist (lazy — created only when actually used)
for _d in (MODELS_DIR, PIPER_MODELS_DIR, OUTPUT_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Audio defaults
# ---------------------------------------------------------------------------

DEFAULT_SAMPLE_RATE: int = 16_000      # 16 kHz — standard for ASR
DEFAULT_MIC_DURATION: float = 5.0      # seconds
DEFAULT_CHANNELS: int = 1              # mono


# ---------------------------------------------------------------------------
# Whisper (STT) configuration
# ---------------------------------------------------------------------------

# Model sizes in ascending order of quality / size:
#   tiny (39 M) < base (74 M) < small (244 M) < medium (769 M) < large-v3 (1.5 G)
#
# Raspberry Pi / edge:  "small"  (good balance)
# Laptop / demo:        "large-v3"  (best multilingual accuracy)
WHISPER_MODEL_SIZE: str = "small"
WHISPER_DEVICE: str = "cpu"            # "cpu" or "cuda"
WHISPER_COMPUTE_TYPE: str = "int8"     # int8 quantisation for speed
WHISPER_BEAM_SIZE: int = 5


# ---------------------------------------------------------------------------
# Piper (TTS) configuration
# ---------------------------------------------------------------------------

# Each entry maps a language code to the Piper voice model filename
# (without extension).  The downloader script fetches the matching
# .onnx + .onnx.json pair from the Piper releases.
#
# Browse voices: https://rhasspy.github.io/piper-samples/
PIPER_VOICES: Dict[str, Dict[str, str]] = {
    "en": {
        "model_name": "en_US-lessac-medium",
        "description": "English (US) — Lessac, medium quality",
    },
    "hi": {
        "model_name": "hi_IN-swara-medium",
        "description": "Hindi — Swara, medium quality",
    },
    # Tamil — limited Piper availability; the engine will fall back to gTTS
    # when a Piper voice is not installed.  Uncomment below if / when a
    # Tamil model becomes available.
    # "ta": {
    #     "model_name": "ta_IN-xxx-medium",
    #     "description": "Tamil — TBD",
    # },
}


def get_piper_model_path(language: str) -> Optional[Path]:
    """Return the ONNX model path for *language*, or ``None``."""
    voice = PIPER_VOICES.get(language)
    if voice is None:
        return None
    onnx = PIPER_MODELS_DIR / f"{voice['model_name']}.onnx"
    return onnx if onnx.exists() else None


# ---------------------------------------------------------------------------
# Supported languages registry
# ---------------------------------------------------------------------------
# This is THE place to add or remove languages.  Every other component
# reads from this dict.

SUPPORTED_LANGUAGES: Dict[str, Dict[str, Any]] = {
    "en": {
        "name": "English",
        "native_name": "English",
        "whisper_code": "en",           # Whisper language code
        "bhashini_code": "en",          # Bhashini / ULCA code
        "piper_voice": PIPER_VOICES.get("en"),
        "gtts_tld": "com",           # gTTS top-level domain for accent
    },
    "hi": {
        "name": "Hindi",
        "native_name": "हिन्दी",
        "whisper_code": "hi",
        "bhashini_code": "hi",
        "piper_voice": PIPER_VOICES.get("hi"),
        "gtts_tld": "com",
    },
    "ta": {
        "name": "Tamil",
        "native_name": "தமிழ்",
        "whisper_code": "ta",
        "bhashini_code": "ta",
        "piper_voice": PIPER_VOICES.get("ta"),
        "gtts_tld": "com",
    },
    "te": {
        "name": "Telugu",
        "native_name": "తెలుగు",
        "whisper_code": "te",
        "bhashini_code": "te",
        "piper_voice": None,
        "gtts_tld": "com",
    },
    "kn": {
        "name": "Kannada",
        "native_name": "ಕನ್ನಡ",
        "whisper_code": "kn",
        "bhashini_code": "kn",
        "piper_voice": None,
        "gtts_tld": "com",
    },
    "ml": {
        "name": "Malayalam",
        "native_name": "മലയാളം",
        "whisper_code": "ml",
        "bhashini_code": "ml",
        "piper_voice": None,
        "gtts_tld": "com",
    },
    "mr": {
        "name": "Marathi",
        "native_name": "मराठी",
        "whisper_code": "mr",
        "bhashini_code": "mr",
        "piper_voice": None,
        "gtts_tld": "com",
    },
    "bn": {
        "name": "Bengali",
        "native_name": "বাংলা",
        "whisper_code": "bn",
        "bhashini_code": "bn",
        "piper_voice": None,
        "gtts_tld": "com",
    },
    "gu": {
        "name": "Gujarati",
        "native_name": "ગુજરાતી",
        "whisper_code": "gu",
        "bhashini_code": "gu",
        "piper_voice": None,
        "gtts_tld": "com",
    },
    "pa": {
        "name": "Punjabi",
        "native_name": "ਪੰਜਾਬੀ",
        "whisper_code": "pa",
        "bhashini_code": "pa",
        "piper_voice": None,
        "gtts_tld": "com",
    },
    "or": {
        "name": "Odia",
        "native_name": "ଓଡ଼ିଆ",
        "whisper_code": "or",
        "bhashini_code": "or",
        "piper_voice": None,
        "gtts_tld": "com",
    },
}


def is_language_supported(code: str) -> bool:
    """Check whether *code* (ISO-639-1) is in the supported set."""
    return code in SUPPORTED_LANGUAGES


def get_language_name(code: str) -> str:
    """Human-readable name for a language code, or the code itself."""
    entry = SUPPORTED_LANGUAGES.get(code)
    return entry["name"] if entry else code
