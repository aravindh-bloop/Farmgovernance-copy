"""
Bhashini (MeitY ULCA) adapter — stub showing how the national-language API
would plug in behind the same STTBackend / TTSBackend interfaces.

This is **not** a working client — it demonstrates the correct request shapes,
auth headers, and response mapping so a teammate can wire in real credentials
later.

References
----------
- Portal: https://bhashini.gov.in
- API docs (Postman): https://www.postman.com/bhashini/workspace/bhashini-api
- GitBook: https://bhashini.gitbook.io/bhashini-apis/
"""

import base64  # noqa: F401 — used in the documented TODO pattern below
import json
import logging
import os

from .interfaces import (
    AudioInput,
    AudioSource,
    STTBackend,
    STTResult,
    TTSBackend,
    TTSResult,
)
from .config import DEFAULT_SAMPLE_RATE, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment variables expected in .env
# ---------------------------------------------------------------------------
# BHASHINI_API_KEY      – inference API key from the Bhashini portal
# BHASHINI_USER_ID      – your registered user / org ID
# BHASHINI_PIPELINE_ID  – pipeline ID that includes ASR + TTS tasks

_BHASHINI_BASE_URL = "https://dhruva-api.bhashini.gov.in/services/inference"


def _get_creds():
    """Read Bhashini credentials from environment."""
    return {
        "api_key": os.getenv("BHASHINI_API_KEY", ""),
        "user_id": os.getenv("BHASHINI_USER_ID", ""),
        "pipeline_id": os.getenv("BHASHINI_PIPELINE_ID", ""),
    }


def _has_creds() -> bool:
    creds = _get_creds()
    return bool(creds["api_key"] and creds["user_id"])


# ---------------------------------------------------------------------------
# Bhashini STT Adapter
# ---------------------------------------------------------------------------

class BhashiniSTTBackend(STTBackend):
    """
    Stub adapter for Bhashini's ASR (Automatic Speech Recognition) service.

    Shows the exact HTTP request/response shape.  To make it live:
    1. Register at https://bhashini.gov.in and get credentials.
    2. Set ``BHASHINI_API_KEY``, ``BHASHINI_USER_ID``, ``BHASHINI_PIPELINE_ID``
       in your ``.env`` file.
    3. Replace the ``NotImplementedError`` with a real ``requests.post()`` call.
    """

    @property
    def name(self) -> str:
        return "bhashini-asr"

    def is_available(self) -> bool:
        return _has_creds()

    def transcribe(self, audio: AudioInput) -> STTResult:
        if not _has_creds():
            return STTResult(
                text="",
                detected_language="unknown",
                confidence=0.0,
                engine=self.name,
                error=(
                    "Bhashini credentials not configured.  "
                    "Set BHASHINI_API_KEY and BHASHINI_USER_ID in .env"
                ),
                is_empty=True,
            )

        # --- Build the request payload (for documentation) ---------------
        #
        # In a real implementation you would:
        #   1. Read the audio bytes from audio.file_path / audio.audio_bytes
        #   2. Base64-encode them
        #   3. POST to the Bhashini inference endpoint
        #
        creds = _get_creds()

        # Determine source language hint (Bhashini code)
        source_lang = "hi"  # default hint
        if audio.source == AudioSource.FILE and audio.file_path:
            # In practice, you might pass the language detected by Whisper
            # or let Bhashini auto-detect.
            pass

        _example_request = {
            "url": f"{_BHASHINI_BASE_URL}/asr",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": creds["api_key"],
                "userID": creds["user_id"],
            },
            "body": {
                "pipelineTasks": [
                    {
                        "taskType": "asr",
                        "config": {
                            "language": {
                                "sourceLanguage": source_lang,
                            },
                            "serviceId": "<MODEL_SERVICE_ID>",
                            "audioFormat": "wav",
                            "samplingRate": 16000,
                        },
                    }
                ],
                "inputData": {
                    "audio": [
                        {
                            "audioContent": "<BASE64_ENCODED_AUDIO>",
                        }
                    ],
                },
            },
        }

        _example_response = {
            "pipelineResponse": [
                {
                    "taskType": "asr",
                    "output": [
                        {
                            "source": "transcribed text here",
                            "langDetected": source_lang,
                        }
                    ],
                }
            ]
        }

        logger.info(
            "Bhashini ASR request shape:\n%s",
            json.dumps(_example_request, indent=2, ensure_ascii=False),
        )

        # -----------------------------------------------------------------
        # TODO: Replace with actual HTTP call:
        #
        #   import requests
        #   audio_b64 = base64.b64encode(audio_bytes).decode()
        #   payload = { ... }  # use _example_request shape above
        #   resp = requests.post(url, json=payload, headers=headers)
        #   data = resp.json()
        #   text = data["pipelineResponse"][0]["output"][0]["source"]
        #   lang = data["pipelineResponse"][0]["output"][0]["langDetected"]
        #   return STTResult(text=text, detected_language=lang, ...)
        # -----------------------------------------------------------------

        raise NotImplementedError(
            "Bhashini ASR stub — replace with real API call.  "
            "See the request/response shapes logged above."
        )


