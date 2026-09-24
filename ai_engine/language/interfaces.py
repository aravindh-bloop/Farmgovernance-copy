"""
Abstract interfaces and data structures for Speech-to-Text and Text-to-Speech.

All STT/TTS backends (Whisper, Piper, Bhashini, etc.) implement these ABCs
so the rest of the pipeline can swap engines without code changes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AudioSource(Enum):
    """How audio was provided to the STT engine."""
    FILE = "file"
    MICROPHONE = "microphone"
    RAW_BYTES = "raw_bytes"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class AudioInput:
    """
    Unified representation of audio input.

    Create from a file path, raw bytes, or the ``"mic"`` sentinel to
    trigger live microphone recording.

    Examples
    --------
    >>> AudioInput.from_file("sample.wav")
    >>> AudioInput.from_bytes(raw_pcm)
    >>> AudioInput.from_mic(duration_sec=5)
    """
    source: AudioSource
    file_path: Optional[Path] = None
    audio_bytes: Optional[bytes] = None
    sample_rate: int = 16_000
    duration_sec: float = 5.0  # only used when source == MICROPHONE

    # -- factory helpers --------------------------------------------------

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "AudioInput":
        """Create an AudioInput from a .wav / .mp3 file path."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Audio file not found: {p}")
        suffix = p.suffix.lower()
        if suffix not in {".wav", ".mp3", ".flac", ".ogg", ".m4a"}:
            raise ValueError(
                f"Unsupported audio format '{suffix}'. "
                "Supported: .wav, .mp3, .flac, .ogg, .m4a"
            )
        return cls(source=AudioSource.FILE, file_path=p)

    @classmethod
    def from_bytes(cls, data: bytes, sample_rate: int = 16_000) -> "AudioInput":
        """Create an AudioInput from raw audio bytes."""
        if not data:
            raise ValueError("Audio bytes cannot be empty.")
        return cls(source=AudioSource.RAW_BYTES, audio_bytes=data,
                   sample_rate=sample_rate)

    @classmethod
    def from_mic(cls, duration_sec: float = 5.0,
                 sample_rate: int = 16_000) -> "AudioInput":
        """Create an AudioInput that will record from the default mic."""
        if duration_sec <= 0:
            raise ValueError("Recording duration must be positive.")
        return cls(source=AudioSource.MICROPHONE,
                   duration_sec=duration_sec, sample_rate=sample_rate)


@dataclass
class STTResult:
    """Result returned by any STT backend."""
    text: str
    detected_language: str
    confidence: float
    engine: str
    error: Optional[str] = None
    is_empty: bool = False

    @property
    def ok(self) -> bool:
        """``True`` when transcription succeeded without errors."""
        return self.error is None and not self.is_empty


@dataclass
class TTSResult:
    """Result returned by any TTS backend."""
    audio_bytes: bytes
    sample_rate: int
    language: str
    engine: str
    file_path: Optional[Path] = None
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        """``True`` when synthesis succeeded without errors."""
        return self.error is None and len(self.audio_bytes) > 0


# ---------------------------------------------------------------------------
# Abstract backend contracts
# ---------------------------------------------------------------------------

class STTBackend(ABC):
    """Contract that every Speech-to-Text engine must fulfil."""

    @abstractmethod
    def transcribe(self, audio: AudioInput) -> STTResult:
        """Transcribe *audio* and return an :class:`STTResult`."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return ``True`` if this backend's dependencies are installed."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable backend name, e.g. ``'faster-whisper'``."""
        ...


class TTSBackend(ABC):
    """Contract that every Text-to-Speech engine must fulfil."""

    @abstractmethod
    def synthesize(self, text: str, language: str) -> TTSResult:
        """Synthesize *text* in *language* and return a :class:`TTSResult`."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return ``True`` if this backend's dependencies are installed."""
        ...

    @abstractmethod
    def supports_language(self, language: str) -> bool:
        """Return ``True`` if this backend can synthesize *language*."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable backend name, e.g. ``'piper-tts'``."""
        ...
