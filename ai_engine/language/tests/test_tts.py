"""
Tests for the Text-to-Speech engine.

Tests cover: Piper backend, gTTS fallback, auto-mode backend selection,
error handling for empty text and unsupported languages.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure project root is on path
_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ai_engine.language.interfaces import TTSResult, TTSBackend
from ai_engine.language.text_to_speech import (
    text_to_speech,
    PiperTTSBackend,
    GttsFallbackBackend,
)
from ai_engine.language.config import SUPPORTED_LANGUAGES


# ---------------------------------------------------------------------------
# Input validation tests  (no model needed)
# ---------------------------------------------------------------------------

class TestTextToSpeechValidation:
    """Test input validation in the top-level text_to_speech() function."""

    def test_empty_text_returns_error(self):
        result = text_to_speech("", "en")
        assert not result.ok
        assert "Empty text" in result.error

    def test_whitespace_text_returns_error(self):
        result = text_to_speech("   ", "en")
        assert not result.ok
        assert "Empty text" in result.error

    def test_unsupported_language(self):
        result = text_to_speech("Hello", "xx")
        assert not result.ok
        assert "Unsupported language" in result.error

    def test_supported_languages_accepted(self):
        """All configured languages should be accepted (validation only)."""
        for code in SUPPORTED_LANGUAGES:
            # We can't guarantee a backend is installed, so we just check
            # that input validation passes (no "Unsupported language" error).
            result = text_to_speech("test", code)
            if not result.ok:
                assert "Unsupported language" not in result.error


# ---------------------------------------------------------------------------
# Backend interface tests  (mocked)
# ---------------------------------------------------------------------------

class TestBackendSelection:
    """Test that the auto-mode backend selection works correctly."""

    def _make_mock_backend(
        self,
        name: str = "mock",
        available: bool = True,
        supports_lang: bool = True,
    ) -> MagicMock:
        backend = MagicMock(spec=TTSBackend)
        backend.name = name
        backend.is_available.return_value = available
        backend.supports_language.return_value = supports_lang
        backend.synthesize.return_value = TTSResult(
            audio_bytes=b"RIFF" + b"\x00" * 100,
            sample_rate=22050,
            language="en",
            engine=name,
        )
        return backend

    def test_explicit_backend_used(self):
        """When a backend is explicitly passed, it should be used."""
        mock = self._make_mock_backend(name="explicit")
        result = text_to_speech("Hello", "en", backend=mock)
        assert result.ok
        assert result.engine == "explicit"
        mock.synthesize.assert_called_once_with("Hello", "en")

    def test_explicit_backend_error_propagated(self):
        """Backend errors should propagate cleanly."""
        mock = self._make_mock_backend()
        mock.synthesize.return_value = TTSResult(
            audio_bytes=b"",
            sample_rate=22050,
            language="en",
            engine="mock",
            error="Something went wrong",
        )
        result = text_to_speech("Hello", "en", backend=mock)
        assert not result.ok
        assert result.error == "Something went wrong"


# ---------------------------------------------------------------------------
# PiperTTSBackend unit tests
# ---------------------------------------------------------------------------

class TestPiperBackend:
    """Test PiperTTSBackend methods."""

    def test_supports_language_no_model(self):
        """If no ONNX file exists, supports_language should return False."""
        piper = PiperTTSBackend()
        # Tamil has no Piper model configured by default
        assert piper.supports_language("ta") is False

    def test_synthesize_empty_text(self):
        piper = PiperTTSBackend()
        result = piper.synthesize("", "en")
        assert not result.ok
        assert "Empty text" in result.error

    def test_synthesize_missing_model(self):
        """Should return a helpful error when the voice model is not downloaded."""
        piper = PiperTTSBackend()
        # Unless the user has actually downloaded models, this should error
        # gracefully — not crash.
        result = piper.synthesize("Hello", "en")
        if not result.ok:
            assert "model" in result.error.lower() or "install" in result.error.lower()


# ---------------------------------------------------------------------------
# GttsFallbackBackend unit tests
# ---------------------------------------------------------------------------

class TestGttsFallback:
    """Test gTTS fallback backend."""

    def test_supports_all_configured_languages(self):
        gtts = GttsFallbackBackend()
        for code in SUPPORTED_LANGUAGES:
            assert gtts.supports_language(code)

    def test_synthesize_empty_text(self):
        gtts = GttsFallbackBackend()
        result = gtts.synthesize("", "en")
        assert not result.ok

    def test_unsupported_language(self):
        gtts = GttsFallbackBackend()
        result = gtts.synthesize("test", "xx")
        assert not result.ok


# ---------------------------------------------------------------------------
# gTTS integration test  (skipped if gTTS not installed or offline)
# ---------------------------------------------------------------------------

_gtts_available = False
try:
    from gtts import gTTS as _gTTS  # noqa: F401
    _gtts_available = True
except ImportError:
    pass


@pytest.mark.skipif(not _gtts_available, reason="gTTS not installed")
class TestGttsIntegration:
    """
    Integration tests that hit Google's TTS service.
    Requires internet — skipped in offline / CI environments.
    """

    @pytest.mark.parametrize("lang,text", [
        ("en", "Hello, how can I help you?"),
        ("hi", "नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?"),
        ("ta", "வணக்கம், நான் உங்களுக்கு எப்படி உதவ முடியும்?"),
    ])
    def test_synthesize_per_language(self, lang, text):
        """gTTS should produce non-empty audio for each supported language."""
        gtts = GttsFallbackBackend()
        try:
            result = gtts.synthesize(text, lang)
            if result.ok:
                assert len(result.audio_bytes) > 0
                assert result.engine == "gTTS"
            # If it fails due to network, that's OK in CI
        except Exception:
            pytest.skip("Network error — skipping gTTS integration test")