# ---------------------------------------------------------------------------
# Bhashini TTS Adapter
# ---------------------------------------------------------------------------

class BhashiniTTSBackend(TTSBackend):
    """
    Stub adapter for Bhashini's TTS (Text-to-Speech Synthesis) service.

    Shows the exact HTTP request/response shape.  Same setup steps as the
    ASR adapter above.
    """

    @property
    def name(self) -> str:
        return "bhashini-tts"

    def is_available(self) -> bool:
        return _has_creds()

    def supports_language(self, language: str) -> bool:
        # Bhashini supports all 22 scheduled Indian languages
        return language in SUPPORTED_LANGUAGES

    def synthesize(self, text: str, language: str) -> TTSResult:
        if not _has_creds():
            return TTSResult(
                audio_bytes=b"",
                sample_rate=DEFAULT_SAMPLE_RATE,
                language=language,
                engine=self.name,
                error=(
                    "Bhashini credentials not configured.  "
                    "Set BHASHINI_API_KEY and BHASHINI_USER_ID in .env"
                ),
            )

        if not text or not text.strip():
            return TTSResult(
                audio_bytes=b"",
                sample_rate=DEFAULT_SAMPLE_RATE,
                language=language,
                engine=self.name,
                error="Empty text — nothing to synthesize.",
            )

        creds = _get_creds()

        _example_request = {
            "url": f"{_BHASHINI_BASE_URL}/tts",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": creds["api_key"],
                "userID": creds["user_id"],
            },
            "body": {
                "pipelineTasks": [
                    {
                        "taskType": "tts",
                        "config": {
                            "language": {
                                "sourceLanguage": language,
                            },
                            "serviceId": "<MODEL_SERVICE_ID>",
                            "gender": "female",
                            "samplingRate": 22050,
                        },
                    }
                ],
                "inputData": {
                    "input": [
                        {
                            "source": text,
                        }
                    ],
                },
            },
        }

        _example_response = {
            "pipelineResponse": [
                {
                    "taskType": "tts",
                    "audio": [
                        {
                            "audioContent": "<BASE64_ENCODED_WAV>",
                            "audioUri": None,
                        }
                    ],
                }
            ]
        }

        logger.info(
            "Bhashini TTS request shape:\n%s",
            json.dumps(_example_request, indent=2, ensure_ascii=False),
        )

        # -----------------------------------------------------------------
        # TODO: Replace with actual HTTP call:
        #
        #   import requests
        #   payload = { ... }  # use _example_request shape above
        #   resp = requests.post(url, json=payload, headers=headers)
        #   data = resp.json()
        #   audio_b64 = data["pipelineResponse"][0]["audio"][0]["audioContent"]
        #   audio_bytes = base64.b64decode(audio_b64)
        #   return TTSResult(audio_bytes=audio_bytes, ...)
        # -----------------------------------------------------------------

        raise NotImplementedError(
            "Bhashini TTS stub — replace with real API call.  "
            "See the request/response shapes logged above."
        )
