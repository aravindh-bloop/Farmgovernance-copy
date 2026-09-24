"""
Multilingual language detection supporting major Indian regional languages and scripts.
"""
import unicodedata
from typing import Dict, Any

class LanguageDetector:
    SCRIPT_RANGES = {
        "hi": (0x0900, 0x097F), # Devanagari (Hindi, Marathi)
        "ta": (0x0B80, 0x0BFF), # Tamil
        "te": (0x0C00, 0x0C7F), # Telugu
        "kn": (0x0C80, 0x0CFF), # Kannada
        "ml": (0x0D00, 0x0D7F), # Malayalam
        "gu": (0x0A80, 0x0AFF), # Gujarati
        "bn": (0x0980, 0x09FF), # Bengali
        "pa": (0x0A00, 0x0A7F), # Gurmukhi (Punjabi)
        "or": (0x0B00, 0x0B7F), # Odia
    }

    def detect(self, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            return {"language": "en", "confidence": 1.0}

        counts = {lang: 0 for lang in self.SCRIPT_RANGES}
        total_indic = 0

        for char in text:
            cp = ord(char)
            for lang, (start, end) in self.SCRIPT_RANGES.items():
                if start <= cp <= end:
                    counts[lang] += 1
                    total_indic += 1
                    break

        if total_indic > 0:
            detected_lang = max(counts, key=counts.get)
            return {"language": detected_lang, "confidence": counts[detected_lang] / total_indic}

        return {"language": "en", "confidence": 0.95}
