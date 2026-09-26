"""
Specialized PACS & PMFBY Crop Insurance Sub-Model Engine for Cooperative AI Portal.
Handles:
- PMFBY 72-Hour Calamity Intimation workflows & intimation channel routing
- PMFBY Standardized Premium Calculations (2% Kharif, 1.5% Rabi, 5% Commercial)
- PMFBY Clause 17.2 & 21.5 Bank Default Liability & DGRC dispute escalation
- PACS Model Bye-laws 25+ Diversified Economic Activities (Custom Hiring, Drones, CSC, Jan Aushadhi)
- PACS Membership rules, Deemed Membership, and 15-Day Loan Processing SLAs
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings
from ai_engine.language.translation import TranslationEngine

class PacsPmfbyEngine:
    def __init__(self):
        self.pacs_catalog: List[Dict[str, Any]] = []
        self.pmfby_catalog: List[Dict[str, Any]] = []
        self.translator = TranslationEngine()
        self._load_catalogs()

    def _load_catalogs(self):
        pacs_path = os.path.join(settings.DATABASE_PATH, "pacs", "pacs_bylaws.json")
        if os.path.exists(pacs_path):
            try:
                with open(pacs_path, "r", encoding="utf-8") as f:
                    self.pacs_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading pacs bylaws: {e}")

        pmfby_path = os.path.join(settings.DATABASE_PATH, "pmfby", "pmfby_guidelines.json")
        if os.path.exists(pmfby_path):
            try:
                with open(pmfby_path, "r", encoding="utf-8") as f:
                    self.pmfby_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading pmfby guidelines: {e}")

    def find_matching_topics(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored = []

        all_items = self.pacs_catalog + self.pmfby_catalog

        triggers = {
            "PACS_DEFINITION_STRUCTURE": ["structure of pacs", "what is pacs", "primary agricultural credit society", "3-tier", "dccb", "stcb", "short-term cooperative credit", "पैक्स क्या है", "கூட்டுறவு அமைப்பு", "పాక్స్ నిర్మాణం"],
            "PACS_MODEL_BYLAWS_25_ACTIVITIES": ["commercial and agricultural services", "model bye-laws", "model bylaws", "25+ activities", "25+", "diversified", "pacs operate", "multi-purpose pacs", "m-pacs", "उप-नियम", "பன்முக சேவைகள்"],
            "PACS_MEMBERSHIP_RULES": ["membership types", "regular member", "nominal member", "share capital", "open membership", "open membership rules", "pacs membership", "member registration", "membership documents", "membership application", "how to join pacs", "enrollment", "new membership", "सदस्यता नियम", "உறுப்பினர் விதிகள்", "உறுப்பினர் சேர்க்கை", "உறுப்பினர் சேர்க்கைக்கு", "புதிய உறுப்பினர்", "சேர்க்கை", "ஆவணங்கள்", "விண்ணப்பிக்க", "விண்ணப்பம்", "பதிவு செய்ய", "சభ్యత్వ నిబంధనలు"],
            "PACS_LOAN_DISPOSAL_SLA": ["statutory time limit", "approve loan", "15-day", "15 days loan", "loan disposal", "loan sla", "citizen charter", "form-b", "15 दिन लोन", "கடன் காலக்கெடு", "రుణం గడువు"],
            "PACS_CUSTOM_HIRING_DRONES": ["rent tractors", "kisan drones", "custom hiring centres", "custom hiring", "chc", "tractor rental", "drone spraying", "drone rental", "chc machinery", "कस्टम हायरिंग", "ड्रोन छिड़काव", "किसान ड्रोन", "டிரோன் தெளிப்பான்"],
            "PACS_CSC_DIGITAL_SERVICES": ["csc in pacs", "common service centre", "common service center", "300+ services", "digital village", "ekyc pacs", "aadhaar pacs", "सीएससी", "இ-சேவை", "డిజిటల్ సేవలు"],
            "PACS_COMPUTERIZATION_ERP": ["pacs computerization", "erp", "cloud erp", "nabard erp", "software", "कंप्यूटरीकरण", "கணினிமயமாக்கல்"],
            "PACS_PETROL_LPG_DEALERSHIP": ["petrol", "diesel", "lpg", "dealership", "pump"],
            "PACS_SOLAR_KUSUM_C": ["solar", "feeder solarization", "kusum component c"],
            "PACS_GOVERNANCE_AUDIT": ["managing committee", "board of directors", "reservation for women", "annual audit", "agm", "statutory audit", "प्रबंध समिति", "தணிக்கை", "ఆడిట్"],
            "AADHAAR_UPDATE_NAME_ADDRESS_CSC": ["change my name", "change name", "change address", "update address", "aadhar card", "aadhaar card", "aadhaar name", "aadhaar address", "aadhaar update", "whom i need to meet", "where i can go", "aadhar", "aadhaar", "correction in aadhar", "aadhar correction", "आधार कार्ड", "नाम बदलना", "पता बदलना", "आधार सुधार", "ஆதார் கார்டு", "ஆதார் பெயர் மாற்றம்", "முகவரி மாற்றம்", "ஆதார் திருத்தம்", "ஆதார் அட்டை", "ఆధార్ కార్డు", "పేరు మార్పు", "చిరునామా మార్పు"],
            "PMFBY_72H_LOCALIZED_CALAMITY": ["72 hours", "72 hour", "72h", "hailstorm", "flood", "inundation", "landslide", "cloudburst", "post-harvest", "cut and spread", "calamity", "heavy rain", "heavy rains", "heavy rainfall", "rain", "rains", "rainfall", "crop loss", "crops lost", "crop damage", "crops damaged", "crops destroyed", "crop destroyed", "crops got desteroyed", "desteroyed", "destroy", "ruined crop", "ruined crops", "flood damage", "rain damage", "excess rain", "72 घंटे", "ओलावृष्टि", "बाढ़", "जलभराव", "72 மணி நேரம்", "ஆலங்கட்டி மழை", "வெள்ளம்", "மழை", "பயிர் சேதம்", "பயிர் அழிந்தது", "72 గంటలు", "వడగళ్ళు", "వరదలు", "వర్షం", "72 तास", "गारपीट", "पाऊस"],
            "PMFBY_72H_CALAMITY_INTIMATION": ["72 hours", "72 hour", "72h", "hailstorm", "flood", "inundation", "landslide", "cloudburst", "post-harvest", "cut and spread", "calamity", "heavy rain", "heavy rains", "heavy rainfall", "rain", "rains", "rainfall", "crop loss", "crops lost", "crop damage", "crops damaged", "crops destroyed", "crop destroyed", "crops got desteroyed", "desteroyed", "destroy", "ruined crop", "ruined crops", "flood damage", "rain damage", "excess rain", "72 घंटे", "ओलावृष्टि", "बाढ़", "जलभराव", "72 மணி நேரம்", "ஆலங்கட்டி மழை", "வெள்ளம்", "மழை", "பயிர் சேதம்", "பயிர் அழிந்தது", "72 గంటలు", "వడగళ్ళు", "వరదలు", "వర్షం", "72 तास", "गारपीट", "पाऊस"],
            "PMFBY_PREMIUM_RATES": ["premium percentage", "kharif, rabi and commercial", "kharif premium", "rabi premium", "2%", "1.5%", "5%", "sum insured", "non-loanee", "loanee", "प्रीमियम", "खरीफ", "रबी", "कாப்பீட்டு கட்டணம்", "பயிர் காப்பீட்டு பிரீமியம்", "பிரிமீயம்", "ప్రీమియం", "पिक विमा हप्ता", "विमा", "फसल विमा", "पीक विमा", "crop insurance example", "विमा म्हणजे"],
            "PMFBY_CORE_PREMIUM_RATES": ["premium percentage", "kharif, rabi and commercial", "kharif premium", "rabi premium", "2%", "1.5%", "5%", "sum insured", "non-loanee", "loanee"],
            "PMFBY_BANK_DEFAULT_CLAUSE": ["failed to upload", "ncip portal", "cut-off date", "who pays my loss", "pacs deducted pmfby", "clause 17.2", "bank default", "pacs did not pay premium", "premium not uploaded", "data not found", "बैंक की गलती", "प्रीमियम जमा नहीं किया", "வங்கி பொறுப்பு", "బ్యాంక్ డిఫాల్ట్"],
            "PMFBY_YIELD_CALCULATION_TECH": ["cce", "crop cutting", "yield calculation", "threshold yield", "yes-tech", "winds", "फसल कटाई प्रयोग", "விளைச்சல் மதிப்பீடு", "దిగుబడి నష్టం"],
            "PMFBY_YES_TECH_AND_WINDS": ["yes-tech", "winds", "cropic", "remote sensing", "satellite", "aws"],
            "PMFBY_POST_HARVEST_COVER": ["post-harvest", "post harvest", "14 days", "cut and spread", "cyclone"]
        }

        q_tokens = set(re.findall(r'\w+', q_lower))

        for item in all_items:
            code = item.get("topic_code", "")
            kw_list = triggers.get(code, [])
            score = 0.0

            # 1. Trigger phrase match
            for kw in kw_list:
                if kw in q_lower:
                    score += 6.0 if " " in kw else 3.0

            # 2. Topic title & code match
            title = (item.get("title", "") + " " + code).lower()
            if code.lower() in q_lower:
                score += 8.0
            for tok in q_tokens:
                if len(tok) > 2 and tok in title:
                    score += 2.0

            # 3. Summary & Provisions match
            summary = item.get("summary", "").lower()
            for tok in q_tokens:
                if len(tok) > 3 and tok in summary:
                    score += 1.0

            # 4. Mandatory rules / details match
            for field in ["mandatory_72h_rule", "membership_rules", "sla_disposal_rule", "default_clause", "authorized_centers"]:
                if field in item and any(tok in str(item[field]).lower() for tok in q_tokens if len(tok) > 3):
                    score += 2.0

            if score > 0:
                scored.append((score, item))

        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            return [s[1] for s in scored]

        return []

    def generate_guidance(self, query: str, language: str = "en") -> Dict[str, Any]:
        matched = self.find_matching_topics(query)
        if not matched:
            return {
                "matched_topics": [],
                "primary_topic": {},
                "guidance_text": "",
                "citations": [],
                "is_verified": True,
                "trust_score": 0.0
            }

        primary = matched[0]

        guidance_text = self._format_response(primary, language)
        if language not in ("en", "ta", "hi"):
            guidance_text = self.translator.translate(guidance_text, "en", language)

        return {
            "matched_topics": [t.get("title") for t in matched],
            "primary_topic": primary,
            "guidance_text": guidance_text,
            "citations": primary.get("citations", []),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_response(self, item: Dict[str, Any], language: str) -> str:
        title = item.get("title", "PACS & PMFBY Advisory")
        code = item.get("topic_code", "")
        summary = item.get("summary", "")
        citations = ", ".join(item.get("citations", []))

        # Check for Aadhaar Update (PACS-11)
        if code in ["AADHAAR_UPDATE_NAME_ADDRESS_CSC", "PACS-11"] or "authorized_centers" in item:
            if language == "ta":
                return (
                    "### 🪪 ஆதார் அட்டையில் பெயர் மற்றும் முகவரி மாற்றம் செய்யும் நடைமுறை & வழிகாட்டுதல்\n\n"
                    "**📌 பொதுவான விளக்கம்:**\n"
                    "ஆதார் அட்டையில் **பெயர்** மற்றும் **முகவரி** இரண்டையும் மாற்றுவதற்கு, அங்கீகரிக்கப்பட்ட **ஆதார் சேவை மையம் (Aadhaar Seva Kendra - ASK)**, **அஞ்சலகம் / வங்கி ஆதார் மையம்** அல்லது உங்கள் பகுதியிலுள்ள **தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்க (PACS) இ-சேவை மையத்திற்கு (CSC / E-Sevai)** நேரில் செல்ல வேண்டும்.\n\n"
                    "> 💡 **முக்கிய குறிப்பு**: முகவரியை மட்டும் ஆன்லைனில் மாற்றிக்கொள்ளலாம்; ஆனால் **பெயர் மாற்றம் செய்வதற்கு பயோமெட்ரிக் (கைரேகை / கருவிழி ஸ்கேன்) சரிபார்ப்பு கட்டாயம்** என்பதால் ஆதார் மையத்திற்கு நேரில் செல்ல வேண்டும்.\n\n"
                    "**🏢 1. எங்கு செல்ல வேண்டும்?**\n"
                    "• **UIDAI நேரடி ஆதார் சேவை மையங்கள் (ASK)**.\n"
                    "• **கிராம அளவிலான PACS இ-சேவை மையங்கள் (CSC / E-Sevai Centers)**: மத்திய கூட்டுறவு அமைச்சகத்தின் கீழ் கிராமங்களில் செயல்படும் பொது சேவை மையங்கள்.\n"
                    "• **தலைமை அஞ்சலகங்கள் மற்றும் தேசியமயமாக்கப்பட்ட வங்கிக் கிளைகளின் ஆதார் மையங்கள்**.\n\n"
                    "**👤 2. யாரை சந்திக்க வேண்டும்?**\n"
                    "• **ஆவண சரிபார்ப்பு அலுவலர் (The Verifier)**: உங்கள் அசல் ஆவணங்களை (Original Documents) சரிபார்த்து டோக்கன் வழங்கும் அரசு அதிகாரி.\n"
                    "• **ஆதார் கணினி ஆபரேட்டர் (Aadhaar Operator)**: புதிய பெயர், முகவரியை UIDAI மென்பொருளில் பதிவேற்றம் செய்து, பயோமெட்ரிக் சரிபார்ப்பு செய்து ரசீது வழங்கும் தொழில்நுட்ப அலுவலர்.\n\n"
                    "**📝 3. தேவையான ஆவணங்கள் மற்றும் படிநிலைகள்:**\n"
                    "• **படி 1: அசல் ஆவணங்களை எடுத்துச் செல்லுதல்** (ஜெராக்ஸ் ஏற்றுக்கொள்ளப்படாது):\n"
                    "  - **பெயர் மாற்றத்திற்கு (அடையாளச் சான்று - PoI)**: பாஸ்போர்ட், பான் கார்டு (PAN), வாக்காளர் அடையாள அட்டை, ஓட்டுநர் உரிமம் அல்லது அரசாணை (Gazette Notification).\n"
                    "  - **முகவரி மாற்றத்திற்கு (முகவரிச் சான்று - PoA)**: வங்கி பாஸ்புக், மின்கட்டண ரசீது (3 மாதங்களுக்குள்), குடும்ப அட்டை (Ration Card), வாக்காளர் அட்டை அல்லது பதிவு செய்யப்பட்ட வாடகை ஒப்பந்தம்.\n"
                    "• **படி 2: டோக்கன் / முன்பதிவு**: `myaadhaar.uidai.gov.in` இணையதளத்தில் முன்பதிவு செய்யலாம் அல்லது நேரடியாகச் சென்று டோக்கன் பெறலாம்.\n"
                    "• **படி 3: விண்ணப்பப் படிவம்**: ஆதார் திருத்தப் படிவத்தைப் பூர்த்தி செய்து வழங்கவும்.\n"
                    "• **படி 4: கட்டணம் மற்றும் பயோமெட்ரிக்**: கைரேகை பதிவு செய்யப்பட்டு, நிர்ணயிக்கப்பட்ட அரசு கட்டணமாக **ரூ. 50 முதல் ரூ. 75** செலுத்த வேண்டும்.\n"
                    "• **படி 5: ரசீது பெறுதல்**: **URN எண் (Update Request Number)** அடங்கிய ஒப்புகைச் சீட்டைப் பெற்றுக்கொள்ளவும். இதன் மூலம் ஆன்லைனில் நிலையை அறியலாம்.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட அரசு ஆதாரங்கள்:** {citations}"
                )
            elif language == "hi":
                return (
                    "### 🪪 आधार कार्ड में नाम एवं पता बदलने की प्रक्रिया एवं मार्गदर्शन\n\n"
                    "**📌 सामान्य विवरण:**\n"
                    "आधार कार्ड में **नाम** और **पता** दोनों बदलने के लिए आपको किसी अधिकृत **आधार सेवा केंद्र (Aadhaar Seva Kendra - ASK)**, **बैंक / डाकघर आधार केंद्र** या नजदीकी **पैक्स सीएससी केंद्र (PACS CSC / E-Seva)** पर जाना होगा।\n\n"
                    "> 💡 **महत्वपूर्ण नियम**: केवल पता ऑनलाइन बदला जा सकता है, लेकिन **नाम बदलने के लिए बायोमेट्रिक प्रमाणीकरण (फिंगरप्रिंट/आइरिस) अनिवार्य है**, इसलिए केंद्र पर व्यक्तिगत रूप से जाना आवश्यक है।\n\n"
                    "**🏢 1. आप कहाँ जा सकते हैं?**\n"
                    "• **UIDAI आधार सेवा केंद्र (ASK)**.\n"
                    "• **ग्राम पंचायत पैक्स कॉमन सर्विस सेंटर (PACS CSC / E-Seva)**.\n"
                    "• **डाकघर एवं राष्ट्रीयकृत बैंकों के स्थायी आधार काउंटर**.\n\n"
                    "**👤 2. आपको किससे मिलना होगा?**\n"
                    "• **दस्तावेज़ सत्यापनकर्ता (The Verifier)**: आपके मूल पहचान एवं पते के प्रमाणों की जांच करने वाले अधिकृत अधिकारी।\n"
                    "• **आधार ऑपरेटर (Aadhaar Operator)**: कंप्यूटर टर्मिनल पर विवरण दर्ज करने, बायोमेट्रिक लेने और पावती पर्ची जारी करने वाले तकनीकी अधिकारी।\n\n"
                    "**📝 3. आवश्यक दस्तावेज़ एवं चरण:**\n"
                    "• **चरण 1: मूल दस्तावेज़ साथ लाएं** (फोटोकॉपी मान्य नहीं):\n"
                    "  - **नाम बदलने के लिए (पहचान प्रमाण - PoI)**: पासपोर्ट, पैन कार्ड, वोटर आईडी, ड्राइविंग लाइसेंस या सरकारी गजट।\n"
                    "  - **पता बदलने के लिए (पता प्रमाण - PoA)**: बैंक पासबुक, बिजली बिल, राशन कार्ड, वोटर आईडी या रेंट एग्रीमेंट।\n"
                    "• **चरण 2: अपॉइंटमेंट / टोकन**: `myaadhaar.uidai.gov.in` पर समय बुक करें या सीधे टोकन लें।\n"
                    "• **चरण 3: फॉर्म भरें**: आधार सुधार फॉर्म भरें।\n"
                    "• **चरण 4: बायोमेट्रिक एवं शुल्क**: निर्धारित शुल्क **₹50 से ₹75** जमा करें और फिंगरप्रिंट दें।\n"
                    "• **चरण 5: पावती रसीद**: **URN (Update Request Number)** पर्ची संभालकर रखें, जिससे स्थिति ट्रैक की जा सके।\n\n"
                    f"🏛️ **सत्यापित आधिकारिक स्रोत:** {citations}"
                )
            else:
                return (
                    "### 🪪 Aadhaar Card Name & Address Update Procedure (AADHAAR_UPDATE_NAME_ADDRESS_CSC)\n\n"
                    "**Overview:**\n"
                    "To change both your **name** and **address** in your Aadhaar card, you must visit an authorized **Aadhaar Enrolment Centre / Aadhaar Seva Kendra (ASK)**, **Designated Post Office / Bank Branch**, or your local **PACS Common Service Centre (CSC) / E-Sevai Center**.\n\n"
                    "> 💡 **Important Distinction**: While address-only changes can be done online on the myAadhaar portal, **name changes require a physical visit** to an authorized center because mandatory biometric verification (fingerprint or iris scan) is required to authorize the name correction.\n\n"
                    "**🏢 1. Where You Can Go:**\n"
                    "• **Aadhaar Seva Kendras (ASK)**: Dedicated official centers operated directly by UIDAI.\n"
                    "• **Authorized PACS Common Service Centres (CSC) / E-Sevai Centers**: Functioning directly at the village/block level under Ministry of Cooperation initiatives.\n"
                    "• **Designated Post Offices & Nationalized Bank Counters**: Permanent Aadhaar update counters.\n\n"
                    "**👤 2. Whom You Need to Meet:**\n"
                    "• **The Verifier**: The government-authorized officer at the token/verification desk who checks your original legal documents to confirm validity.\n"
                    "• **The Aadhaar Operator**: The technical official at the computer terminal who enters the new details into UIDAI software, scans original documents, captures biometric authentication, and issues your acknowledgment slip.\n\n"
                    "**📝 3. Step-by-Step Instructions & Required Documents:**\n"
                    "• **Step 1: Gather Original Documents** (Photocopies are not accepted):\n"
                    "  - **For Name Change (Proof of Identity - PoI)**: Passport, PAN Card, Voter ID, Driving License, or Gazette Notification.\n"
                    "  - **For Address Change (Proof of Address - PoA)**: Bank Passbook/Statement with photo, Electricity Bill (within 3 months), Voter ID, Ration Card, or Registered Rent Agreement.\n"
                    "• **Step 2: Book Appointment / Walk-In**: Book a time slot on the official **UIDAI myAadhaar Portal** (`myaadhaar.uidai.gov.in`) or walk in to get a token.\n"
                    "• **Step 3: Fill Correction Form**: Complete the standard Aadhaar Enrolment/Update Form.\n"
                    "• **Step 4: Biometric Authentication & Fee**: Operator captures your biometric sign-off. The standard government fee for demographic update is **₹50 - ₹75**.\n"
                    "• **Step 5: Collect Acknowledgement Slip**: Keep the receipt containing the **Update Request Number (URN)** to track status online.\n\n"
                    f"🏛️ **Verified Official Sources:** {citations}"
                )

        # Specialized Tamil Formatting
        if language == "ta":
            if code in ["PACS_MEMBERSHIP_RULES", "PACS-03"]:
                return (
                    "### 🏛️ தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கத்தில் (PACS) உறுப்பினர் சேர்க்கை நடைமுறை & ஆவணங்கள்\n\n"
                    "**📌 பொதுவான விளக்கம்:**\n"
                    "தமிழ்நாடு கூட்டுறவுச் சங்கங்களின் சட்டம் (Section 21 & 23) மற்றும் மாதிரி துணை விதிகளின்படி, சங்கத்தின் எல்லைக்குட்பட்ட பகுதியில் வசிக்கும் தகுதியுடைய அனைத்து விவசாயிகளுக்கும் 'திறந்த மற்றும் தன்னார்வ உறுப்பினர் உரிமை' (Open & Voluntary Membership) வழங்கப்பட வேண்டும்.\n\n"
                    "**📁 உறுப்பினர் சேர்க்கைக்குத் தேவையான முக்கிய ஆவணங்கள்:**\n"
                    "1. **பூர்த்தி செய்யப்பட்ட உறுப்பினர் விண்ணப்பப் படிவம் (படிவம்-1)**.\n"
                    "2. **நில உரிமை ஆவணங்கள்**: பட்டா, சிட்டா, அடங்கல் அல்லது குத்தகை ஒப்பந்தப் பத்திரம் (விவசாயி என்பதை உறுதிப்படுத்த).\n"
                    "3. **அடையாளச் சான்று**: ஆதார் அட்டை / குடும்ப அட்டை (Ration Card) / வாக்காளர் அடையாள அட்டை நகல்.\n"
                    "4. **வங்கி கணக்கு விவரம்**: தேசியமயமாக்கப்பட்ட வங்கி அல்லது DCCB வங்கிக் கணக்கு புத்தக நகல் (IFSC குறியீட்டுடன்).\n"
                    "5. **பாஸ்போர்ட் அளவு புகைப்படங்கள்**: 2 புகைப்படங்கள்.\n"
                    "6. **பங்கு மூலதனத் தொகை மற்றும் நுழைவுக் கட்டணம்**: குறைந்தபட்ச பங்குத் தொகை (ரூ. 100 முதல் ரூ. 500 வரை) மற்றும் நுழைவுக் கட்டணம்.\n\n"
                    "**📝 விண்ணப்பிக்கும் செயல்முறை & காலக்கெடு (SLA):**\n"
                    "• **யாரிடம் சமர்ப்பிக்க வேண்டும்**: உங்கள் கிராமத்திற்குரிய தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கத்தின் (PACS) செயலாளர் அல்லது நிர்வாக அலுவலரிடம் விண்ணப்பத்தை அளிக்க வேண்டும்.\n"
                    "• **கருதப்படும் உறுப்பினர் உரிமை (Deemed Membership)**: விண்ணப்பம் மற்றும் கட்டணம் செலுத்திய 30 முதல் 60 நாட்களுக்குள் சங்கம் எந்தவித முடிவும் தெரிவிக்கவில்லை எனில், சட்டப்படி உறுப்பினர் சேர்க்கை அனுமதிக்கப்பட்டதாகக் கருதப்படும்.\n"
                    "• **மறுக்கப்பட்டால் மேல்முறையீடு**: விண்ணப்பம் நிராகரிக்கப்பட்டால், சரக கூட்டுறவு சங்கங்களின் துணைப் பதிவாளர் (Deputy Registrar of Cooperative Societies) அவர்களிடம் உடனடியாக மேல்முறையீடு செய்யலாம்.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட சட்டக் குறிப்புகள்:** {citations}"
                )
            elif code in ["PMFBY_72H_LOCALIZED_CALAMITY", "PMFBY_72H_CALAMITY_INTIMATION"]:
                return (
                    "### 🌧️ PMFBY பயிர் காப்பீடு: 72 மணி நேர இழப்பீட்டு அறிவிப்பு நடைமுறை & வழிகாட்டுதல்\n\n"
                    "**⚠️ கட்டாய 72 மணி நேர காலக்கெடு:**\n"
                    "இயற்கை பேரிடர் (ஆலங்கட்டி மழை, வெள்ளம், நிலச்சரிவு, புயல் அல்லது திடீர் கனமழை) ஏற்பட்ட **72 மணி நேரத்திற்குள்** பயிர் இழப்பு குறித்து கட்டாயம் தகவல் தெரிவிக்க வேண்டும்.\n\n"
                    "**📲 புகார் தெரிவிக்கும் 3 அதிகாரப்பூர்வ வழிகள்:**\n"
                    "1. **பயிர் காப்பீட்டுச் செயலி (Crop Insurance App / NCIP)** மூலம் நேரடியாகப் பதிவு செய்தல்.\n"
                    "2. **தேசிய இலவச உதவி எண்: 14447** அல்லது **1800-180-1551** என்ற எண்ணை அழைத்து புகார் பதிவு செய்தல்.\n"
                    "3. உங்கள் பகுதி **தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்க (PACS) செயலாளர்** அல்லது **வட்டார வேளாண்மை உதவி அலுவலரிடம் (AAO)** எழுத்துப்பூர்வமாக மனு அளித்தல்.\n\n"
                    "**⏱️ இழப்பீட்டு மதிப்பீடு மற்றும் தீர்வு காலக்கெடு:**\n"
                    "• **48 மணி நேரம்**: காப்பீட்டு நிறுவனத்தால் மதிப்பீட்டாளர் நியமனம்.\n"
                    "• **7 - 10 நாட்கள்**: வேளாண் துறை மற்றும் காப்பீட்டு நிறுவனத்தின் கூட்டு கள ஆய்வு.\n"
                    "• **15 நாட்கள்**: கள ஆய்வுக்குப் பின் 100% இழப்பீட்டுத் தொகை நேரடியாக விவசாயியின் வங்கிக் கணக்கில் DBT மூலம் வரவு வைக்கப்படும்.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட அரசு நெறிமுறைகள்:** {citations}"
                )
            elif code in ["PMFBY_PREMIUM_RATES", "PMFBY_CORE_PREMIUM_RATES"]:
                return (
                    "### 🌾 PMFBY பயிர் காப்பீட்டு பிரீமியம் விகிதங்கள்\n\n"
                    "**💰 விவசாயிகள் செலுத்த வேண்டிய சட்டப்பூர்வ பிரீமியம் அளவு:**\n"
                    "• **காரீப் பயிர்கள் (Kharif Crops)**: காப்பீட்டுத் தொகையில் **2% மட்டுமே**.\n"
                    "• **ரபி பயிர்கள் (Rabi Crops)**: காப்பீட்டுத் தொகையில் **1.5% மட்டுமே**.\n"
                    "• **வணிக மற்றும் தோட்டக்கலை பயிர்கள்**: காப்பீட்டுத் தொகையில் **5% மட்டுமே**.\n"
                    "*(மீதமுள்ள அனைத்து பிரீமியம் தொகையையும் மத்திய மற்றும் மாநில அரசுகள் 50:50 விகிதத்தில் மானியமாக வழங்குகின்றன)*.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட சட்டக் குறிப்புகள்:** {citations}"
                )

        # Check for 72h Calamity item
        if "intimation_protocol" in item or "mandatory_72h_rule" in item:
            if "intimation_protocol" in item:
                proto = "\n".join([f"  - {p}" for p in item["intimation_protocol"]])
                return (
                    f"### 🌧️ {title} ({code})\n\n"
                    f"**Overview:**\n{summary}\n\n"
                    f"**⚠️ Statutory 72-Hour Calamity Intimation Protocol & SLA:**\n{proto}\n\n"
                    f"🏛️ **Verified Official Sources:** {citations}"
                )
            else:
                perils = "\n".join([f"  - {p}" for p in item.get("covered_perils", [])])
                channels = "\n".join([f"  - {c}" for c in item.get("intimation_channels", [])])
                timeline = item.get("claim_settlement_timeline", {})
                tl_fmt = (
                    f"  • **48 Hours**: {timeline.get('appointment_of_assessor', 'Assessor appointed')}\n"
                    f"  • **10 Days**: {timeline.get('joint_survey', 'Joint survey completed')}\n"
                    f"  • **15 Days**: {timeline.get('claim_disbursal', 'Direct DBT bank payout')}"
                )
                return (
                    f"### 🌧️ {title} ({code})\n\n"
                    f"**⚠️ Mandatory 72-Hour Calamity Rule:**\n{item['mandatory_72h_rule']}\n\n"
                    f"**🌩️ Covered Natural Calamities & Perils:**\n{perils}\n\n"
                    f"**📲 3 Official Intimation Channels:**\n{channels}\n\n"
                    f"**⏱️ 4-Step Claim Settlement SLA Timeline:**\n{tl_fmt}\n\n"
                    f"🏛️ **Verified Legal Sources:** {citations}"
                )

        # Check for Premium Rates / Slabs
        elif "premium_rates" in item or "premium_slabs" in item:
            rates_dict = item.get("premium_rates") or item.get("premium_slabs", {})
            slabs = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in rates_dict.items()])
            return (
                f"### 🌾 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**💰 Statutory Farmer Premium Rates:**\n{slabs}\n\n"
                f"🏛️ **Verified Legal Sources:** {citations}"
            )

        # Check for PACS Multi-Services
        elif "permitted_activities" in item:
            acts = "\n".join([f"  - {a}" for a in item.get("permitted_activities", [])])
            return (
                f"### 🏢 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🛠️ Permitted Multi-Purpose Services at PACS:**\n{acts}\n\n"
                f"🏛️ **Verified Official Sources:** {citations}"
            )

        # Check for PACS Membership Rules
        elif "membership_rules" in item or "provisions" in item:
            provs = item.get("membership_rules") or item.get("provisions", [])
            if isinstance(provs, dict):
                rules = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in provs.items()])
            else:
                rules = "\n".join([f"  - {p}" for p in provs])
            return (
                f"### 📋 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🏛️ Statutory Membership Rules & Documents:**\n{rules}\n\n"
                f"🏛️ **Verified Legal Sources:** {citations}"
            )

        # Check for PACS Loan Disposal SLA
        elif "operational_rules" in item:
            rules = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in item.get("operational_rules", {}).items()])
            return (
                f"### ⏱️ {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**📜 Mandatory Operational SLAs:**\n{rules}\n\n"
                f"🏛️ **Verified Citizen Charter Standards:** {citations}"
            )

        # Check for PACS Custom Hiring
        elif "machinery_and_rates" in item:
            rates = "\n".join([f"  - {m}" for m in item.get("machinery_and_rates", [])])
            booking = item.get("booking_process", "")
            return (
                f"### 🚜 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🛠️ Available Machinery & Regulated Rental Rates:**\n{rates}\n\n"
                f"**📝 Booking Procedure:** {booking}\n\n"
                f"🏛️ **Verified Official Guidelines:** {citations}"
            )

        # Check for PACS CSC Services
        elif "key_services" in item:
            services = "\n".join([f"  - {s}" for s in item.get("key_services", [])])
            return (
                f"### 📲 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🌐 Available Digital Village Services:**\n{services}\n\n"
                f"🏛️ **Verified Digital Mission Standards:** {citations}"
            )

        # Check for PACS Jan Aushadhi / PMKSK
        elif "key_benefits" in item:
            benefits = "\n".join([f"  - {b}" for b in item.get("key_benefits", [])])
            return (
                f"### 💊 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🏥 Community Healthcare & Input Advantages:**\n{benefits}\n\n"
                f"🏛️ **Verified Government Sources:** {citations}"
            )

        # Check for Grain Storage Plan
        elif "financial_and_infra_support" in item:
            infra = "\n".join([f"  - {s}" for s in item.get("financial_and_infra_support", [])])
            return (
                f"### 🏗️ {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**📦 Infrastructure & Financial Subsidies:**\n{infra}\n\n"
                f"🏛️ **Verified Cabinet Decisions:** {citations}"
            )

        # Check for Computerization ERP
        elif "core_features" in item:
            feats = "\n".join([f"  - {f}" for f in item.get("core_features", [])])
            return (
                f"### 💻 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🖥️ Core Cloud ERP Capabilities:**\n{feats}\n\n"
                f"🏛️ **Verified National Project Standards:** {citations}"
            )

        # Check for Governance & Audit
        elif "governance_standards" in item:
            gov = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in item.get("governance_standards", {}).items()])
            return (
                f"### 🏛️ {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**⚖️ Statutory Governance & Audit Norms:**\n{gov}\n\n"
                f"🏛️ **Verified Cooperative Act Standards:** {citations}"
            )

        # Check for Bank Default Clause
        elif "statutory_rule" in item:
            return (
                f"### ⚖️ {title} ({code})\n\n"
                f"**🛡️ 100% Bank Default Liability Mandate:**\n{item.get('statutory_rule')}\n\n"
                f"**🏛️ Adjudication Authority:** {item.get('enforcement_authority')}\n\n"
                f"🏛️ **Verified Legal Sources:** {citations}"
            )

        # Default fallback
        return (
            f"### 📌 {title}\n\n"
            f"**Overview:**\n{summary}\n\n"
            f"🏛️ **Verified Sources:** {citations}"
        )
