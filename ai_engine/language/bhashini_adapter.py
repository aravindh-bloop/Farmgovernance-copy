"""
Bhashini (Government of India) Neural MT + speech adapter.

Two parts:
1. ``bhashini_translate`` — **working** NMT client for the Bhashini
   ``sarvam_translate`` pipeline (https://api.bhashini.gov.in). Used as the
   primary translation provider for the multilingual answers.
2. ``BhashiniSTTBackend`` / ``BhashiniTTSBackend`` — interface-compatible
   backends preserved for future ASR/TTS wiring. The active speech chain uses
   Sarvam (STT/TTS) and Whisper/gTTS fallbacks, so these never run unless
   explicitly selected.

Credentials (from https://bhashini.gov.in):
  - BHASHINI_USER_ID            (pipeline / user key)
  - BHASHINI_INFERENCE_API_KEY  (inference API key)
"""

import re

import httpx

from config.settings import settings
from .config import DEFAULT_SAMPLE_RATE, SUPPORTED_LANGUAGES
from .interfaces import STTBackend, STTResult, TTSBackend, TTSResult

_BHASHINI_MT_URL = "https://api.bhashini.gov.in/v1/sarvam_translate"


def _user_id() -> str:
    return settings.BHASHINI_USER_ID or settings.BHASHINI_PIPELINE_ID or ""


def _inference_api_key() -> str:
    return settings.BHASHINI_INFERENCE_API_KEY or settings.BHASHINI_API_KEY or ""


def is_configured() -> bool:
    return bool(_user_id() and _inference_api_key())


def _split_sentences(text: str, max_len: int = 450) -> list:
    """Split long content into sentence-grouped chunks that fit the API."""
    rough = [s.strip() for s in re.split(r"(?<=[.!?।।?|])\s+", text) if s.strip()]
    chunks: list = []
    current = ""
    for s in rough:
        if len(current) + len(s) > max_len and current:
            chunks.append(current)
            current = s
        else:
            current = f"{current} {s}".strip()
    if current:
        chunks.append(current)
    return chunks or ([text[:max_len]] if text else [])


def bhashini_translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate ``text`` from ``source_lang`` to ``target_lang`` using the
    Bhashini NMT pipeline. Returns the translated text, or ``""`` on failure.
    """
    if not text or not is_configured() or source_lang == target_lang:
        return ""

    chunks = _split_sentences(text)
    translated_parts: list = []

    for chunk in chunks:
        try:
            response = httpx.post(
                _BHASHINI_MT_URL,
                headers={
                    "Authorization": f"Bearer {_inference_api_key()}",
                    "User-ID": _user_id(),
                    "Content-Type": "application/json",
                },
                json={
                    "sourceLanguage": source_lang,
                    "targetLanguage": target_lang,
                    "sentences": [chunk],
                },
                timeout=45.0,
            )
            response.raise_for_status()
            payload = response.json()
            pipeline_response = payload.get("pipelineResponse") or []
            targets = [p.get("target", "") for p in pipeline_response if p.get("target")]
            if not targets:
                return ""
            translated_parts.append(" ".join(targets))
        except Exception as exc:
            print(f"Bhashini translation failed for '{chunk[:40]}...': {exc}")
            return ""

    return "\n".join(translated_parts).strip()


class BhashiniSTTBackend(STTBackend):
    """
    Bhashini ASR backend. Kept for interface compatibility — select it
    explicitly only after wiring a Bhashini ASR pipeline serviceId.
    """

    @property
    def name(self) -> str:
        return "bhashini-asr"

    def is_available(self) -> bool:
        return is_configured()

    def transcribe(self, audio, language=None) -> STTResult:
        return STTResult(
            text="",
            detected_language=language or "unknown",
            confidence=0.0,
            engine=self.name,
            error="Bhashini ASR pipeline not wired (use Sarvam or Whisper STT).",
            is_empty=True,
        )


class BhashiniTTSBackend(TTSBackend):
    """
    Bhashini TTS backend. Kept for interface compatibility — select it
    explicitly only after wiring a Bhashini TTS pipeline serviceId.
    """

    @property
    def name(self) -> str:
        return "bhashini-tts"

    def is_available(self) -> bool:
        return is_configured()

    def supports_language(self, language: str) -> bool:
        return language in SUPPORTED_LANGUAGES

    def synthesize(self, text: str, language: str) -> TTSResult:
        return TTSResult(
            audio_bytes=b"",
            sample_rate=DEFAULT_SAMPLE_RATE,
            language=language,
            engine=self.name,
            error="Bhashini TTS pipeline not wired (use Sarvam or gTTS TTS).",
        )