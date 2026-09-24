"""
End-to-end demo: record/accept audio → transcribe → print → synthesize → play.

Usage
-----
# Live mic (record 5 seconds, transcribe, reply, play)
python -m ai_engine.language.demo

# From an audio file
python -m ai_engine.language.demo --file path/to/audio.wav

# Skip audio playback (CI / headless)
python -m ai_engine.language.demo --file audio.wav --no-play

# Custom recording duration
python -m ai_engine.language.demo --duration 8

# Use Bhashini adapter (stub — will show request shapes)
python -m ai_engine.language.demo --backend bhashini
"""

import argparse
import logging
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so we can run as
#   python -m ai_engine.language.demo
# from the repo root directory.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from ai_engine.language.interfaces import AudioInput
from ai_engine.language.speech_to_text import speech_to_text, WhisperSTTBackend
from ai_engine.language.text_to_speech import text_to_speech
from ai_engine.language.bhashini_adapter import BhashiniSTTBackend
from ai_engine.language.config import SUPPORTED_LANGUAGES
from ai_engine.language import audio_utils

# ---------------------------------------------------------------------------
# Stub replies (simulating what the RAG + LLM pipeline would return)
# ---------------------------------------------------------------------------
_STUB_REPLIES = {
    "en": (
        "Under the PM-KISAN scheme, eligible farmers receive ₹6,000 per year "
        "in three equal installments directly to their bank accounts. "
        "To apply, visit your nearest Common Service Centre with your Aadhaar card."
    ),
    "hi": (
        "पीएम किसान सम्मान निधि योजना के तहत, पात्र किसानों को प्रति वर्ष ₹6,000 "
        "तीन समान किस्तों में सीधे उनके बैंक खाते में मिलते हैं। "
        "आवेदन करने के लिए अपने नज़दीकी जन सेवा केंद्र पर आधार कार्ड लेकर जाएं।"
    ),
    "ta": (
        "பிரதமர் கிசான் சம்மான் நிதி திட்டத்தின் கீழ், தகுதியான விவசாயிகள் "
        "ஆண்டுக்கு ₹6,000 மூன்று சம தவணைகளில் நேரடியாக வங்கிக் கணக்கில் பெறுவார்கள்."
    ),
}


def _get_reply(language: str) -> str:
    """Return a stub reply in the detected language."""
    return _STUB_REPLIES.get(language, _STUB_REPLIES["en"])


# ---------------------------------------------------------------------------
# Pretty terminal output helpers
# ---------------------------------------------------------------------------

def _banner(step: str, msg: str):
    print(f"\n  {'─' * 60}")
    print(f"  [{step}]  {msg}")
    print(f"  {'─' * 60}")


def _info(label: str, value: str):
    print(f"    {label:<14s}  {value}")


# ---------------------------------------------------------------------------
# Main demo flow
# ---------------------------------------------------------------------------

def run_demo(
    file_path: str = None,
    duration: float = 5.0,
    backend_name: str = "whisper",
    no_play: bool = False,
):
    """Run the full STT → reply → TTS demo loop."""

    print("\n" + "=" * 64)
    print("  🎙️  MULTILINGUAL VOICE ASSISTANT — STT/TTS DEMO")
    print("  Team BRAVITS | SIH 2026 — Problem SIH26088")
    print("=" * 64)

    supported = ", ".join(
        f"{v['name']} ({k})" for k, v in SUPPORTED_LANGUAGES.items()
    )
    _info("Languages", supported)

    # ----- Step 1: Obtain audio ------------------------------------------
    if file_path:
        _banner("1  FILE INPUT", f"Loading audio from: {file_path}")
        audio = AudioInput.from_file(file_path)
    else:
        _banner("1  MIC RECORDING", f"Speak now — recording {duration:.0f} seconds …")
        audio = AudioInput.from_mic(duration_sec=duration)

    # ----- Step 2: Transcribe (STT) --------------------------------------
    _banner("2  SPEECH → TEXT", f"Transcribing with backend: {backend_name}")

    stt_backend = None
    if backend_name == "bhashini":
        stt_backend = BhashiniSTTBackend()

    stt_result = speech_to_text(audio, backend=stt_backend)

    if not stt_result.ok:
        print(f"\n  ❌  STT Error: {stt_result.error}")
        print("  Tip: Make sure faster-whisper is installed and models are downloaded.")
        return

    _info("Transcript", f'"{stt_result.text}"')
    _info("Language", f"{stt_result.detected_language} (confidence: {stt_result.confidence:.2f})")
    _info("Engine", stt_result.engine)

    # ----- Step 3: Generate reply (stub) ---------------------------------
    reply_lang = stt_result.detected_language
    reply_text = _get_reply(reply_lang)

    _banner("3  LLM REPLY", "(Stub — simulating RAG + LLM response)")
    _info("Language", reply_lang)
    _info("Reply", f'"{reply_text[:80]}…"' if len(reply_text) > 80 else f'"{reply_text}"')

    # ----- Step 4: Synthesize (TTS) --------------------------------------
    _banner("4  TEXT → SPEECH", f"Synthesizing {reply_lang} audio …")

    tts_result = text_to_speech(
        reply_text,
        reply_lang,
        play_audio=(not no_play),
    )

    if not tts_result.ok:
        print(f"\n  ⚠️  TTS Warning: {tts_result.error}")
        print("  (The transcription still worked — only audio playback failed.)")
    else:
        _info("Engine", tts_result.engine)
        _info("Audio size", f"{len(tts_result.audio_bytes):,} bytes")
        if no_play:
            _info("Playback", "Skipped (--no-play)")
        else:
            _info("Playback", "✅ Done")

    # ----- Done ----------------------------------------------------------
    print("\n" + "=" * 64)
    print("  ✅  Demo complete!  Full pipeline: mic → STT → reply → TTS → speaker")
    print("=" * 64 + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Multilingual STT/TTS end-to-end demo",
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        default=None,
        help="Path to an audio file (.wav / .mp3).  Omit to use live mic.",
    )
    parser.add_argument(
        "--duration", "-d",
        type=float,
        default=5.0,
        help="Mic recording duration in seconds (default: 5).",
    )
    parser.add_argument(
        "--backend", "-b",
        type=str,
        choices=["whisper", "bhashini"],
        default="whisper",
        help="STT backend to use (default: whisper).",
    )
    parser.add_argument(
        "--no-play",
        action="store_true",
        help="Skip audio playback (for CI / headless environments).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging.",
    )
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(name)-30s  %(levelname)-8s  %(message)s",
    )

    try:
        run_demo(
            file_path=args.file,
            duration=args.duration,
            backend_name=args.backend,
            no_play=args.no_play,
        )
    except KeyboardInterrupt:
        print("\n  ⏹  Interrupted.")
    except Exception as exc:
        print(f"\n  ❌  Fatal error: {exc}")
        raise


if __name__ == "__main__":
    main()
