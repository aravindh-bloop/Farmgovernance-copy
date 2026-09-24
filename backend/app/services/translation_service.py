"""
Translation service bridging frontend and AI Engine translation layer.
"""
from ai_engine.language.translation import TranslationEngine
from ai_engine.language.language_detector import LanguageDetector

class TranslationService:
    def __init__(self):
        self.engine = TranslationEngine()
        self.detector = LanguageDetector()

    def translate_text(self, text: str, target_lang: str, source_lang: str = None) -> dict:
        if not source_lang:
            detection = self.detector.detect(text)
            source_lang = detection["language"]

        translated = self.engine.translate(text, source_lang, target_lang)
        return {
            "source_language": source_lang,
            "target_language": target_lang,
            "original_text": text,
            "translated_text": translated
        }

translation_service = TranslationService()
