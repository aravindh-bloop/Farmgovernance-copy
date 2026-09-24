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

    def transcribe(self, audio: AudioInput) -> STTResult:
        if not self.is_available():
            return STTResult("", "unknown", 0.0, self.name, "SARVAM_API_KEY is not configured", True)

        content = _audio_bytes(audio)
        if not content:
            return STTResult("", "unknown", 0.0, self.name, "No audio bytes were supplied", True)

        try:
            response = httpx.post(
                f"{_BASE_URL}/speech-to-text",
                headers={"api-subscription-key": _api_key()},
                files={"file": ("recording.wav", content, "audio/wav")},
                data={"model": "saarika:v2.5", "language_code": "unknown"},
                timeout=30.0,
            )
            response.raise_for_status()
            payload = response.json()
            text = (payload.get("transcript") or payload.get("text") or "").strip()
            detected = payload.get("language_code") or "unknown"
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

        try:
            response = httpx.post(
                f"{_BASE_URL}/text-to-speech",
                headers={"api-subscription-key": _api_key(), "Content-Type": "application/json"},
                json={
                    "inputs": [text.strip()[:500]],
                    "target_language_code": language,
                    "speaker": "meera",
                    "model": "bulbul:v2",
                    "output_audio_codec": "mp3",
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