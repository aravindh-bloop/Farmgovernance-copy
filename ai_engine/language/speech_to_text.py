"""
Speech-to-Text engine — Faster-Whisper backend with live mic + file input.

Public API
----------
>>> from ai_engine.language import speech_to_text
>>> result = speech_to_text("path/to/audio.wav")
>>> print(result.text, result.detected_language, result.confidence)
"""

import logging
import tempfile
from pathlib import Path
from typing import Optional, Union

from .interfaces import AudioInput, AudioSource, STTBackend, STTResult
from .config import (
    WHISPER_MODEL_SIZE,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE,
    WHISPER_BEAM_SIZE,
)
from . import audio_utils

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Whisper STT Backend
# ---------------------------------------------------------------------------

class WhisperSTTBackend(STTBackend):
    """
    Offline Speech-to-Text powered by **faster-whisper** (CTranslate2).

    The model is **lazy-loaded** on first ``transcribe()`` call so importing
    this module stays fast.
    """

    def __init__(
        self,
        model_size: str = WHISPER_MODEL_SIZE,
        device: str = WHISPER_DEVICE,
        compute_type: str = WHISPER_COMPUTE_TYPE,
        beam_size: int = WHISPER_BEAM_SIZE,
    ):
        self._model_size = model_size
        self._device = device
        self._compute_type = compute_type
        self._beam_size = beam_size
        self._model = None  # lazy

    # -- interface ---------------------------------------------------------

    @property
    def name(self) -> str:
        return "faster-whisper"

    def is_available(self) -> bool:
        try:
            import faster_whisper  # noqa: F401
            return True
        except ImportError:
            return False

    def transcribe(self, audio: Union[AudioInput, str, Path, bytes]) -> STTResult:
        """
        Transcribe audio and auto-detect the spoken language.
        """
        # Normalise input if raw type passed directly to backend
        if isinstance(audio, str):
            if audio.lower() == "mic":
                audio = AudioInput.from_mic()
            else:
                audio = AudioInput.from_file(audio)
        elif isinstance(audio, Path):
            audio = AudioInput.from_file(audio)
        elif isinstance(audio, bytes):
            audio = AudioInput.from_bytes(audio)
        elif not isinstance(audio, AudioInput):
            return STTResult(
                text="",
                detected_language="unknown",
                confidence=0.0,
                engine=self.name,
                error=f"Unsupported audio input type: {type(audio).__name__}",
                is_empty=True,
            )

        try:
            return self._do_transcribe(audio)
        except Exception as exc:
            logger.exception("STT transcription failed")
            return STTResult(
                text="",
                detected_language="unknown",
                confidence=0.0,
                engine=self.name,
                error=str(exc),
                is_empty=True,
            )

    # -- internals --------------------------------------------------------

    def _ensure_model(self):
        """Lazy-load the Whisper model on first use."""
        if self._model is not None:
            return

        try:
            from faster_whisper import WhisperModel
        except ImportError:
            raise RuntimeError(
                "faster-whisper is not installed. "
                "Install it with: pip install faster-whisper"
            )

        logger.info(
            "Loading Whisper model '%s' (device=%s, compute=%s) …",
            self._model_size, self._device, self._compute_type,
        )
        self._model = WhisperModel(
            self._model_size,
            device=self._device,
            compute_type=self._compute_type,
        )
        logger.info("Whisper model loaded.")

    def _do_transcribe(self, audio: AudioInput) -> STTResult:
        self._ensure_model()

        audio_path: Optional[Path] = None
        tmp_path: Optional[Path] = None

        if audio.source == AudioSource.FILE:
            audio_path = audio.file_path

        elif audio.source == AudioSource.MICROPHONE:
            arr = audio_utils.record_from_mic(
                duration_sec=audio.duration_sec,
                sample_rate=audio.sample_rate,
            )
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            tmp_path = Path(tmp.name)
            tmp.close()  # Close handle BEFORE writing (Windows compat)
            audio_utils.save_audio(arr, tmp_path, audio.sample_rate)
            audio_path = tmp_path

        elif audio.source == AudioSource.RAW_BYTES:
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            tmp_path = Path(tmp.name)
            tmp.close()  # Close handle BEFORE writing (Windows compat)
            tmp_path.write_bytes(audio.audio_bytes)
            audio_path = tmp_path

        try:
            segments, info = self._model.transcribe(
                str(audio_path),
                beam_size=self._beam_size,
                vad_filter=True,  # skip silence
            )

            # Materialise segments
            full_text = " ".join(seg.text.strip() for seg in segments).strip()

            if not full_text:
                return STTResult(
                    text="",
                    detected_language=getattr(info, "language", "unknown") or "unknown",
                    confidence=0.0,
                    engine=self.name,
                    error="No speech detected in audio.",
                    is_empty=True,
                )

            return STTResult(
                text=full_text,
                detected_language=getattr(info, "language", "unknown") or "unknown",
                confidence=round(getattr(info, "language_probability", 0.0), 4),
                engine=self.name,
            )
        finally:
            if tmp_path and tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass


