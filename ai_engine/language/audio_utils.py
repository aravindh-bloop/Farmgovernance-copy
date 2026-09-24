"""
Shared audio utilities — mic recording, file loading, playback, and format
conversion. Used by both the STT and TTS engines.
"""

import io
import logging
import struct
import wave
from pathlib import Path
from typing import Tuple, Union

import numpy as np

from .config import DEFAULT_SAMPLE_RATE, DEFAULT_MIC_DURATION, DEFAULT_CHANNELS

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Microphone recording
# ---------------------------------------------------------------------------

def record_from_mic(
    duration_sec: float = DEFAULT_MIC_DURATION,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
) -> np.ndarray:
    """
    Record audio from the default system microphone.

    Returns a 1-D NumPy float32 array of shape ``(samples,)``.
    """
    if duration_sec <= 0:
        raise ValueError("Recording duration must be positive.")

    try:
        import sounddevice as sd
    except ImportError:
        raise RuntimeError(
            "sounddevice is required for mic recording. "
            "Install it with: pip install sounddevice"
        )

    logger.info("Recording %.2f s of audio at %d Hz …", duration_sec, sample_rate)
    try:
        audio = sd.rec(
            int(duration_sec * sample_rate),
            samplerate=sample_rate,
            channels=channels,
            dtype="float32",
        )
        sd.wait()  # block until recording is finished
    except Exception as exc:
        raise RuntimeError(f"Microphone recording failed: {exc}") from exc

    # Flatten to mono 1-D
    audio = np.squeeze(audio)
    if audio.size == 0 or np.all(audio == 0):
        logger.warning("Recorded audio is empty or pure silence.")

    logger.info("Recorded %d samples (%.2f s).", audio.size, audio.size / max(sample_rate, 1))
    return audio


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def load_audio_file(
    path: Union[str, Path],
    target_sr: int = DEFAULT_SAMPLE_RATE,
) -> Tuple[np.ndarray, int]:
    """
    Load an audio file and resample to *target_sr* Hz mono float32.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    suffix = path.suffix.lower()

    # --- WAV: pure-stdlib or soundfile ---
    if suffix == ".wav":
        return _load_wav(path, target_sr)

    # --- Everything else via pydub ---
    try:
        from pydub import AudioSegment
    except ImportError:
        raise RuntimeError(
            f"pydub is required for {suffix} files. "
            "Install it with: pip install pydub"
        )

    try:
        seg = AudioSegment.from_file(str(path))
        seg = seg.set_channels(1).set_frame_rate(target_sr).set_sample_width(2)
        samples = np.array(seg.get_array_of_samples(), dtype=np.float32) / 32768.0
        return samples, target_sr
    except Exception as exc:
        raise RuntimeError(f"Failed to load audio file '{path}': {exc}") from exc


def _load_wav(path: Path, target_sr: int) -> Tuple[np.ndarray, int]:
    """Load a WAV file using soundfile if available, otherwise stdlib wave."""
    try:
        import soundfile as sf
        audio, sr = sf.read(str(path), dtype="float32", always_2d=False)
        if len(audio) == 0:
            return np.array([], dtype=np.float32), target_sr
        # Mono
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        # Resample if needed
        if sr != target_sr and len(audio) > 1:
            ratio = target_sr / sr
            new_len = max(1, int(len(audio) * ratio))
            indices = np.linspace(0, len(audio) - 1, new_len)
            audio = np.interp(indices, np.arange(len(audio)), audio).astype(np.float32)
        return audio, target_sr
    except ImportError:
        pass

    # Fallback: stdlib wave
    with wave.open(str(path), "rb") as wf:
        n_ch = wf.getnchannels()
        sw = wf.getsampwidth()
        sr = wf.getframerate()
        frames = wf.readframes(wf.getnframes())

    if len(frames) == 0:
        return np.array([], dtype=np.float32), target_sr

    # Decode PCM
    if sw == 2:  # 16-bit
        fmt = f"<{len(frames) // 2}h"
        samples = np.array(struct.unpack(fmt, frames), dtype=np.float32) / 32768.0
    elif sw == 1:  # 8-bit unsigned
        samples = np.frombuffer(frames, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0
    elif sw == 4:  # 32-bit int or float
        samples = np.frombuffer(frames, dtype=np.float32)
    elif sw == 3:  # 24-bit
        raw = np.frombuffer(frames, dtype=np.uint8)
        # Convert 24-bit to 32-bit int
        raw_padded = np.zeros(len(raw) // 3 * 4, dtype=np.uint8)
        raw_padded[1::4] = raw[0::3]
        raw_padded[2::4] = raw[1::3]
        raw_padded[3::4] = raw[2::3]
        samples = raw_padded.view(np.int32).astype(np.float32) / 2147483648.0
    else:
        raise ValueError(f"Unsupported WAV sample width: {sw} bytes")

    # Downmix to mono
    if n_ch > 1 and len(samples) >= n_ch:
        samples = samples.reshape(-1, n_ch).mean(axis=1)

    # Resample if needed
    if sr != target_sr and len(samples) > 1:
        ratio = target_sr / sr
        new_len = max(1, int(len(samples) * ratio))
        indices = np.linspace(0, len(samples) - 1, new_len)
        samples = np.interp(indices, np.arange(len(samples)), samples).astype(np.float32)

    return samples, target_sr


def save_audio(
    audio: Union[np.ndarray, bytes],
    path: Union[str, Path],
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> Path:
    """
    Save audio data (NumPy float32 array or raw WAV/MP3 bytes) to a file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(audio, bytes):
        path.write_bytes(audio)
        return path

    # NumPy array → 16-bit PCM WAV
    pcm = (audio * 32767).clip(-32768, 32767).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())

    return path


