"""
Chat API Endpoint for Multilingual Cooperative & Legal Inquiries.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Response
from typing import Optional
import tempfile
import os
from pydantic import BaseModel
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service
from ai_engine.language.speech_to_text import speech_to_text
from ai_engine.language.text_to_speech import text_to_speech, clean_speech_text
from ai_engine.language.interfaces import AudioInput

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    language: Optional[str] = "en"

@router.post("/", response_model=ChatResponse)
async def handle_chat_query(payload: ChatRequest):
    try:
        response = chat_service.process_chat(
            query=payload.query,
            language=payload.language or "en"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts")
async def handle_tts(payload: TTSRequest):
    try:
        clean_text = clean_speech_text(payload.text, max_chars=220)
        target_lang = payload.language or "en"
        # Auto-detect Indic script to guarantee pure native Indic pronunciation
        if any('\u0B80' <= c <= '\u0BFF' for c in clean_text):
            target_lang = "ta"
        elif any('\u0900' <= c <= '\u097F' for c in clean_text):
            target_lang = "hi"
        elif any('\u0C00' <= c <= '\u0C7F' for c in clean_text):
            target_lang = "te"
        elif any('\u0C80' <= c <= '\u0CFF' for c in clean_text):
            target_lang = "kn"
        elif any('\u0D00' <= c <= '\u0D7F' for c in clean_text):
            target_lang = "ml"
        elif any('\u0980' <= c <= '\u09FF' for c in clean_text):
            target_lang = "bn"
        elif any('\u0A80' <= c <= '\u0AFF' for c in clean_text):
            target_lang = "gu"
        elif any('\u0A00' <= c <= '\u0A7F' for c in clean_text):
            target_lang = "pa"

        tts_res = text_to_speech(clean_text, target_lang, play_audio=False)
        if not tts_res.ok or not tts_res.audio_bytes:
            raise HTTPException(status_code=500, detail=tts_res.error or "TTS synthesis failed")
        return Response(content=tts_res.audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice", response_model=ChatResponse)
async def handle_voice_query(
    audio: Optional[UploadFile] = File(None),
    language: Optional[str] = Form("en"),
    transcript: Optional[str] = Form(None)
):
    try:
        transcription = (transcript or "").strip()
        detected_lang = language or "en"
        
        if not transcription and audio:
            suffix = os.path.splitext(audio.filename or "")[1] or ".wav"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp_path = tmp.name
                content = await audio.read()
                tmp.write(content)
            try:
                audio_input = AudioInput.from_file(tmp_path)
                stt_res = speech_to_text(audio_input, language=language)
                if stt_res.ok and stt_res.text:
                    transcription = stt_res.text
                    detected_lang = stt_res.detected_language or detected_lang
            except Exception:
                pass
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        if not transcription or not transcription.strip():
            msg_map = {
                "en": "No clear speech was detected. Please speak into the microphone or type your question in the box below.",
                "hi": "कोई स्पष्ट आवाज़ नहीं मिली। कृपया माइक्रोफ़ोन में स्पष्ट बोलें या नीचे अपना प्रश्न लिखें।",
                "ta": "தெளிவான குரல் பதிவு எதுவும் கண்டறியப்படவில்லை. தயவுசெய்து மைக்கில் தெளிவாகப் பேசவும் அல்லது உங்கள் கேள்வியை தட்டச்சு செய்யவும்.",
                "te": "స్పష్టమైన వాయిస్ నమోదు కాలేదు. దయచేసి మైక్రోఫోన్‌లో స్పష్టంగా మాట్లాడండి లేదా మీ ప్రశ్నను టైప్ చేయండి.",
                "mr": "स्पष्ट आवाज आढळला नाही. कृपया मायक्रोफोनमध्ये स्पष्ट बोला किंवा खाली तुमचा प्रश्न टाइप करा."
            }
            user_msg = msg_map.get(detected_lang, msg_map["en"])
            return {
                "query": "",
                "transcription": "",
                "language": detected_lang,
                "domain": "general",
                "active_domains": [],
                "is_multi_domain": False,
                "confidence": 1.0,
                "answer": user_msg,
                "response": user_msg,
                "recommended_officer": None,
                "citations": [],
                "verification_status": True,
                "trust_score": 1.0,
                "verified_facts": [],
                "corrections_applied": [],
                "source_authority": "Smart Cooperative AI Voice Assistant",
                "procedure": None,
                "extracted_slots": {},
                "authorities": []
            }

        rag_res = chat_service.process_chat(
            query=transcription,
            language=detected_lang
        )
        rag_res["transcription"] = transcription
        return rag_res
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

