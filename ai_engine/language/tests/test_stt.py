"""
Tests for the Speech-to-Text engine.

These tests are self-contained — they generate synthetic test audio via TTS
(or raw sine waves) so no external audio samples are needed.
"""

import io
import math
import struct
import sys
import wave
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import numpy as np

# Ensure project root is on path
_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ai_engine.language.interfaces import AudioInput, STTResult, AudioSource
from ai_engine.language.speech_to_text import speech_to_text, WhisperSTTBackend


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_wav_bytes(
    duration_sec: float = 1.0,
    sample_rate: int = 16000,
    freq_hz: float = 440.0,
) -> bytes:
    """Generate a sine-wave WAV file as bytes (for testing audio loading)."""
    n_samples = int(duration_sec * sample_rate)
    samples = [
        int(32767 * math.sin(2 * math.pi * freq_hz * t / sample_rate))
        for t in range(n_samples)
    ]
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f"<{n_samples}h", *samples))
    return buf.getvalue()


def _make_wav_file(tmp_path: Path, name: str = "test.wav", **kwargs) -> Path:
    """Write a WAV file to tmp_path and return its path."""
    p = tmp_path / name
    p.write_bytes(_make_wav_bytes(**kwargs))
    return p


# ---------------------------------------------------------------------------
# AudioInput construction tests  (no model needed)
# ---------------------------------------------------------------------------

class TestAudioInput:
    """Test the AudioInput factory methods."""

    def test_from_file_valid(self, tmp_path):
        p = _make_wav_file(tmp_path)
        ai = AudioInput.from_file(p)
        assert ai.source == AudioSource.FILE
        assert ai.file_path == p

    def test_from_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            AudioInput.from_file("/nonexistent/audio.wav")

    def test_from_file_bad_format(self, tmp_path):
        p = tmp_path / "test.xyz"
        p.write_text("not audio")
        with pytest.raises(ValueError, match="Unsupported audio format"):
            AudioInput.from_file(p)

    def test_from_bytes_valid(self):
        data = _make_wav_bytes()
        ai = AudioInput.from_bytes(data)
        assert ai.source == AudioSource.RAW_BYTES
        assert ai.audio_bytes == data

    def test_from_bytes_empty(self):
        with pytest.raises(ValueError, match="empty"):
            AudioInput.from_bytes(b"")

    def test_from_mic(self):
        ai = AudioInput.from_mic(duration_sec=3.0)
        assert ai.source == AudioSource.MICROPHONE
        assert ai.duration_sec == 3.0

    def test_from_mic_zero_duration(self):
        with pytest.raises(ValueError, match="positive"):
            AudioInput.from_mic(duration_sec=0)


# ---------------------------------------------------------------------------
# speech_to_text convenience function tests  (model mocked)
# ---------------------------------------------------------------------------

class TestSpeechToTextConvenience:
    """Test the top-level speech_to_text() function's input normalisation."""

    def _mock_backend(self) -> MagicMock:
        """Create a mock STT backend that returns a success result."""
        backend = MagicMock(spec=WhisperSTTBackend)
        backend.name = "mock-whisper"
        backend.is_available.return_value = True
        backend.transcribe.return_value = STTResult(
            text="hello world",
            detected_language="en",
            confidence=0.95,
            engine="mock-whisper",
        )
        return backend

    def test_file_path_string(self, tmp_path):
        p = _make_wav_file(tmp_path)
        backend = self._mock_backend()
        result = speech_to_text(str(p), backend=backend)
        assert result.ok
        assert result.text == "hello world"
        backend.transcribe.assert_called_once()

    def test_file_path_object(self, tmp_path):
        p = _make_wav_file(tmp_path)
        backend = self._mock_backend()
        result = speech_to_text(p, backend=backend)
        assert result.ok

    def test_bytes_input(self):
        data = _make_wav_bytes()
        backend = self._mock_backend()
        result = speech_to_text(data, backend=backend)
        assert result.ok

    def test_mic_string(self):
        backend = self._mock_backend()
        result = speech_to_text("mic", backend=backend)
        assert result.ok

    def test_unsupported_input_type(self):
        result = speech_to_text(12345)
        assert not result.ok
        assert "Unsupported" in result.error

    def test_backend_not_available(self, tmp_path):
        p = _make_wav_file(tmp_path)
        backend = self._mock_backend()
        backend.is_available.return_value = False
        result = speech_to_text(str(p), backend=backend)
        assert not result.ok
        assert "not installed" in result.error


# ---------------------------------------------------------------------------
# Whisper backend integration tests  (skipped if model not installed)
# ---------------------------------------------------------------------------

_whisper_available = False
try:
    import faster_whisper  # noqa: F401
    _whisper_available = True
except ImportError:
    pass


@pytest.mark.skipif(
    not _whisper_available,
    reason="faster-whisper not installed — skipping integration tests",
)
class TestWhisperIntegration:
    """
    Integration tests that run the actual Whisper model.

    These use short synthetic sine-wave audio.  Whisper will likely return
    empty text for a sine wave (no speech), which is the expected behaviour —
    we're testing that the pipeline doesn't crash.
    """

    def test_transcribe_wav_file_no_crash(self, tmp_path):
        p = _make_wav_file(tmp_path, duration_sec=1.0)
        result = speech_to_text(str(p))
        # Result may be empty (sine wave is not speech) but should not error
        assert isinstance(result, STTResult)

    def test_transcribe_raw_bytes_no_crash(self):
        data = _make_wav_bytes(duration_sec=1.0)
        result = speech_to_text(data)
        assert isinstance(result, STTResult)

    def test_transcribe_empty_silence(self, tmp_path):
        """A very short silence should return empty text gracefully."""
        # Generate near-silence (very low amplitude)
        sr = 16000
        n = sr  # 1 second
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(b"\x00\x00" * n)
        p = tmp_path / "silence.wav"
        p.write_bytes(buf.getvalue())

        result = speech_to_text(str(p))
        assert isinstance(result, STTResult)
        # Empty/silence is OK — just shouldn't crash