def numpy_to_wav_bytes(
    audio: np.ndarray,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> bytes:
    """Convert a float32 NumPy array to in-memory WAV bytes."""
    pcm = (audio * 32767).clip(-32768, 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())
    return buf.getvalue()


def wav_bytes_to_numpy(data: bytes) -> Tuple[np.ndarray, int]:
    """Convert WAV bytes back to (float32 array, sample_rate)."""
    if not data:
        return np.array([], dtype=np.float32), DEFAULT_SAMPLE_RATE

    buf = io.BytesIO(data)
    try:
        with wave.open(buf, "rb") as wf:
            sr = wf.getframerate()
            sw = wf.getsampwidth()
            frames = wf.readframes(wf.getnframes())

        if len(frames) == 0:
            return np.array([], dtype=np.float32), sr

        if sw == 2:
            fmt = f"<{len(frames) // 2}h"
            arr = np.array(struct.unpack(fmt, frames), dtype=np.float32) / 32768.0
        elif sw == 1:
            arr = np.frombuffer(frames, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0
        elif sw == 4:
            arr = np.frombuffer(frames, dtype=np.float32)
        else:
            arr = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

        return arr, sr
    except Exception as exc:
        logger.warning("Failed to decode WAV bytes via wave module: %s", exc)
        # Try soundfile fallback if available
        try:
            import soundfile as sf
            buf.seek(0)
            arr, sr = sf.read(buf, dtype="float32", always_2d=False)
            if arr.ndim > 1:
                arr = arr.mean(axis=1)
            return arr, sr
        except Exception:
            raise ValueError(f"Invalid or unsupported audio bytes: {exc}") from exc


# ---------------------------------------------------------------------------
# Playback
# ---------------------------------------------------------------------------

def play_audio(
    audio: Union[np.ndarray, bytes, str, Path],
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> None:
    """
    Play audio through the system's default speaker.
    Accepts a NumPy array, raw WAV bytes, or a file path.
    """
    try:
        import sounddevice as sd
    except ImportError:
        raise RuntimeError(
            "sounddevice is required for audio playback. "
            "Install it with: pip install sounddevice"
        )

    if isinstance(audio, (str, Path)):
        arr, sr = load_audio_file(audio, target_sr=sample_rate)
    elif isinstance(audio, bytes):
        arr, sr = wav_bytes_to_numpy(audio)
    else:
        arr = audio
        sr = sample_rate

    if arr.size == 0:
        logger.warning("Audio buffer is empty — skipping playback.")
        return

    duration = len(arr) / max(sr, 1)
    logger.info("Playing audio (%.2f s) …", duration)
    try:
        sd.play(arr, samplerate=sr)
        sd.wait()
    except Exception as exc:
        raise RuntimeError(f"Audio playback failed: {exc}") from exc

