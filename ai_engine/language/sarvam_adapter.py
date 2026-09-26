"""Sarvam AI speech adapters used when Bhashini credentials are unavailable."""

import base64
import os
from pathlib import Path
from typing import Optional

import httpx

from config.settings import settings
from .config import DEFAULT_SAMPLE_RATE, SUPPORTED_LANGUAGES
from .interfaces import AudioInput, STTBackend, STTResult, TTSBackend, TTSResult

_BASE_URL = "https://api.sarvam.ai"

# Sarvam expects BCP-47 style regional codes (e.g. "ta-IN") — bare ISO codes
# (e.g. "ta") are silently rejected by both the ASR and TTS endpoints.
SARVAM_LANG_CODES = {
    "en": "en-IN",
    "hi": "hi-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "mr": "mr-IN",
    "bn": "bn-IN",
    "gu": "gu-IN",
    "pa": "pa-IN",
    "or": "od-IN",
}


def to_sarvam_code(language: str) -> str:
    """Map a bare ISO-639-1 code to Sarvam's regional code (e.g. ta -> ta-IN)."""
    return SARVAM_LANG_CODES.get(language, language)


def _api_key() -> str:
    return settings.SARVAM_API_KEY or os.getenv("SARVAM_API_KEY", "")


def _audio_bytes(audio: AudioInput) -> Optional[bytes]:
    if audio.audio_bytes:
        return audio.audio_bytes
    if audio.file_path and Path(audio.file_path).exists():
        return Path(audio.file_path).read_bytes()
    return None


class SarvamSTTBackend(STTBackend):
    """Transcribe kiosk recordings through Sarvam's speech-to-text API."""

    @property
    def name(self) -> str:
        return "sarvam-saarika"

    def is_available(self) -> bool:
        return bool(_api_key())

    def transcribe(self, audio: AudioInput, language: str = "en") -> STTResult:
        if not self.is_available():
            return STTResult("", "unknown", 0.0, self.name, "SARVAM_API_KEY is not configured", True)

        content = _audio_bytes(audio)
        if not content:
            return STTResult("", "unknown", 0.0, self.name, "No audio bytes were supplied", True)

        lang_code = to_sarvam_code(language) if language and language != "unknown" else "unknown"
        try:
            response = httpx.post(
                f"{_BASE_URL}/speech-to-text",
                headers={"api-subscription-key": _api_key()},
                files={"file": ("recording.wav", content, "audio/wav")},
                data={"model": "saarika:v2.5", "language_code": lang_code},
                timeout=30.0,
            )
            response.raise_for_status()
            payload = response.json()
            text = (payload.get("transcript") or payload.get("text") or "").strip()
            detected = payload.get("language_code") or language or "unknown"
            if detected and len(detected) > 2 and "-" in detected:
                detected = detected.split("-")[0].lower()
            return STTResult(text, detected, 1.0 if text else 0.0, self.name, None if text else "No speech detected", not bool(text))
        except Exception as exc:
            return STTResult("", "unknown", 0.0, self.name, f"Sarvam STT failed: {exc}", True)


class SarvamTTSBackend(TTSBackend):
    """Generate multilingual kiosk speech through Sarvam Bulbul."""

    @property
    def name(self) -> str:
        return "sarvam-bulbul"

    def is_available(self) -> bool:
        return bool(_api_key())

    def supports_language(self, language: str) -> bool:
        return language in SUPPORTED_LANGUAGES

    def synthesize(self, text: str, language: str) -> TTSResult:
        if not self.is_available():
            return TTSResult(b"", DEFAULT_SAMPLE_RATE, language, self.name, error="SARVAM_API_KEY is not configured")
        if not text or not text.strip():
            return TTSResult(b"", DEFAULT_SAMPLE_RATE, language, self.name, error="Empty text")

        target_code = to_sarvam_code(language)
        try:
            response = httpx.post(
                f"{_BASE_URL}/text-to-speech",
                headers={"api-subscription-key": _api_key(), "Content-Type": "application/json"},
                json={
                    "inputs": [text.strip()[:500]],
                    "target_language_code": target_code,
                    "speaker": "priya",
                    "model": "bulbul:v3",
                    "audio_format": "mp3",
                },
                timeout=30.0,
            )
            response.raise_for_status()
            payload = response.json()
            audios = payload.get("audios") or []
            audio_bytes = base64.b64decode(audios[0]) if audios else b""
            if not audio_bytes:
                return TTSResult(b"", DEFAULT_SAMPLE_RATE, language, self.name, error="Sarvam returned no audio")
            return TTSResult(audio_bytes, 22050, language, self.name)
        except Exception as exc:
            return TTSResult(b"", DEFAULT_SAMPLE_RATE, language, self.name, error=f"Sarvam TTS failed: {exc}")


def sarvam_translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    Neural translation through Sarvam's Mayura translation API.
    Returns the translated string, or '' on failure.
    """
    if not text or not _api_key():
        return ""
    try:
        response = httpx.post(
            f"{_BASE_URL}/translate",
            headers={"api-subscription-key": _api_key(), "Content-Type": "application/json"},
            json={
                "input": text,
                "source_language_code": to_sarvam_code(source_lang),
                "target_language_code": to_sarvam_code(target_lang),
                "mode": "formal",
                "model": "mayura:v1",
                "enable_preprocessing": True,
                "numerals_format": "international",
            },
            timeout=45.0,
        )
        response.raise_for_status()
        return (response.json().get("translated_text") or "").strip()
    except Exception:
        return ""