# ---------------------------------------------------------------------------
# Module-level singleton & convenience function
# ---------------------------------------------------------------------------

_default_backend: Optional[WhisperSTTBackend] = None


def _get_default_backend() -> WhisperSTTBackend:
    global _default_backend
    if _default_backend is None:
        _default_backend = WhisperSTTBackend()
    return _default_backend


def speech_to_text(
    audio_input,
    backend: Optional[STTBackend] = None,
) -> STTResult:
    """
    High-level convenience function — the main entry point for teammates.

    Parameters
    ----------
    audio_input : str | Path | bytes | AudioInput
        - A file path string or ``Path`` → transcribe that file.
        - Raw ``bytes`` → treat as audio data.
        - ``"mic"`` → record from the default microphone.
        - An ``AudioInput`` instance → use directly.
    backend : STTBackend, optional
        Custom backend (e.g. ``BhashiniSTTBackend``). Defaults to
        the built-in Whisper backend.

    Returns
    -------
    STTResult
        ``{text, detected_language, confidence, engine, error}``
    """
    # Normalise input first
    if isinstance(audio_input, str):
        if audio_input.lower().strip() == "mic":
            audio = AudioInput.from_mic()
        else:
            try:
                audio = AudioInput.from_file(audio_input)
            except Exception as exc:
                return STTResult(
                    text="",
                    detected_language="unknown",
                    confidence=0.0,
                    engine="none",
                    error=str(exc),
                    is_empty=True,
                )
    elif isinstance(audio_input, Path):
        try:
            audio = AudioInput.from_file(audio_input)
        except Exception as exc:
            return STTResult(
                text="",
                detected_language="unknown",
                confidence=0.0,
                engine="none",
                error=str(exc),
                is_empty=True,
            )
    elif isinstance(audio_input, bytes):
        try:
            audio = AudioInput.from_bytes(audio_input)
        except Exception as exc:
            return STTResult(
                text="",
                detected_language="unknown",
                confidence=0.0,
                engine="none",
                error=str(exc),
                is_empty=True,
            )
    elif isinstance(audio_input, AudioInput):
        audio = audio_input
    else:
        return STTResult(
            text="",
            detected_language="unknown",
            confidence=0.0,
            engine="none",
            error=f"Unsupported audio_input type: {type(audio_input).__name__}",
            is_empty=True,
        )

    if backend is None:
        try:
            from .sarvam_adapter import SarvamSTTBackend
            sarvam = SarvamSTTBackend()
            engine = sarvam if sarvam.is_available() else _get_default_backend()
        except Exception:
            engine = _get_default_backend()
    else:
        engine = backend

    if not engine.is_available():
        return STTResult(
            text="",
            detected_language="unknown",
            confidence=0.0,
            engine=engine.name,
            error=f"{engine.name} is not installed. Run: pip install -r ai_engine/language/requirements.txt",
            is_empty=True,
        )

    return engine.transcribe(audio)


