"""
ai_engine.language — Multilingual Speech-to-Text & Text-to-Speech module.

Quick start::

    from ai_engine.language import speech_to_text, text_to_speech

    # Transcribe an audio file
    stt_result = speech_to_text("recording.wav")
    print(stt_result.text, stt_result.detected_language)

    # Synthesize speech and play it
    tts_result = text_to_speech("नमस्ते!", "hi", play_audio=True)
"""

from .speech_to_text import speech_to_text, WhisperSTTBackend
from .text_to_speech import text_to_speech, PiperTTSBackend, GttsFallbackBackend
from .bhashini_adapter import BhashiniSTTBackend, BhashiniTTSBackend
from .sarvam_adapter import SarvamSTTBackend, SarvamTTSBackend
from .interfaces import AudioInput, STTResult, TTSResult, STTBackend, TTSBackend
from .config import SUPPORTED_LANGUAGES, is_language_supported

__all__ = [
    # Main convenience functions
    "speech_to_text",
    "text_to_speech",
    # Backends
    "WhisperSTTBackend",
    "PiperTTSBackend",
    "GttsFallbackBackend",
    "BhashiniSTTBackend",
    "BhashiniTTSBackend",
    "SarvamSTTBackend",
    "SarvamTTSBackend",
    # Data classes & ABCs
    "AudioInput",
    "STTResult",
    "TTSResult",
    "STTBackend",
    "TTSBackend",
    # Config helpers
    "SUPPORTED_LANGUAGES",
    "is_language_supported",
]
