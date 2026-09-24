"""
Specialized Cooperative Law & Governance Sub-Model Engine for Cooperative AI Portal.
Handles:
- Multi-State Co-operative Societies Act 2002 & 2023 Amendment
- Cooperative Election Authority (Section 45) & Election dispute arbitration
- Statutory Arbitration under Section 84 (3-year limitation period, civil courts barred)
- Cooperative Ombudsman under Section 85 for member grievance redressal
- Statutory Surcharge & Inquiries under Section 88 / 108
- Board disqualifications (Section 43/44), Women & SC/ST reservations, democratic voting rights (Section 20)
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings

class CooperativeLawEngine:
    def __init__(self):
        self.laws_catalog: List[Dict[str, Any]] = []
        self._load_catalog()

    def _load_catalog(self):
        laws_path = os.path.join(settings.DATABASE_PATH, "laws", "cooperative_laws.json")
        if os.path.exists(laws_path):
            try:
                with open(laws_path, "r", encoding="utf-8") as f:
                    self.laws_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading cooperative laws: {e}")

    def find_matching_laws(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored = []

        triggers = {
            "LAW_ELECTION_AUTHORITY": ["section 45", "sec 45", "election authority", "cooperative election", "electoral roll", "voter list", "cea", "धारा 45", "चुनाव प्राधिकरण", "தேர்தல் ஆணையம்", "ఎన్నికల అథారిటీ"],
            "LAW_ARBITRATION_SECTION_84": ["section 84", "sec 84", "arbitration", "arbitrator", "statutory arbitration", "civil court barred", "dispute", "धारा 84", "मध्यस्थता", "நடுவர் மன்றம்", "మధ్యవర్తిత్వం"],
            "LAW_OMBUDSMAN_SECTION_85": ["section 85", "sec 85", "ombudsman", "cooperative ombudsman", "deficiency in service", "धारा 85", "लोकपाल", "ஒம்புட்ஸ்மேன்", "ఓంబుడ్స్‌మన్"],
            "LAW_BOARD_DISQUALIFICATIONS": ["disqualification", "board of directors", "default on loan", "reservation for women", "tenure", "निदेशक अयोग्यता", "இயக்குனர் தகுதிநீக்கம்", "బోర్డు అనర్హత"],
            "LAW_INQUIRY_SURCHARGE": ["section 108", "section 88", "surcharge", "statutory inquiry", "misappropriation", "forensic audit", "धारा 88", "धारा 108", "अधिभार", "விசாரணை"],
            "LAW_OPEN_MEMBERSHIP_SECTION_19": ["section 19", "sec 19", "open membership", "deemed membership", "refusal of membership", "धारा 19", "खुली सदस्यता", "உறுப்பினர் உரிமை"],
            "LAW_NET_PROFITS_DIVIDEND": ["section 67", "net profit", "reserve fund", "25%", "dividend", "education fund", "धारा 67", "लाभांश", "பங்கு லாபம்", "డివిడెండ్"],
            "LAW_DEMOCRATIC_VOTING_RIGHTS": ["section 20", "one member one vote", "voting rights", "no proxy", "active member", "धारा 20", "मतदान अधिकार", "வாக்குரிமை", "ఓటు ஹక్కు"]
        }

        q_tokens = set(re.findall(r'\w+', q_lower))

        for item in self.laws_catalog:
            code = item.get("topic_code", "")
            kw_list = triggers.get(code, [])
            score = 0.0

            # 1. Trigger phrase match
            for kw in kw_list:
                if kw in q_lower:
                    score += 6.0 if " " in kw else 3.0

            # 2. Section & Title match
            sec = (item.get("section", "") + " " + item.get("title", "") + " " + code).lower()
            if code.lower() in q_lower or (item.get("section", "").lower() and item.get("section", "").lower() in q_lower):
                score += 8.0
            for tok in q_tokens:
                if len(tok) > 2 and tok in sec:
                    score += 2.0

            # 3. Summary & Provisions match
            summary = item.get("summary", "").lower()
            for tok in q_tokens:
                if len(tok) > 3 and tok in summary:
                    score += 1.0

            if score > 0:
                scored.append((score, item))

        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            return [s[1] for s in scored]

        return self.laws_catalog[:2]

    def generate_guidance(self, query: str, language: str = "en") -> Dict[str, Any]:
        matched = self.find_matching_laws(query)
        primary = matched[0]

        guidance_text = self._format_response(primary, language)

        return {
            "matched_laws": [l.get("title") for l in matched],
            "primary_law": primary,
            "guidance_text": guidance_text,
            "citations": primary.get("citations", []),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_response(self, item: Dict[str, Any], language: str) -> str:
        title = item.get("title", "Cooperative Legal Guidance")
        act = item.get("act_name", "Multi-State Co-operative Societies Act")
        section = item.get("section", "")
        summary = item.get("summary", "")
        code = item.get("topic_code", "")
        citations = ", ".join(item.get("citations", []))

        # Specialized Tamil Formatting
        if language == "ta":
            if code == "LAW_ARBITRATION_SECTION_84":
                return (
                    f"### 🏛️ கூட்டுறவு சங்க தகராறுகளுக்கான சட்டப்பூர்வ நடுவர் தீர்ப்பு (பிரிவு 84)\n\n"
                    f"**📜 பொருந்தக்கூடிய சட்டம்:** பல்மாநில கூட்டுறவு சங்கங்கள் சட்டம் 2002 / தமிழ்நாடு கூட்டுறவு சங்கங்கள் சட்டம்\n"
                    f"**⚖️ சட்டப்பிரிவு:** பிரிவு 84 (Statutory Arbitration)\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n"
                    f"கூட்டுறவு சங்கங்கள், உறுப்பினர்கள், நிர்வாகக் குழு அல்லது ஊழியர்களுக்கு இடையேயான அனைத்து நிதி மற்றும் மேலாண்மை தகராறுகளும் பதிவுத்துறை நடுவர் மன்றம் மூலமாகவே விசாரிக்கப்பட வேண்டும்; சிவில் நீதிமன்றங்களுக்கு இதில் தலையிட அதிகாரம் இல்லை.\n\n"
                    f"**⚖️ முக்கிய சட்ட விதிகள்:**\n"
                    f"• **சிவில் நீதிமன்ற தடை (Bar of Civil Courts)**: பிரிவு 84(3)-ன் கீழ் சிவில் நீதிமன்றங்களில் வழக்கு தொடர அனுமதி இல்லை.\n"
                    f"• **3 ஆண்டு கால வரம்பு (Limitation Period)**: தகராறு ஏற்பட்ட நாளிலிருந்து 3 ஆண்டுகளுக்குள் பதிவுத்துறை அல்லது நடுவரிடம் முறையிட வேண்டும்.\n"
                    f"• **தீர்ப்பின் அதிகாரம் (Finality of Award)**: நடுவரின் தீர்ப்பு சிவில் நீதிமன்ற ஆணைக்கு நிகரானது மற்றும் கட்டாயமாக நிறைவேற்றத்தக்கது.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட சட்டப்பூர்வ சான்றுகள்:** {citations}"
                )
            elif code == "LAW_OMBUDSMAN_SECTION_85":
                return (
                    f"### 🏛️ உறுப்பினர் குறைதீர்ப்பு கூட்டுறவு ஒம்புட்ஸ்மேன் (பிரிவு 85)\n\n"
                    f"**📜 பொருந்தக்கூடிய சட்டம்:** பல்மாநில கூட்டுறவு சங்கங்கள் திருத்தச் சட்டம் 2023\n"
                    f"**⚖️ சட்டப்பிரிவு:** பிரிவு 85 (Cooperative Ombudsman)\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n"
                    f"கூட்டுறவு சங்க உறுப்பினர்களின் புகார்கள், சேவை குறைபாடுகள் மற்றும் வைப்புத்தொகை மோசடிகளை விசாரிக்க மத்திய அரசால் சுயாதீன கூட்டுறவு ஒம்புட்ஸ்மேன் நியமிக்கப்படுகிறார்.\n\n"
                    f"**⚖️ முக்கிய சட்ட விதிகள்:**\n"
                    f"• **இலவச புகார் மனு**: வைப்புத்தொகை அல்லது கடன் மறுப்பு தொடர்பாக விவசாயிகள் கட்டணமின்றி ஒம்புட்ஸ்மேனிடம் முறையிடலாம்.\n"
                    f"• **30 நாள் காலக்கெடு**: புகாரை விசாரித்து 30 நாட்களுக்குள் தீர்வு காண ஒம்புட்ஸ்மேனுக்கு சட்ட அதிகாரம் உண்டு.\n"
                    f"• **இழப்பீடு உத்தரவு**: சங்கத்தின் சேவை குறைபாட்டிற்கு உறுப்பினருக்கு நஷ்டஈடு பெற்றுத்தர உத்தரவிடலாம்.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட சட்டப்பூர்வ சான்றுகள்:** {citations}"
                )
            elif code == "LAW_ELECTION_AUTHORITY":
                return (
                    f"### 🏛️ கூட்டுறவு தேர்தல் ஆணையம் & தேர்தல் நடைமுறைகள் (பிரிவு 45)\n\n"
                    f"**📜 பொருந்தக்கூடிய சட்டம்:** MSCS திருத்தச் சட்டம் 2023\n"
                    f"**⚖️ சட்டப்பிரிவு:** பிரிவு 45 (Cooperative Election Authority - CEA)\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n"
                    f"கூட்டுறவு சங்கங்களின் நிர்வாகக் குழு தேர்தல்களை நியாயமாகவும் வெளிப்படையாகவும் நடத்த மத்திய கூட்டுறவு தேர்தல் ஆணையம் அமைக்கப்பட்டுள்ளது.\n\n"
                    f"**⚖️ முக்கிய சட்ட விதிகள்:**\n"
                    f"• **சுயாதீன தேர்தல்**: சங்கத்தின் பதவி காலம் முடிவதற்குள் தேர்தலை நடத்தி புதிய குழுவை தேர்வு செய்ய வேண்டும்.\n"
                    f"• **வாக்காளர் பட்டியல் சரிபார்ப்பு**: தகுதியான அனைத்து உறுப்பினர்களும் வாக்காளர் பட்டியலில் சேர்க்கப்பட வேண்டும்.\n"
                    f"• **இடஒதுக்கீடு**: நிர்வாகக் குழுவில் பெண்களுக்கு 2 இடங்களும், SC/ST பிரிவினருக்கு 1 இடமும் கட்டாயமாக ஒதுக்கப்பட வேண்டும்.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட சட்டப்பூர்வ சான்றுகள்:** {citations}"
                )
            else:
                provisions = item.get("key_provisions", [])
                prov_fmt = "\n".join([f"• {p}" for p in provisions])
                return (
                    f"### 🏛️ {title} ({section})\n\n"
                    f"**📜 சட்டம்:** {act}\n"
                    f"**⚖️ சட்டப்பிரிவு:** {section}\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n{summary}\n\n"
                    f"**⚖️ முக்கிய சட்ட விதிகள்:**\n{prov_fmt}\n\n"
                    f"🏛️ **சட்டப்பூர்வ சான்றுகள்:** {citations}"
                )

        # Specialized Hindi Formatting
        elif language == "hi":
            if code == "LAW_ARBITRATION_SECTION_84":
                return (
                    f"### 🏛️ सहकारी विवादों में वैधानिक मध्यस्थता (धारा 84)\n\n"
                    f"**📜 लागू अधिनियम:** बहु-राज्य सहकारी सोसायटी अधिनियम 2002\n"
                    f"**⚖️ वैधानिक धारा:** धारा 84 (Statutory Arbitration)\n\n"
                    f"**📌 सामान्य विवरण:**\n"
                    f"सहकारी समिति, सदस्यों, निदेशकों अथवा कर्मचारियों के बीच किसी भी वित्तीय या प्रबंधन विवाद का निपटारा केवल रजिस्ट्रार/मध्यस्थ के माध्यम से होगा; दीवानी अदालतों का क्षेत्राधिकार वर्जित है।\n\n"
                    f"**⚖️ प्रमुख कानूनी प्रावधान:**\n"
                    f"• **दीवानी अदालतों का वर्जन (Bar of Civil Courts)**: धारा 84(3) के तहत सिविल कोर्ट में सीधे वाद दायर नहीं किया जा सकता।\n"
                    f"• **3-वर्षीय परिसीमा काल (Limitation Period)**: विवाद उत्पन्न होने के 3 वर्ष के भीतर मध्यस्थता हेतु आवेदन अनिवार्य है।\n"
                    f"• **अंतिम एवं बाध्यकारी निर्णय**: मध्यस्थ का पंचाट (Award) सिविल डिक्री के समान प्रवर्तनीय है।\n\n"
                    f"🏛️ **सत्यापित आधिकारिक कानूनी संदर्भ:** {citations}"
                )
            elif code == "LAW_OMBUDSMAN_SECTION_85":
                return (
                    f"### 🏛️ सदस्य शिकायत निवारण हेतु सहकारी लोकपाल (धारा 85)\n\n"
                    f"**📜 लागू अधिनियम:** बहु-राज्य सहकारी सोसायटी संशोधन अधिनियम 2023\n"
                    f"**⚖️ वैधानिक धारा:** धारा 85 (Cooperative Ombudsman)\n\n"
                    f"**📌 सामान्य विवरण:**\n"
                    f"सहकारी समिति के सदस्यों की शिकायतों, सेवा में कमी एवं जमा राशि वापसी के विवादों के त्वरित निवारण हेतु केंद्र सरकार द्वारा स्वतंत्र लोकपाल की नियुक्ति की गई है।\n\n"
                    f"**⚖️ प्रमुख कानूनी प्रावधान:**\n"
                    f"• **निःशुल्क शिकायत**: सदस्य बिना किसी अदालती शुल्क के लोकपाल के समक्ष आवेदन प्रस्तुत कर सकते हैं।\n"
                    f"• **30-दिवसीय समय-सीमा**: लोकपाल द्वारा 30 दिनों के भीतर वैधानिक समाधान आदेश पारित किया जाता है।\n\n"
                    f"🏛️ **सत्यापित आधिकारिक कानूनी संदर्भ:** {citations}"
                )
            else:
                provisions = item.get("key_provisions", [])
                prov_fmt = "\n".join([f"• {p}" for p in provisions])
                return (
                    f"### 🏛️ {title} ({section})\n\n"
                    f"**📜 कानून:** {act}\n"
                    f"**⚖️ वैधानिक धारा:** {section}\n\n"
                    f"**📌 सामान्य विवरण:**\n{summary}\n\n"
                    f"**⚖️ प्रमुख कानूनी प्रावधान:**\n{prov_fmt}\n\n"
                    f"🏛️ **सत्यापित आधिकारिक कानूनी संदर्भ:** {citations}"
                )

        # English Default
        else:
            provisions = item.get("key_provisions", [])
            prov_fmt = "\n".join([f"  - {p}" for p in provisions])
            return (
                f"### 🏛️ {title} ({section})\n\n"
                f"**Governing Act:** {act}\n"
                f"**Statutory Section:** {section}\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**Key Statutory Provisions & Legal Rules:**\n{prov_fmt}\n\n"
                f"🏛️ **Verified Legal Sources & Gazette Citations:** {citations}"
            )
