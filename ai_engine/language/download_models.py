"""
Model downloader — fetches Whisper + Piper models for offline operation.

Usage
-----
python -m ai_engine.language.download_models           # download all
python -m ai_engine.language.download_models --stt      # STT models only
python -m ai_engine.language.download_models --tts      # TTS models only
python -m ai_engine.language.download_models --whisper-size large-v3  # bigger model
"""

import argparse
import logging
import sys
import urllib.request
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from ai_engine.language.config import (
    WHISPER_MODEL_SIZE,
    PIPER_VOICES,
    PIPER_MODELS_DIR,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Piper model download URLs
# ---------------------------------------------------------------------------

_PIPER_HF_BASE = (
    "https://huggingface.co/rhasspy/piper-voices/resolve/main"
)


def _piper_urls(model_name: str):
    """
    Build download URLs for a Piper voice model.
    Structure: <lang_code>/<region>/<model_name>/<quality>/<model_name>.onnx
    """
    parts = model_name.split("-")
    lang_region = parts[0]                                # e.g. "en_US" or "hi_IN"
    voice_name = parts[1] if len(parts) > 1 else "default"
    quality = parts[2] if len(parts) > 2 else "medium"

    lang_code = lang_region.split("_")[0]                 # e.g. "en" or "hi"

    base = f"{_PIPER_HF_BASE}/{lang_code}/{lang_region}/{voice_name}/{quality}"
    return {
        "onnx": f"{base}/{model_name}.onnx",
        "json": f"{base}/{model_name}.onnx.json",
    }


def _download_file(url: str, dest: Path, desc: str = ""):
    """Download a file with a progress indicator."""
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  ✓ Already exists: {dest.name}")
        return

    print(f"  ↓ Downloading {desc or dest.name} …")
    print(f"    URL: {url}")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            dest.parent.mkdir(parents=True, exist_ok=True)

            with open(dest, "wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)  # 1 MB chunks
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = downloaded * 100 // total
                        bar = "█" * (pct // 2) + "░" * (50 - pct // 2)
                        print(f"\r    [{bar}] {pct}%  ({downloaded // 1024:,} KB)", end="", flush=True)

            print()  # newline after progress bar
            print(f"  ✓ Saved: {dest.name} ({dest.stat().st_size // 1024:,} KB)")

    except Exception as exc:
        print(f"\n  ✗ Download failed for {desc or dest.name}: {exc}")
        if dest.exists():
            try:
                dest.unlink()
            except OSError:
                pass
        raise


# ---------------------------------------------------------------------------
# STT (Whisper) model download
# ---------------------------------------------------------------------------

def download_whisper_model(model_size: str = WHISPER_MODEL_SIZE) -> bool:
    """Download the faster-whisper model."""
    print(f"\n{'='*60}")
    print(f"  STT: Downloading faster-whisper model '{model_size}'")
    print(f"{'='*60}")

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("  ✗ faster-whisper not installed.")
        print("    Run: pip install faster-whisper")
        return False

    try:
        print("  ↓ Initializing model download (HuggingFace Hub) …")
        _model = WhisperModel(model_size, device="cpu", compute_type="int8")
        print(f"  ✓ Whisper model '{model_size}' is ready.")
        del _model
        return True
    except Exception as exc:
        print(f"  ✗ Failed to download Whisper model '{model_size}': {exc}")
        return False


# ---------------------------------------------------------------------------
# TTS (Piper) model download
# ---------------------------------------------------------------------------

def download_piper_models() -> bool:
    """Download Piper ONNX voice models for all configured languages."""
    print(f"\n{'='*60}")
    print(f"  TTS: Downloading Piper voice models")
    print(f"{'='*60}")

    if not PIPER_VOICES:
        print("  (No Piper voices configured in config.py)")
        return True

    success = True
    for lang, info in PIPER_VOICES.items():
        model_name = info["model_name"]
        desc = info.get("description", model_name)
        print(f"\n  Language [{lang}]: {desc}")

        urls = _piper_urls(model_name)
        onnx_dest = PIPER_MODELS_DIR / f"{model_name}.onnx"
        json_dest = PIPER_MODELS_DIR / f"{model_name}.onnx.json"

        try:
            _download_file(urls["onnx"], onnx_dest, f"{model_name}.onnx")
            _download_file(urls["json"], json_dest, f"{model_name}.onnx.json")
        except Exception:
            success = False

    return success


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Download models for offline STT/TTS",
    )
    parser.add_argument("--stt", action="store_true", help="Download STT models only.")
    parser.add_argument("--tts", action="store_true", help="Download TTS models only.")
    parser.add_argument(
        "--whisper-size",
        type=str,
        default=WHISPER_MODEL_SIZE,
        help=f"Whisper model size (default: {WHISPER_MODEL_SIZE}).",
    )
    args = parser.parse_args()

    do_stt = args.stt or (not args.stt and not args.tts)
    do_tts = args.tts or (not args.stt and not args.tts)

    print("\n" + "=" * 60)
    print("  🔽 MODEL DOWNLOADER — Multilingual STT/TTS Module")
    print("=" * 60)

    stt_ok = True
    tts_ok = True

    if do_stt:
        stt_ok = download_whisper_model(args.whisper_size)

    if do_tts:
        tts_ok = download_piper_models()

    ok = stt_ok and tts_ok

    print("\n" + "=" * 60)
    if ok:
        print("  ✅ All models downloaded successfully!")
        print("  Run the demo: python -m ai_engine.language.demo")
    else:
        print("  ⚠️ Some downloads failed — check the errors above.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

