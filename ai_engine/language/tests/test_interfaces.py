"""
Tests for the abstract interfaces, dataclasses, and backend switching.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Ensure project root is on path
_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ai_engine.language.interfaces import (
    AudioInput,
    AudioSource,
    STTBackend,
    STTResult,
    TTSBackend,
    TTSResult,
)
from ai_engine.language.bhashini_adapter import BhashiniSTTBackend, BhashiniTTSBackend
from ai_engine.language.config import SUPPORTED_LANGUAGES, is_language_supported


# ---------------------------------------------------------------------------
# STTResult / TTSResult
# ---------------------------------------------------------------------------

class TestSTTResult:
    def test_ok_when_no_error(self):
        r = STTResult(text="hello", detected_language="en", confidence=0.9, engine="test")
        assert r.ok is True

    def test_not_ok_when_error(self):
        r = STTResult(text="", detected_language="en", confidence=0.0, engine="test", error="fail")
        assert r.ok is False

    def test_not_ok_when_empty(self):
        r = STTResult(text="", detected_language="en", confidence=0.0, engine="test", is_empty=True)
        assert r.ok is False


class TestTTSResult:
    def test_ok_with_audio_bytes(self):
        r = TTSResult(audio_bytes=b"\x00\x01", sample_rate=22050, language="en", engine="test")
        assert r.ok is True

    def test_not_ok_when_error(self):
        r = TTSResult(audio_bytes=b"", sample_rate=22050, language="en", engine="test", error="fail")
        assert r.ok is False

    def test_not_ok_when_empty_bytes(self):
        r = TTSResult(audio_bytes=b"", sample_rate=22050, language="en", engine="test")
        assert r.ok is False


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

class TestConfig:
    def test_supported_languages_include_en_hi_ta(self):
        assert is_language_supported("en")
        assert is_language_supported("hi")
        assert is_language_supported("ta")

    def test_unsupported_language(self):
        assert not is_language_supported("xx")
        assert not is_language_supported("")

    def test_language_entries_have_required_keys(self):
        for code, entry in SUPPORTED_LANGUAGES.items():
            assert "name" in entry, f"Language '{code}' missing 'name'"
            assert "whisper_code" in entry, f"Language '{code}' missing 'whisper_code'"
            assert "bhashini_code" in entry, f"Language '{code}' missing 'bhashini_code'"


# ---------------------------------------------------------------------------
# Backend switching
# ---------------------------------------------------------------------------

class TestBackendSwitching:
    """Ensure that custom backends are respected when passed explicitly."""

    def test_custom_stt_backend_called(self):
        from ai_engine.language.speech_to_text import speech_to_text

        mock_backend = MagicMock(spec=STTBackend)
        mock_backend.name = "custom-stt"
        mock_backend.is_available.return_value = True
        mock_backend.transcribe.return_value = STTResult(
            text="custom result",
            detected_language="hi",
            confidence=0.99,
            engine="custom-stt",
        )

        # Use from_bytes to avoid file-not-found
        import io, wave, struct
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(struct.pack("<100h", *([0] * 100)))
        wav_bytes = buf.getvalue()

        result = speech_to_text(wav_bytes, backend=mock_backend)
        assert result.text == "custom result"
        assert result.engine == "custom-stt"
        mock_backend.transcribe.assert_called_once()

    def test_custom_tts_backend_called(self):
        from ai_engine.language.text_to_speech import text_to_speech

        mock_backend = MagicMock(spec=TTSBackend)
        mock_backend.name = "custom-tts"
        mock_backend.is_available.return_value = True
        mock_backend.supports_language.return_value = True
        mock_backend.synthesize.return_value = TTSResult(
            audio_bytes=b"fake-audio",
            sample_rate=22050,
            language="ta",
            engine="custom-tts",
        )

        result = text_to_speech("வணக்கம்", "ta", backend=mock_backend)
        assert result.engine == "custom-tts"
        mock_backend.synthesize.assert_called_once_with("வணக்கம்", "ta")


# ---------------------------------------------------------------------------
# Bhashini adapter stubs
# ---------------------------------------------------------------------------

class TestBhashiniAdapter:
    """Test that the Bhashini stubs behave correctly without real credentials."""

    def test_stt_without_creds_returns_error(self, monkeypatch):
        monkeypatch.delenv("BHASHINI_API_KEY", raising=False)
        monkeypatch.delenv("BHASHINI_USER_ID", raising=False)

        backend = BhashiniSTTBackend()
        assert backend.is_available() is False

        audio = AudioInput.from_bytes(b"\x00" * 100)
        result = backend.transcribe(audio)
        assert not result.ok
        assert "credentials" in result.error.lower() or "configured" in result.error.lower()

    def test_tts_without_creds_returns_error(self, monkeypatch):
        monkeypatch.delenv("BHASHINI_API_KEY", raising=False)
        monkeypatch.delenv("BHASHINI_USER_ID", raising=False)

        backend = BhashiniTTSBackend()
        assert backend.is_available() is False

        result = backend.synthesize("Hello", "en")
        assert not result.ok
        assert "credentials" in result.error.lower() or "configured" in result.error.lower()

    def test_tts_supports_configured_languages(self):
        backend = BhashiniTTSBackend()
        for code in SUPPORTED_LANGUAGES:
            assert backend.supports_language(code)
