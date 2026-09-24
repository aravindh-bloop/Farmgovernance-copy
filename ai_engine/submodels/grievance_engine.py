"""
Specialized Grievance Redressal Sub-Model Engine for Cooperative AI Portal.
Handles grievance classification, 4-step statutory remedies, legal escalation ladders,
competent override authorities, evidence checklists, and auto-generated ready-to-print
formal legal complaint/petition drafts across Indian languages.
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings

class GrievanceEngine:
    def __init__(self):
        self.grievances_catalog: List[Dict[str, Any]] = []
        self._load_catalog()

    def _load_catalog(self):
        catalog_path = os.path.join(settings.DATABASE_PATH, "grievances", "grievance_catalog.json")
        if os.path.exists(catalog_path):
            try:
                with open(catalog_path, "r", encoding="utf-8") as f:
                    self.grievances_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading grievances catalog: {e}")

    def find_matching_grievance(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored = []

        triggers = {
            "PACS_LOAN_DELAY": ["loan delay", "loan denied", "refused loan", "delaying loan", "loan sanction", "pending loan", "लोन में देरी", "ऋण देने से मना", "கடன் தாமதம்", "రుణం ఆలస్యం", "कर्ज नकार"],
            "PMFBY_PREMIUM_DEFAULT": ["pmfby default", "premium not paid by pacs", "bank default", "insurance rejected", "crop insurance claim not received", "डाटा नॉट फाउंड", "प्रीमियम जमा नहीं किया", "காப்பீடு நிராகரிப்பு", "బీమా క్లెయిమ్ రాలేదు"],
            "FERTILIZER_OVERCHARGING_BUNDLING": ["mrp", "fertilizer overcharging", "bundling", "urea price", "dap price", "black market", "खाद अधिक दाम", "यूरिया अधिक मूल्य", "உரம் கூடுதல் விலை", "ఎరువుల ఎక్కువ ధర", "खतांचा काळाबाजार"],
            "MEMBERSHIP_DENIAL_POLITICAL": ["membership denied", "refused membership", "cancel membership", "member banaya nahi", "सदस्यता देने से इनकार", "உறுப்பினர் சேர்க்கை மறுப்பு", "సభ్యత్వం నిరాకరణ", "सभासदत्व नकार"],
            "BRIBE_CORRUPTION_COMMISSION": ["bribe", "corruption", "cut", "commission", "asking money", "demand money", "रिश्वत", "घूस", "கமிஷன்", "லஞ்சம்", "లంచం", "लाच मागितली"],
            "NO_DUES_CERTIFICATE_DELAY": ["no dues", "noc", "title deed", "land deed", "mortgage release", "एनओसी", "नो ड्यूज", "நோ டியூஸ்", "నో డ్యూస్", "कागदपत्रे परत"],
            "COOP_ELECTION_VOTER_FRAUD": ["election", "voter list", "electoral roll", "voting right", "चुनाव", "मतदाता सूची", "தேர்தல் முறைகேடு", "ఎన్నికల ఓటర్ జాబితా", "निवडणूक गैरव्यवहार"],
            "DIVIDEND_SHARE_WITHHOLDING": ["dividend", "bonus", "share money", "लाभांश", "डिविडेंड", "பங்கு லாபம்", "డివిడెండ్", "लाभांश मिळाला नाही"],
            "UNAUTHORIZED_BANK_DEDUCTIONS": ["unauthorized deduction", "hidden charges", "insurance deducted without permission", "खाते से अवैध कटौती", "அனுமதியின்றி பிடித்தம்", "ఖాతా నుండి అనధికారిక కట్", "विनापरवानगी पैसे कपात"],
            "FINANCIAL_FRAUD_MISAPPROPRIATION": ["embezzlement", "fraud", "scam", "bogus loan", "gaban", "घोटाला", "फर्जी लोन", "முறைகேடு", "மோசம்", "पैशांची अफरातफर"],
            "IRRIGATION_WATER_DISPUTE": ["water problem", "water not coming", "water scarcity", "water shortage", "canal water", "irrigation water", "water dispute", "drinking water", "water supply", "panchayat water", "borewell dried", "irrigation delay", "தண்ணீர் பிரச்சனை", "குடிநீர் பிரச்சனை", "வாய்க்கால் தண்ணீர்", "பாசன நீர்", "पानी की समस्या", "नहर का पानी", "सिंचाई समस्या", "நீటి సమస్య"],
            "AADHAAR_UPDATE_NAME_ADDRESS_GRIEVANCE": ["aadhar", "aadhaar", "aadhar card", "aadhaar card", "change my name", "change name", "change address", "update address", "update my address", "update name", "where i can go", "whom i need to meet", "where can i go", "whom do i meet", "who to meet", "aadhar update", "aadhaar update", "correction in aadhar", "aadhar correction", "aadhaar correction", "ask center", "aadhaar seva kendra", "आधार कार्ड", "नाम बदलना", "पता बदलना", "आधार सुधार", "आधार केंद्र", "ஆதார் கார்டு", "ஆதார் பெயர் மாற்றம்", "முகவரி மாற்றம்", "ஆதார் திருத்தம்", "ஆதார் அட்டை", "எங்கு செல்ல வேண்டும்", "யாரை சந்திக்க வேண்டும்"]
        }

        q_tokens = set(re.findall(r'\w+', q_lower))

        for item in self.grievances_catalog:
            code = item.get("grievance_code", "")
            kw_list = triggers.get(code, [])
            score = 0.0

            # 1. Trigger phrase match
            for kw in kw_list:
                if kw in q_lower:
                    score += 6.0 if " " in kw else 3.0

            # 2. Category & Code match
            cat = (item.get("category", "") + " " + code).lower()
            if code.lower() in q_lower:
                score += 8.0
            for tok in q_tokens:
                if len(tok) > 2 and tok in cat:
                    score += 2.0

            # 3. Problem statement & Remedy match
            prob = (item.get("problem_statement", "") + " " + item.get("statutory_remedy", "")).lower()
            for tok in q_tokens:
                if len(tok) > 3 and tok in prob:
                    score += 1.0

            if score > 0:
                scored.append((score, item))

        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            return [s[1] for s in scored]

        return self.grievances_catalog[:2]

    def generate_grievance_guidance(self, query: str, language: str = "en") -> Dict[str, Any]:
        matched = self.find_matching_grievance(query)
        primary = matched[0]

        guidance_text = self._format_grievance_response(primary, language)

        return {
            "matched_grievances": [g.get("category") for g in matched],
            "primary_grievance": primary,
            "guidance_text": guidance_text,
            "statutory_remedy": primary.get("statutory_remedy"),
            "override_authority": primary.get("override_authority"),
            "legal_sections": primary.get("legal_sections", []),
            "sla_days": primary.get("sla_days", 15),
            "required_evidence": primary.get("required_evidence", []),
            "penalty_on_violator": primary.get("penalty_on_violator"),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_grievance_response(self, g: Dict[str, Any], language: str) -> str:
        cat = g.get("category", "Cooperative Grievance")
        code = g.get("grievance_code", "GRV")
        problem = g.get("problem_statement", "")
        remedy = g.get("statutory_remedy", "")
        override = g.get("override_authority", "")
        sections = ", ".join(g.get("legal_sections", []))
        sla = g.get("sla_days", 15)
        evidence = g.get("required_evidence", [])
        ladder = g.get("escalation_ladder", [])
        penalty = g.get("penalty_on_violator", "")

        # Specialized Aadhaar Name & Address Update Format
        if code == "AADHAAR_UPDATE_NAME_ADDRESS_GRIEVANCE":
            if language == "ta":
                return (
                    "### 🪪 ஆதார் அட்டையில் பெயர் மற்றும் முகவரி மாற்றம் செய்யும் நடைமுறை வழிகாட்டுதல்\n\n"
                    "ஆதார் அட்டையில் **பெயர்** மற்றும் **முகவரி** இரண்டையும் மாற்றுவதற்கு, நீங்கள் அங்கீகரிக்கப்பட்ட **ஆதார் சேர்க்கை மையம் (Aadhaar Enrolment Centre)** அல்லது **ஆதார் சேவை மையத்திற்கு (Aadhaar Seva Kendra - ASK)** நேரில் செல்ல வேண்டும்.\n\n"
                    "> 💡 **முக்கிய வேறுபாடு / குறிப்பு**: முகவரியை மட்டும் myAadhaar போர்டலில் ஆன்லைனில் மாற்றிக்கொள்ளலாம்; ஆனால் **பெயர் மாற்றம் செய்வதற்கு பயோமெட்ரிக் (கைரேகை அல்லது கருவிழி ஸ்கேன்) சரிபார்ப்பு கட்டாயம்** என்பதால் ஆதார் மையத்திற்கு நேரில் செல்ல வேண்டும்.\n\n"
                    "🏢 **எங்கு செல்லலாம்? (அங்கீகரிக்கப்பட்ட இடங்கள்)**\n"
                    "• **ஆதார் சேவை மையங்கள் (Aadhaar Seva Kendras - ASK)**: UIDAI நேரடி மேற்பார்வையில் செயல்படும் பிரத்யேக அரசு மையங்கள்.\n"
                    "• **அங்கீகரிக்கப்பட்ட வங்கிக் கிளைகள் மற்றும் அஞ்சலகங்கள்**: பல தேசியமயமாக்கப்பட்ட வங்கிகள் மற்றும் தலைமை அஞ்சலகங்களில் நிரந்தர ஆதார் கவுண்டர்கள் செயல்படுகின்றன.\n"
                    "• **மாநில அரசு இ-சேவை மையங்கள் (E-Sevai Centers) & தொடக்க வேளாண் கூட்டுறவு சங்க இ-சேவை மையங்கள் (PACS CSC)**: கிராம மற்றும் வட்டார அளவில் செயல்படும் அங்கீகரிக்கப்பட்ட மையங்கள்.\n\n"
                    "👤 **யாரை சந்திக்க வேண்டும்?**\n"
                    "மையத்திற்குச் செல்லும்போது நீங்கள் இரண்டு அங்கீகரிக்கப்பட்ட அதிகாரிகளுடன் தொடர்பு கொள்வீர்கள்:\n"
                    "• **ஆவண சரிபார்ப்பு அலுவலர் (The Verifier)**: நுழைவு அல்லது டோக்கன் கவுண்டரில் உங்கள் புதிய பெயர் மற்றும் முகவரிக்கான அசல் சட்டப்பூர்வ ஆவணங்களைச் சரிபார்த்து உறுதி செய்யும் அரசு அலுவலர்.\n"
                    "• **ஆதார் கணினி ஆபரேட்டர் (The Aadhaar Operator)**: கணினி முனையத்தில் புதிய விவரங்களை UIDAI மென்பொருளில் பதிவேற்றி, ஆவணங்களை ஸ்கேன் செய்து, பயோமெட்ரிக் (கைரேகை/கருவிழி) சரிபார்ப்பு செய்து விண்ணப்பத்தைச் சமர்ப்பிக்கும் தொழில்நுட்ப அலுவலர்.\n\n"
                    "📝 **படிநிலைகள் மற்றும் தேவையான ஆவணங்கள்:**\n\n"
                    "• **படி 1: அசல் ஆவணங்களை எடுத்துச் செல்லுதல்** (அசல் ஆவணங்கள் மட்டுமே ஏற்றுக்கொள்ளப்படும்; ஜெராக்ஸ் செல்லாது):\n"
                    "  - **பெயர் மாற்றத்திற்கு (அடையாளச் சான்று - PoI)**: பாஸ்போர்ட், பான் கார்டு (PAN), வாக்காளர் அடையாள அட்டை, ஓட்டுநர் உரிமம் அல்லது அரசாணை (Gazette Notification).\n"
                    "  - **முகவரி மாற்றத்திற்கு (முகவரிச் சான்று - PoA)**: வங்கி கணக்கு புத்தகம் (Bank Passbook), மின்கட்டண ரசீது (3 மாதங்களுக்குள்), வாக்காளர் அட்டை, குடும்ப அட்டை (Ration Card) அல்லது பதிவு செய்யப்பட்ட வாடகை ஒப்பந்தம்.\n\n"
                    "• **படி 2: முன்பதிவு செய்தல் (பரிந்துரைக்கப்படுகிறது)**: `myaadhaar.uidai.gov.in` இணையதளத்தில் முன்பதிவு செய்து செல்லலாம் அல்லது நேரடியாகச் சென்று டோக்கன் பெறலாம்.\n\n"
                    "• **படி 3: விண்ணப்பப் படிவத்தைப் பூர்த்தி செய்தல்**: ஆதார் திருத்தப் படிவத்தைப் பூர்த்தி செய்து வழங்கவும்.\n\n"
                    "• **படி 4: கட்டணம் மற்றும் பயோமெட்ரிக் பதிவு**: பயோமெட்ரிக் சரிபார்ப்புக்குப் பின் நிர்ணயிக்கப்பட்ட அரசு கட்டணமாக **ரூ. 50 முதல் ரூ. 75** செலுத்த வேண்டும்.\n\n"
                    "• **படி 5: ரசீது பெறுதல்**: **URN எண் (Update Request Number)** அடங்கிய ஒப்புகைச் சீட்டைப் பெற்றுக்கொள்ளவும். இதன் மூலம் ஆதார் நிலையை ஆன்லைனில் கண்காணிக்கலாம்.\n\n"
                    "🏛️ **புகார் மற்றும் உதவிக்கு**: கூடுதல் கட்டணம் வசூலித்தால் அல்லது ஆவணங்களை ஏற்க மறுத்தால் UIDAI கட்டணமில்லா உதவி எண் **1947** அல்லது மாவட்ட இ-சேவை மேலாளரிடம் (DeGM) புகார் அளிக்கலாம்.\n\n"
                    "💬 *உங்கள் ஆவணங்களை முன்கூட்டியே சரிபார்க்க விரும்பினால், புதிய பெயர் மற்றும் முகவரிக்காக உங்களிடம் தற்போது உள்ள ஆவணங்களைக் குறிப்பிடவும்; அவை UIDAI பட்டியலில் உள்ளதா என்பதை நான் உறுதிப்படுத்துகிறேன்.*"
                )
            elif language == "hi":
                return (
                    "### 🪪 आधार कार्ड में नाम एवं पता बदलने की प्रक्रिया एवं कानूनी मार्गदर्शन\n\n"
                    "आधार कार्ड में **नाम** और **पता** दोनों बदलने के लिए आपको किसी अधिकृत **आधार नामांकन केंद्र (Aadhaar Enrolment Centre)** या **आधार सेवा केंद्र (Aadhaar Seva Kendra - ASK)** पर व्यक्तिगत रूप से जाना होगा।\n\n"
                    "> 💡 **महत्वपूर्ण नियम / अंतर**: केवल पता myAadhaar पोर्टल पर ऑनलाइन बदला जा सकता है, लेकिन **नाम बदलने के लिए बायोमेट्रिक प्रमाणीकरण (फिंगरप्रिंट या आइरिस स्कैन) अनिवार्य है**, इसलिए केंद्र पर जाना आवश्यक है।\n\n"
                    "🏢 **आप कहाँ जा सकते हैं? (अधिकृत केंद्र)**\n\n"
                    "• **आधार सेवा केंद्र (ASK)**: UIDAI द्वारा सीधे संचालित आधिकारिक केंद्र।\n"
                    "• **अधिकृत बैंक शाखाएं एवं डाकघर**: स्थायी आधार अपडेट काउंटर।\n"
                    "• **राज्य सरकार ई-सेवा केंद्र एवं पैक्स कॉमन सर्विस सेंटर (PACS CSC)**: ग्राम पंचायत एवं ब्लॉक स्तर के अधिकृत नागरिक केंद्र।\n\n"
                    "👤 **आपको किससे मिलना होगा?**\n\n"
                    "केंद्र पर आपकी मुलाकात दो अधिकृत व्यक्तियों से होगी:\n"
                    "• **दस्तावेज़ सत्यापनकर्ता (The Verifier)**: प्रवेश/टोकन डेस्क पर आपके मूल पहचान एवं पते के प्रमाणों की जांच करने वाले अधिकृत अधिकारी।\n"
                    "• **आधार ऑपरेटर (The Aadhaar Operator)**: कंप्यूटर टर्मिनल पर विवरण दर्ज करने, दस्तावेज़ स्कैन करने, बायोमेट्रिक लेने और पावती पर्ची जारी करने वाले तकनीकी अधिकारी।\n\n"
                    "📝 **चरणबद्ध निर्देश एवं आवश्यक दस्तावेज़:**\n\n"
                    "• **चरण 1: मूल दस्तावेज़ साथ लाएं** (केवल ओरिजिनल कॉपी मान्य; फोटोकॉपी स्वीकार नहीं की जाएगी):\n"
                    "  - **नाम बदलने के लिए (पहचान प्रमाण - PoI)**: पासपोर्ट, पैन कार्ड, वोटर आईडी, ड्राइविंग लाइसेंस या सरकारी गजट अधिसूचना।\n"
                    "  - **पता बदलने के लिए (पता प्रमाण - PoA)**: बैंक पासबुक, बिजली बिल (3 महीने के भीतर), राशन कार्ड, वोटर आईडी या पंजीकृत रेंट एग्रीमेंट।\n\n"
                    "• **चरण 2: अपॉइंटमेंट बुक करें (वैकल्पिक परंतु अनुशंसित)**: `myaadhaar.uidai.gov.in` पर ऑनलाइन समय बुक करें या सीधे केंद्र जाकर टोकन लें।\n\n"
                    "• **चरण 3: फॉर्म भरें**: केंद्र पर आधार सुधार फॉर्म भरें।\n\n"
                    "• **चरण 4: बायोमेट्रिक एवं शुल्क**: निर्धारित सरकारी शुल्क **₹50 से ₹75** जमा करें और बायोमेट्रिक पुष्टि दें।\n\n"
                    "• **चरण 5: पावती रसीद प्राप्त करें**: **URN (Update Request Number)** पर्ची संभालकर रखें, जिससे स्थिति ट्रैक की जा सके।\n\n"
                    "🏛️ **शिकायत निवारण एवं सहायता**: अधिक पैसे मांगने या मना करने पर UIDAI टोल-फ्री **1947** या जिला ई-गवर्नेंस प्रबंधक (DeGM) से शिकायत करें।\n\n"
                    "💬 *यदि आप अपने दस्तावेज़ों की पहले से पुष्टि करना चाहते हैं, तो कृपया बताएं कि आपके पास नए नाम और पते के कौन-से दस्तावेज़ हैं; मैं जांच कर बताऊंगा कि वे UIDAI सूची में मान्य हैं या नहीं।*"
                )
            else:
                return (
                    "To change both your **name** and **address** in your Aadhaar card, you must visit an authorized **Aadhaar Enrolment Centre or Aadhaar Seva Kendra (ASK)**.\n\n"
                    "> 💡 **Important Distinction**: While address-only changes can be done online on the official myAadhaar portal, **name changes require a physical visit to a center** because your biometric information (fingerprints or iris scan) must be scanned by the operator to verify your identity and authorize the change.\n\n"
                    "🏢 **Where You Can Go**\n\n"
                    "• **Aadhaar Seva Kendras (ASK)**: These are dedicated, official centers run directly by UIDAI.\n"
                    "• **Authorized Bank Branches & Post Offices**: Many nationalized banks and local post offices host permanent Aadhaar update counters.\n"
                    "• **State Government E-Seva Centers / PACS Common Service Centres (CSC)**: Approved citizen service centers operated by your state government and Primary Agricultural Credit Societies.\n\n"
                    "👤 **Whom You Need to Meet**\n\n"
                    "When you arrive at the center, you will interact with two specific individuals who are trained and authorized by the government:\n"
                    "• **The Verifier**: A government-appointed officer at the entry or token desk who checks your original legal documents to confirm they are valid and match the new name and address you are requesting.\n"
                    "• **The Aadhaar Operator**: The technical official sitting at the computer terminal. They will physically type your new name and address into the secure UIDAI software, scan your documents, and capture your fingerprint or iris scan to biometrically \"sign off\" and submit your request.\n\n"
                    "📝 **Step-by-Step Instructions & Document Checklist**\n\n"
                    "• **Step 1: Gather Your Documents** (You must bring original physical documents with you; photocopied versions will not be accepted):\n"
                    "  - **For Name Change (Proof of Identity - PoI)**: Bring a valid Proof of Identity showing your correct name (e.g., Passport, PAN Card, Voter ID, Driving License, or a Government Gazette Notification).\n"
                    "  - **For Address Change (Proof of Address - PoA)**: Bring a valid Proof of Address showing your new residence (e.g., Bank Passbook/Statement, Electricity Bill within 3 months, Voter ID, Ration Card, or Rent Agreement).\n\n"
                    "• **Step 2: Book an Appointment (Optional but Recommended)**: You can go to the official **UIDAI myAadhaar Portal** (`myaadhaar.uidai.gov.in`) to book a specific time slot at a nearby center to avoid long lines. If you do not book online, you can walk in directly and request a token.\n\n"
                    "• **Step 3: Fill Out the Form**: At the center, fill out the Aadhaar Correction/Update Form with your correct new name and address.\n\n"
                    "• **Step 4: Update and Fee**: The operator will process your request and take your biometrics. A standard demographic update fee of **₹50 to ₹75** is charged at the counter.\n\n"
                    "• **Step 5: Keep the Receipt**: The operator will hand you an Acknowledgement Slip containing an **Update Request Number (URN)**. Use this URN on the UIDAI portal to track your update status until your new card is generated.\n\n"
                    "🏛️ **Grievance Redressal**: If an operator overcharges or wrongfully refuses service, escalate immediately to UIDAI Toll-Free **1947** or your District e-Governance Manager (DeGM).\n\n"
                    "💬 *If you want to prepare your papers beforehand, what specific documents do you currently have that show your correct new name and address? I can verify if they are on the official UIDAI approved list.*"
                )

        evidence_fmt = "\n".join([f"  - {e}" for e in evidence])
        ladder_fmt = "\n".join([f"  • **Level {l['level']} ({l['authority']} - {l['timeline']})**: {l['action']}" for l in ladder])

        if language == "hi":
            return (
                f"### ⚖️ कानूनी शिकायत निवारण एवं समाधान: {cat}\n\n"
                f"**🔍 समस्या विश्लेषण:**\n{problem}\n\n"
                f"**🛡️ वैधानिक समाधान एवं आपके अधिकार:**\n{remedy}\n\n"
                f"**🪜 3-स्तरीय अपीलीय सीढ़ी (SLA समय सीमा: {sla} दिन):**\n{ladder_fmt}\n\n"
                f"**📁 अनिवार्य साक्ष्य चेकलिस्ट:**\n{evidence_fmt}\n\n"
                f"**🏛️ सक्षम अपीलीय अधिकारी:** {override}\n"
                f"**📜 कानूनी धाराएं:** {sections}\n"
                f"**⚠️ दोषी अधिकारी पर कार्रवाई:** {penalty}\n\n"
                f"📝 **औपचारिक शिकायत प्रारूप (Petition Draft):**\n"
                f"```text\n"
                f"सेवा में,\n"
                f"श्रीमान {override}\n"
                f"विषय: {cat} के संबंध में वैधानिक शिकायत - धारा {sections}\n\n"
                f"महोदय,\n"
                f"मैं प्राथमिक कृषि ऋण समिति (PACS) का सदस्य हूँ। {problem}\n"
                f"नागरिक अधिकार पत्र (Citizen Charter) के तहत निर्धारित {sla} दिनों में कोई समाधान नहीं हुआ है।\n"
                f"प्रार्थना: कृपया {sections} के तहत तत्काल राहत प्रदान करें और दोषी अधिकारी के विरुद्ध विभागीय जांच का आदेश दें।\n\n"
                f"भवदीय,\n"
                f"[आवेदक का नाम, हस्ताक्षर एवं मोबाइल]\n"
                f"```"
            )
        elif language == "ta":
            return (
                f"### ⚖️ சட்டப்பூர்வ தீர்வு மற்றும் புகார் நடைமுறை: {cat}\n\n"
                f"**🔍 பிரச்சனை விபரம்:**\n{problem}\n\n"
                f"**🛡️ சட்டப்பூர்வ தீர்வு மற்றும் உங்கள் உரிமைகள்:**\n{remedy}\n\n"
                f"**🪜 மேல்முறையீட்டு படிநிலைகள் (SLA: {sla} நாட்கள்):**\n{ladder_fmt}\n\n"
                f"**📁 தேவையான ஆதாரங்கள்:**\n{evidence_fmt}\n\n"
                f"**🏛️ மேல்முறையீட்டு அதிகாரி:** {override}\n"
                f"**📜 சட்டப் பிரிவுகள்:** {sections}\n"
                f"**⚠️ விதிமீறலுக்கான தண்டனை:** {penalty}"
            )
        else:
            return (
                f"### ⚖️ Statutory Grievance Resolution & Legal Remedy: {cat} ({code})\n\n"
                f"**🔍 Problem Analysis:**\n{problem}\n\n"
                f"**🛡️ Statutory Remedy & Farmer Rights:**\n{remedy}\n\n"
                f"**🪜 3-Tier Escalation Ladder & Time Limits (SLA: {sla} Days):**\n{ladder_fmt}\n\n"
                f"**📁 Mandatory Evidence Checklist:**\n{evidence_fmt}\n\n"
                f"**🏛️ Competent Override Authority:** {override}\n"
                f"**📜 Applicable Statutory Laws:** {sections}\n"
                f"**⚠️ Penalties on Violator:** {penalty}\n\n"
                f"**📝 Ready-to-Print Legal Petition Draft:**\n"
                f"```text\n"
                f"To,\n"
                f"The Competent Authority / {override}\n\n"
                f"Subject: Formal Statutory Petition regarding {cat} under {sections} - Reg.\n\n"
                f"Respected Sir/Madam,\n"
                f"I am a member of the Primary Agricultural Credit Society (PACS). {problem}\n"
                f"Despite representations, the service has been unlawfully withheld beyond the statutory timeline of {sla} days.\n\n"
                f"PRAYER / RELIEF SOUGHT:\n"
                f"1. Direct immediate sanction/redressal under the powers vested under {sections}.\n"
                f"2. Initiate disciplinary action against the responsible officer.\n"
                f"3. Award compensation for harassment and financial loss.\n\n"
                f"Yours sincerely,\n"
                f"[Applicant Name, Signature, Member ID & Mobile]\n"
                f"```"
            )
