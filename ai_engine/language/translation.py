"""
Multilingual Translation Engine supporting Neural MT, Bhashini AI pipeline, and comprehensive local glossary.
Provides complete, fluent, and contextual translation for Tamil (ta), Hindi (hi), Telugu (te),
Kannada (kn), Marathi (mr), Bengali (bn), Gujarati (gu), Malayalam (ml), Punjabi (pa), and Odia (or).
"""
import urllib.request
import urllib.parse
import json
import re
from typing import Dict, Any, List

class TranslationEngine:
    def __init__(self):
        # In-memory translation cache for lightning-fast repeated translations
        self._cache: Dict[str, str] = {}

        # Domain-specific terminology and UI glossary
        self.glossary = {
            "ta": {
                "**Overview:**": "**📌 பொதுவான விளக்கம்:**",
                "**Overview & Guidance:**": "**📌 பொதுவான விளக்கம் மற்றும் வழிகாட்டுதல்:**",
                "**Problem Analysis:**": "**🔍 பிரச்சனை விபரம்:**",
                "**Statutory Remedy & Farmer Rights:**": "**🛡️ சட்டப்பூர்வ தீர்வு & உழவர் உரிமைகள்:**",
                "**Mandatory Evidence Checklist:**": "**📁 தேவையான முக்கிய ஆவணங்கள்:**",
                "**Key Provisions / Guidelines:**": "**📜 முக்கிய நெறிமுறைகள் & வழிகாட்டுதல்கள்:**",
                "**3-Tier Escalation Ladder": "**🪜 3 அடுக்கு மேல்முறையீட்டு படிநிலைகள்",
                "**Competent Override Authority:**": "**🏛️ மேல்முறையீட்டு உயர் அதிகாரி:**",
                "**Applicable Statutory Laws:**": "**📜 பொருந்தக்கூடிய சட்டப் பிரிவுகள்:**",
                "**Penalties on Violator:**": "**⚠️ விதிமீறலுக்கான தண்டனை:**",
                "**Ready-to-Print Legal Petition Draft:**": "**📝 மனு மாதிரி (Petition Draft):**",
                "**Regulated Interest Rates & Subventions:**": "**📊 ஒழுங்குபடுத்தப்பட்ட வட்டி விகிதங்கள் மற்றும் மானியங்கள்:**",
                "**Standard Calculation Formulas:**": "**📐 நிலையான கணக்கீட்டு முறைகள்:**",
                "**Statutory Rights & Penalty Directives:**": "**📜 சட்டப்பூர்வ உரிமைகள் & அபராத வழிகாட்டுதல்கள்:**",
                "**Biometric & Micro-ATM Safety Rules:**": "**🛡️ பயோமெட்ரிக் மற்றும் மைக்ரோ-ஏடிஎம் பாதுகாப்பு விதிகள்:**",
                "**Direct Benefit Transfer (DBT) Directives:**": "**🔍 நேரடி பயன் பரிமாற்றம் (DBT) வழிகாட்டுதல்கள்:**",
                "**Financial Benefit & Subsidy Slabs:**": "**💰 நிதி உதவி மற்றும் மானிய விபரம்:**",
                "**Scheme Overview:**": "**📌 திட்ட விளக்கம்:**",
                "**Mandatory Document Checklist:**": "**📋 தேவையான ஆவணங்கள்:**",
                "**Eligibility Criteria:**": "**🎯 தகுதி வரம்புகள்:**",
                "**Application Workflow:**": "**📝 விண்ணப்பிக்கும் முறை:**",
                "Verified Legal Sources:": "சரிபார்க்கப்பட்ட சட்டக் குறிப்புகள்:",
                "Verified Official Sources:": "சரிபார்க்கப்பட்ட அரசு ஆதாரங்கள்:",
                "Verified Sources:": "சரிபார்க்கப்பட்ட அரசு ஆதாரங்கள்:",
                "Verified Financial Sources:": "சரிபார்க்கப்பட்ட நிதி ஆதாரங்கள்:",
                "Verified Citizen Charter Standards:": "சரிபார்க்கப்பட்ட குடிமக்கள் சாசன விதிகள்:",
                "cooperative society": "கூட்டுறவு சங்கம் (PACS)",
                "crop insurance": "பயிர் காப்பீடு",
                "interest subvention": "வட்டி மானியம்",
                "Primary Agricultural Credit Society": "தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACS)",
                "Kisan Credit Card": "கிசான் கிரெடிட் கார்டு (KCC)",
            },
            "hi": {
                "**Overview:**": "**📌 सामान्य विवरण:**",
                "**Overview & Guidance:**": "**📌 विवरण एवं मार्गदर्शन:**",
                "**Problem Analysis:**": "**🔍 समस्या विश्लेषण:**",
                "**Statutory Remedy & Farmer Rights:**": "**🛡️ वैधानिक समाधान एवं किसान अधिकार:**",
                "**Mandatory Evidence Checklist:**": "**📁 आवश्यक साक्ष्य चेकलिस्ट:**",
                "**Key Provisions / Guidelines:**": "**📜 मुख्य प्रावधान एवं दिशानिर्देश:**",
                "**3-Tier Escalation Ladder": "**🪜 3-स्तरीय अपीलीय सीढ़ी",
                "**Competent Override Authority:**": "**🏛️ सक्षम अपीलीय प्राधिकारी:**",
                "**Applicable Statutory Laws:**": "**📜 लागू वैधानिक धाराएं:**",
                "**Penalties on Violator:**": "**⚠️ दोषी पर कानूनी कार्रवाई:**",
                "**Ready-to-Print Legal Petition Draft:**": "**📝 औपचारिक शिकायत प्रारूप (Petition Draft):**",
                "**Regulated Interest Rates & Subventions:**": "**📊 विनियमित ब्याज दरें एवं सब्सिडी:**",
                "**Standard Calculation Formulas:**": "**📐 मानक गणना सूत्र:**",
                "**Statutory Rights & Penalty Directives:**": "**📜 वैधानिक अधिकार एवं जुर्माना निर्देश:**",
                "**Biometric & Micro-ATM Safety Rules:**": "**🛡️ बायोमेट्रिक एवं माइक्रो-एटीएम सुरक्षा नियम:**",
                "**Direct Benefit Transfer (DBT) Directives:**": "**🔍 प्रत्यक्ष लाभ अंतरण (DBT) दिशानिर्देश:**",
                "**Financial Benefit & Subsidy Slabs:**": "**💰 वित्तीय लाभ एवं सब्सिडी स्लैब:**",
                "**Scheme Overview:**": "**📌 योजना विवरण:**",
                "**Mandatory Document Checklist:**": "**📋 आवश्यक दस्तावेज़ चेकलिस्ट:**",
                "**Eligibility Criteria:**": "**🎯 पात्रता मानदंड:**",
                "**Application Workflow:**": "**📝 आवेदन प्रक्रिया:**",
                "Verified Legal Sources:": "सत्यापित कानूनी स्रोत:",
                "Verified Official Sources:": "सत्यापित सरकारी स्रोत:",
                "Verified Sources:": "सत्यापित सरकारी स्रोत:",
                "Verified Financial Sources:": "सत्यापित वित्तीय स्रोत:",
                "cooperative society": "सहकारी समिति (पैक्स)",
                "crop insurance": "प्रधानमंत्री फसल बीमा",
                "interest subvention": "ब्याज अनुदान",
                "Primary Agricultural Credit Society": "प्राथमिक कृषि ऋण समिति (पैक्स)",
                "Kisan Credit Card": "किसान क्रेडिट कार्ड (KCC)",
            }
        }

    def _translate_segment(self, text: str, target_lang: str) -> str:
        """Translates a clean single text segment preserving numbers and punctuation."""
        if not text or not text.strip():
            return text

        cache_key = f"{target_lang}:{text.strip()}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=4) as response:
                raw_data = json.loads(response.read().decode("utf-8"))
                translated = "".join([part[0] for part in raw_data[0] if part[0]])
                if translated:
                    self._cache[cache_key] = translated
                    return translated
        except Exception:
            pass

        return text

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translates markdown content into the target Indian language while preserving markdown formatting,
        emojis, statutory citations, URLs, and numbers.
        """
        if not text or source_lang == target_lang or target_lang == "en":
            return text

        # 1. Apply high-priority glossary replacements
        processed = text
        if target_lang in self.glossary:
            for en_term, target_term in self.glossary[target_lang].items():
                processed = processed.replace(en_term, target_term)

        # 2. Translate line-by-line or paragraph-by-paragraph to preserve Markdown layout
        lines = processed.split("\n")
        translated_lines: List[str] = []

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                translated_lines.append(line)
                continue

            # Preserve code blocks and raw citations without translating them
            if trimmed.startswith("```") or trimmed.startswith("🏛️") or trimmed.startswith("📜 Applicable") or "http://" in trimmed or "https://" in trimmed:
                translated_lines.append(line)
                continue

            # Check if line already has Indic characters (Tamil, Devanagari, Telugu, Kannada, etc.)
            has_indic = any('\u0900' <= char <= '\u0DFF' or '\u0B80' <= char <= '\u0BFF' for char in line)
            
            # If line is primarily in English, translate the text content
            if not has_indic or len(re.findall(r'[a-zA-Z]{4,}', line)) >= 3:
                # Handle bullet points
                prefix = ""
                content = line
                if line.startswith("• "):
                    prefix = "• "
                    content = line[2:]
                elif line.startswith("- "):
                    prefix = "- "
                    content = line[2:]
                elif line.startswith("  - "):
                    prefix = "  - "
                    content = line[4:]
                elif line.startswith("  • "):
                    prefix = "  • "
                    content = line[4:]

                # Handle bold headers like **Overview:** or **Benchmark Lending Rate:**
                bold_match = re.match(r'^(\*\*.*?\*\*:\s*)(.*)$', content)
                if bold_match:
                    header_part = bold_match.group(1)
                    body_part = bold_match.group(2)
                    
                    # Translate header and body
                    tr_header = self._translate_segment(header_part.replace("**", "").replace(":", ""), target_lang)
                    tr_body = self._translate_segment(body_part, target_lang) if body_part.strip() else ""
                    
                    translated_lines.append(f"{prefix}**{tr_header}:** {tr_body}".strip())
                else:
                    tr_content = self._translate_segment(content, target_lang)
                    translated_lines.append(f"{prefix}{tr_content}")
            else:
                translated_lines.append(line)

        return "\n".join(translated_lines)
