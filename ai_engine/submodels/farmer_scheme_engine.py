"""
Specialized Farmer Scheme Sub-Model Engine for Cooperative AI Portal.
Handles scheme identification, eligibility matching, subsidy calculation, document checklists,
and verified online/offline application workflows across all 20+ Central & State agricultural schemes.
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings
from ai_engine.language.translation import TranslationEngine

class FarmerSchemeEngine:
    def __init__(self):
        self.schemes_catalog: List[Dict[str, Any]] = []
        self.translator = TranslationEngine()
        self._load_schemes()

    def _load_schemes(self):
        schemes_path = os.path.join(settings.DATABASE_PATH, "schemes", "farmer_schemes.json")
        if os.path.exists(schemes_path):
            try:
                with open(schemes_path, "r", encoding="utf-8") as f:
                    self.schemes_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading schemes catalog: {e}")

    def find_matching_schemes(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored_schemes = []

        # Exhaustive Weighted Trigger Registry for all 20 Schemes
        triggers = {
            "SVAMITVA": ["svamitva", "property card", "village mapping", "drone survey", "gharauni", "स्वामित्व", "घरौनी", "சொத்து அட்டை", "గ్రామీణ ఆస్తి", "प्रॉपर्टी कार्ड"],
            "SPICES-BOARD": ["cardamom", "spices board", "turmeric boiler", "pepper thresher", "lakadong", "iccd", "silpaulin", "इलायची", "मसाला बोर्ड", "हल्दी", "ஏலக்காய்", "மஞ்சள்", "మిరియాలు", "पसुपु", "वेलची"],
            "COFFEE-BOARD": ["coffee board", "coffee plantation", "baby pulper", "drying yard", "coffee", "कॉफी", "காபி", "కాఫీ"],
            "COCONUT-CPIS-KERA": ["coconut palm", "kera suraksha", "tree climber", "coconut board", "neera", "नारियल", "केरा सुरक्षा", "தென்னை", "కొబ్బరి"],
            "ACABC": ["acabc", "ac&abc", "agri clinic", "agri business center", "agri graduate", "कृषि क्लीनिक", "வேளாண் மருந்தகம்", "అగ్రి క్లినిక్", "अॅग्री क्लिनिक"],
            "NMNF-BPKP": ["natural farming", "nmnf", "bpkp", "jeevamrutha", "krishi sakhi", "cow based", "प्राकृतिक खेती", "जीवामृत", "இயற்கை வேளாண்மை", "సహజ వ్యవసాయం", "नैसर्गिक शेती"],
            "GOPAL-RATNA": ["gopal ratna", "gokul mission", "indigenous breed", "dairy award", "गोपाल रत्न", "गोकुल मिशन", "கோபால் ரத்னா", "గోపాల్ రత్న"],
            "STUDENT-READY": ["student ready", "rawe", "iari scholarship", "icar fellowship", "स्टूडेंट रेडी", "आईएआरआई", "மாணவர் ஊரக"],
            "GOBARDHAN": ["gobardhan", "biogas subsidy", "cbg plant", "cattle dung", "गोवर्धन", "बायोगैस", "கோபர்தன்", "గోబర్ధన్"],
            "AMI-ISAM": ["ami", "isam", "rural godown", "storage subsidy", "ग्रामीण गोदाम", "கிடங்கு மானியம்", "గ్రామీణ గోదాము"],
            "NMEO-OP": ["nmeo", "oil palm", "palm oil", "palm plantation", "ऑयल पाम", "पाम की खेती", "ஆயில் பாம்", "ఆయిల్ పామ్"],
            "PMJVM-TRIFED": ["pmjvm", "trifed", "van dhan", "minor forest produce", "vdvk", "वन धन", "जनजातीय", "பழங்குடியினர்", "వన్ ధన్"],
            "TDPS-TEA": ["tea board", "small tea grower", "small tea growers", "tea plucking", "tea mechanization", "tea plantation", "चाय विकास", "தேயிலை", "టీ అభివృద్ధి"],
            "NFSM": ["nfsm", "food security mission", "seed minikit", "pulses subsidy", "nutri cereals", "paddy seed", "wheat seed", "pulses seed", "certified seed", "खाद्य सुरक्षा मिशन", "बीज मिनीकिट", "உணவுப் பாதுகாப்பு", "சான்றளிக்கப்பட்ட விதை", "ఆహార భద్రత"],
            "SHC": ["soil health", "soil test", "soil testing", "soil card", "मिट्टी परीक्षण", "मृदा स्वास्थ्य", "மண் பரிசோதனை", "నేల పరీక్ష"],
            "ENAM": ["e-nam", "enam", "e nam", "mandi online", "online mandi", "mandi trade", "ई-नाम", "மண்டி வர்த்தகம்", "ఈ-நாம்"],
            "MIDH": ["midh", "tomato", "tomato seed", "tomato seeds", "vegetable seeds", "vegetable seed", "seeds", "seed", "sowing", "sow", "seedling", "seedlings", "horticulture", "polyhouse", "poly house", "shade net", "mulching", "orchard", "greenhouse", "mushroom", "vegetable cultivation", "தக்காளி", "விதை", "விதைகள்", "தக்காளி விதை", "காய்கறி விதை", "நாற்று", "தோட்டக்கலை", "பாலிஹவுஸ்", "पॉलीहाउस", "शेडनेट", "टमाटर के बीज", "सब्जी बीज", "தோட்டக்கலை துறை"],
            "RKVY-RAFTAAR": ["rkvy", "raftaar", "agri startup", "startup grant", "incubator", "रफ्तार", "एग्री-स्टार्टअप", "தொழில்முனைவு"],
            "PM-AASHA": ["pm-aasha", "pmaasha", "msp", "minimum support price", "procurement", "price support", "एमएसपी", "न्यूनतम समर्थन मूल्य", "குறைந்தபட்ச ஆதரவு விலை"],
            "FPO-10000": ["fpo", "farmer producer organization", "10000 fpo", "equity grant", "एफपीओ", "உழவர் உற்பத்தியாளர் அமைப்பு", "రైతు ఉత్పత్తిదారుల"],
            "NBHM": ["nbhm", "beekeeping", "honey mission", "bee box", "मधुमक्खी पालन", "शहद मिशन", "தேனீ வளர்ப்பு", "తేనెటీగల పెంపకం"],
            "PM-KMY": ["pm-kmy", "pmkmy", "maan-dhan", "maandhan", "farmer pension", "3000 pension", "₹3,000", "किसान पेंशन", "விவசாயிகள் ஓய்வூதியம்", "రైతు పెన్షన్"],
            "PM-KUSUM": ["kusum", "solar pump", "solar subsidy", "solar tubewell", "solar water pump", "water pump", "irrigation pump", "borewell motor", "5 hp", "7.5 hp", "3 hp", "power cut pump", "power cut", "electricity problem", "power supply", "feeder solarization", "agricultural pump", "pump set", "solar motor", "power cut problem", "सोलर पंप", "சோலார் பம்ப்", "சவுர பம்பு", "सौर कृषी पंप"],
            "SMAM": ["smam", "mechanization", "tractor subsidy", "drone subsidy", "kisan drone", "rotavator", "कृषि यंत्र", "ட்ராக்டர் மானியம்"],
            "PKVY": ["pkvy", "organic farming", "paramparagat krishi", "50000", "50,000", "जैविक खेती", "இயற்கை விவசாயம்"],
            "PMKSY-PDMC": ["pmksy", "drip irrigation", "sprinkler", "micro irrigation", "per drop more crop", "water problem", "water scarcity", "water shortage", "irrigation water", "water not coming", "borewell water", "farm water", "drip", "sprinkler subsidy", "ड्रिप सिंचाई", "पानी की समस्या", "सिंचाई पानी", "சொட்டு நீர் பாசனம்", "தண்ணீர் பிரச்சனை", "பாசன நீர்", "நீటి సమస్య", "సాగునీరు"],
            "PMAY-G": ["pmay", "awaas", "awas yojana", "pucca house", "rural housing", "120000", "1,20,000", "आवास योजना", "வீட்டு வசதி திட்டம்"],
            "NLM-AHIDF": ["livestock", "goat farming", "sheep farming", "poultry subsidy", "piggery", "पशुधन मिशन", "बकरी पालन", "ஆடு வளர்ப்பு"],
            "PMMSY": ["pmmsy", "matsya", "fisheries", "fish pond", "biofloc", "மத்ஸ்ய சம்பதா", "मछली पालन", "மீன்வள மேம்பாடு"],
            "AIF": ["aif", "agri infra", "agriculture infrastructure fund", "cold storage subsidy", "godown subsidy", "कृषि अवसंरचना कोष"],
            "KCC": ["kcc", "kisan credit card", "crop loan", "4%", "4 percent", "interest subvention", "केसीसी", "किसान क्रेडिट कार्ड", "பயிர் கடன்"],
            "PM-KISAN": ["pm-kisan", "pmkisan", "pm kisan", "kisan samman", "samman nidhi", "6000", "₹6,000", "2000", "installment", "किस्त", "पीएम किसान", "தவணை"],
            "RUBBER-MTFP": ["rubber", "natural rubber", "rubber board", "replanting rubber", "रबर", "ரப்பர்"],
            "NBM": ["bamboo", "bamboo mission", "बांस मिशन", "மூங்கில்"],
            "RAD-IFS": ["rainfed", "integrated farming", "ifs", "वर्षा आधारित खेती", "ஒருங்கிணைந்த பண்ணை"],
            "ISAC-NCDC": ["ncdc", "isac", "cooperative loan", "सहकारिता ऋण", "கூட்டுறவு கடன்"],
            "APEDA-FAS": ["apeda", "export promotion", "agri export", "कृषि निर्यात", "வேளாண் ஏற்றுமதி"],
            "LHDC": ["lhdc", "animal vaccination", "foot and mouth", "fmd", "pashu aadhaar", "पशु आधार", "पशु टीकाकरण", "கால்நடை தடுப்பூசி"],
            "ECOMARK": ["ecomark", "eco label", "पर्यावरण अनुकूल", "சுற்றுச்சூழல் முத்திரை"],
            "NAGAR-VAN": ["nagar van", "city forest", "nagar vatika", "नगर वन"],
            "PMAAGY-PMAGY": ["adi adarsh", "adarsh gram", "pm-ajay", "आदर्श ग्राम", "மாதிரி கிராமம்"],
            "PM-VANBANDHU": ["vanbandhu", "tribal scholarship", "वनबंधु कल्याण", "பழங்குடியினர் உதவித்தொகை"],
            "AGRI-AWARDS": ["krishi vigyan puraskar", "national water awards competition", "dhanwantari award", "geoscience award", "कृषि पुरस्कार"]
        }

        # 1. Multi-Field + Trigger Weighted Scoring
        q_tokens = set(re.findall(r'\w+', q_lower))

        for scheme in self.schemes_catalog:
            code = scheme.get("scheme_code", "")
            kw_list = triggers.get(code, [])
            score = 0.0

            # Direct trigger phrase matches
            for kw in kw_list:
                if kw in q_lower:
                    score += 6.0 if " " in kw else 3.0

            # Scheme Name and Code direct token matches
            s_name = scheme.get("scheme_name", "").lower()
            s_code = code.lower()
            if s_code and (s_code in q_lower or s_code.replace("-", "") in q_lower.replace("-", "")):
                score += 8.0
            for tok in q_tokens:
                if len(tok) > 2 and tok in s_name:
                    score += 2.0

            # Summary, Category & Benefit matches
            summary = (scheme.get("summary", "") + " " + scheme.get("category", "")).lower()
            for tok in q_tokens:
                if len(tok) > 3 and tok in summary:
                    score += 1.0

            # Financial benefit & Eligibility token matches
            benefit = scheme.get("financial_benefit", "").lower()
            for tok in q_tokens:
                if len(tok) > 3 and tok in benefit:
                    score += 1.0

            if score > 0:
                scored_schemes.append((score, scheme))

        # Sort by score descending
        if scored_schemes:
            scored_schemes.sort(key=lambda x: x[0], reverse=True)
            return [item[1] for item in scored_schemes]

        # No matching scheme — return empty so the caller can handle gracefully
        # instead of dumping the top catalog entries (the PM-KISAN-everything bug).
        return []

    def generate_scheme_guidance(self, query: str, language: str = "en") -> Dict[str, Any]:
        matched = self.find_matching_schemes(query)
        if not matched:
            return {
                "matched_schemes": [],
                "primary_scheme": {},
                "guidance_text": "",
                "financial_benefit": None,
                "official_portal": None,
                "documents_required": [],
                "citations": [],
                "is_verified": True,
                "trust_score": 0.0
            }

        primary = matched[0]

        guidance_text = self._format_scheme_response(primary, query, language)
        if language not in ("en", "ta", "hi"):
            guidance_text = self.translator.translate(guidance_text, "en", language)

        return {
            "matched_schemes": [s.get("scheme_name") for s in matched],
            "primary_scheme": primary,
            "guidance_text": guidance_text,
            "financial_benefit": primary.get("financial_benefit"),
            "official_portal": primary.get("official_portal"),
            "documents_required": primary.get("documents_required", []),
            "citations": primary.get("citations", []),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_scheme_response(self, scheme: Dict[str, Any], query: str, language: str) -> str:
        code = scheme.get("scheme_code", "")
        name = scheme.get("scheme_name", "Farmer Welfare Scheme")
        summary = scheme.get("summary", "")
        benefit = scheme.get("financial_benefit", "")
        eligibility = scheme.get("eligibility_criteria", "")
        portal = scheme.get("official_portal", "https://myscheme.gov.in")
        docs = scheme.get("documents_required", [])
        online_mode = scheme.get("application_mode_online", "")
        offline_mode = scheme.get("application_mode_offline", "")
        citations = scheme.get("citations", [])

        q_low = query.lower()

        is_asking_docs = any(w in q_low for w in ["document", "documents", "paper", "papers", "proof", "दस्तावेज़", "ஆவணங்கள்", "காగితాలు"])
        is_asking_subsidy = any(w in q_low for w in ["subsidy", "benefit", "amount", "money", "how much", "rate", "subvention", "अनुदान", "लाभ", "रुपये", "மானியம்", "தொகை", "సబ్சிడీ"])
        is_asking_eligibility = any(w in q_low for w in ["eligible", "eligibility", "who can", "criteria", "पात्रता", "தகுதி", "అర్హత"])
        is_asking_apply = any(w in q_low for w in ["how to apply", "apply", "registration", "register", "आवेदन", "விண்ணப்பிக்க", "దరఖాస్తు"])
        is_asking_seed = any(w in q_low for w in ["seed", "seeds", "sow", "sowing", "tomato", "vegetable", "seedling", "seedlings", "collect", "where to get", "where could i", "விதை", "விதைகள்", "நாற்று", "தக்காளி", "காய்கறி", "बीज", "टमाटर"])

        # Comprehensive Tamil Scheme Translations
        SCHEME_MAP_TA = {
            "MIDH": {
                "name": "ஒருங்கிணைந்த தோட்டக்கலை மேம்பாட்டு இயக்கம் (MIDH / தேசிய தோட்டக்கலை இயக்கம்)",
                "summary": "தோட்டக்கலை பயிர்கள், காய்கறி, தக்காளி விதைகள், பசுமைக்குடில் (Polyhouse) மற்றும் பழத்தோட்ட அமைப்பிற்கு 50% வரை அரசு மானியம் வழங்கும் திட்டம்.",
                "benefit": "சான்றளிக்கப்பட்ட காய்கறி மற்றும் தக்காளி விதைகளுக்கு 50% மானியம்; குழித்தட்டு நாற்றுகளுக்கு (Pro-tray Seedlings) 50% மானியம்; பசுமைக்குடில் அமைக்க சதுர மீட்டருக்கு ₹446 முதல் ₹530 வரை மானியம்.",
                "eligibility": "காய்கறி, தக்காளி, பழங்கள் மற்றும் தோட்டக்கலை பயிர்கள் சாகுபடி செய்யும் அனைத்து விவசாயிகள் மற்றும் கூட்டுறவு சங்கங்கள்.",
                "docs": [
                    "விண்ணப்பதாரரின் ஆதார் அட்டை (e-KYC)",
                    "நில உரிமை ஆவணம் (பட்டா / சிட்டா / அடங்கல் நகல்)",
                    "ஆதார் இணைக்கப்பட்ட வங்கி கணக்கு பாஸ்புக் (Direct Benefit Transfer)",
                    "வட்டார தோட்டக்கலை / கிராம நிர்வாக அலுவலர் (VAO) சாகுபடி சான்றிதழ்"
                ],
                "online": "உழவன் செயலி (Uzhavan App) அல்லது MIDH போர்ட்டல் (midh.gov.in)",
                "offline": "வட்டார தோட்டக்கலை உதவி இயக்குனர் அலுவலகம் (ADA Horticulture) / வட்டார வேளாண்மை விரிவாக்க மையம் (AEC) / உள்ளூர் தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACS)."
            },
            "NFSM": {
                "name": "தேசிய உணவு பாதுகாப்பு இயக்கம் (NFSM - சான்றளிக்கப்பட்ட விதை விநியோகம்)",
                "summary": "நெல், கோதுமை, பயறு வகைகள் மற்றும் சிறுதானியங்களின் உற்பத்தி திறனை அதிகரிக்க 50% மானியத்தில் சான்றளிக்கப்பட்ட விதைகள் மற்றும் மினிகிட் வழங்கும் திட்டம்.",
                "benefit": "பயறு மற்றும் சிறுதானிய விதைகளுக்கு 50% அரசு மானியம் (அல்லது கிலோவிற்கு ₹25 முதல் ₹50 வரை மானியம்); இலவச விதை மினிகிட் தொகுப்பு.",
                "eligibility": "அனைத்து சிறு, குறு மற்றும் பெரு விவசாயிகள்.",
                "docs": ["ஆதார் அட்டை", "பட்டா / சிட்டா", "வங்கி பாஸ்புக்"],
                "online": "உழவன் செயலி (Uzhavan App)",
                "offline": "வட்டார வேளாண்மை விரிவாக்க மையம் (AEC) / உள்ளூர் PACS சங்கம்."
            },
            "PM-KISAN": {
                "name": "பிரதான் மந்திரி கிசான் சம்மான் நிதி (PM-KISAN நேரடி வருமான ஆதரவு)",
                "summary": "சொந்தமாக சாகுபடி நிலம் வைத்துள்ள விவசாய குடும்பங்களுக்கு ஆண்டுதோறும் ₹6,000 நிதியுதவி (3 தவணைகளில் ₹2,000 வீதம்) நேரடியாக வங்கிக் கணக்கில் வழங்கப்படுகிறது.",
                "benefit": "ஆண்டுக்கு ₹6,000 (4 மாதங்களுக்கு ஒருமுறை ₹2,000 வீதம் 3 சம தவணைகளில் ஆதார் இணைக்கப்பட்ட வங்கிக் கணக்கில் DBT மூலம் வரவு).",
                "eligibility": "சொந்தமாக சாகுபடி நிலம் உள்ள அனைத்து விவசாய குடும்பங்கள்.",
                "docs": ["ஆதார் அட்டை (e-KYC)", "நில உரிமை பட்டா/சிட்டா", "ஆதார் இணைக்கப்பட்ட வங்கி பாஸ்புக்"],
                "online": "PM-KISAN போர்ட்டல் (pmkisan.gov.in) -> New Farmer Registration",
                "offline": "தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACS) / பொது இ-சேவை மையம் (CSC) / வட்டார வேளாண்மை விரிவாக்க மையம்."
            },
            "KCC": {
                "name": "கிசான் கிரெடிட் கார்டு (KCC - 4% மானிய பயிர் கடன்)",
                "summary": "விவசாயிகள் பயிர் சாகுபடி, விதை, உரம் மற்றும் அறுவடை செலவுகளுக்காக ₹3 லட்சம் வரை 4% சலுகை வட்டியில் குறுகிய கால கடன் வழங்கும் திட்டம்.",
                "benefit": "₹3 லட்சம் வரை 7% அடிப்படை வட்டியில் 3% உடனடி திருப்பிச் செலுத்தும் மானியம் (PRI) போக நிகர 4% வட்டியில் கடன். ₹1.60 லட்சம் வரை பிணையமற்ற கடன்.",
                "eligibility": "சொந்த நில விவசாயிகள், குத்தகை விவசாயிகள், பங்கு சாகுபடியாளர்கள் மற்றும் சுயஉதவி குழுக்கள்.",
                "docs": ["விண்ணப்பப் படிவம்", "ஆதார் / வாக்காளர் அட்டை", "பட்டா / நில குத்தகை ஆவணம்", "VAO பயிர் சாகுபடி அடங்கல் சான்றிதழ்"],
                "online": "ஜனசமர்த் போர்ட்டல் (jansamarth.in) அல்லது வங்கி இணையதளம்",
                "offline": "உள்ளூர் தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACS) / மாவட்ட மத்திய கூட்டுறவு வங்கி (DCCB) கிளை."
            },
            "PMFBY": {
                "name": "பிரதான் மந்திரி பயிர் காப்பீட்டுத் திட்டம் (PMFBY)",
                "summary": "இயற்கை பேரிடர், வறட்சி, அதிக கனமழை, வெள்ளம் மற்றும் பூச்சித் தாக்குதலால் ஏற்படும் பயிர் இழப்புகளுக்கு முழு காப்பீட்டு இழப்பீடு வழங்கும் திட்டம்.",
                "benefit": "விவசாயி செலுத்தும் பிரீமியம்: காரிஃப் உணவுப் பயிர்களுக்கு 2.0%, ரபி பயிர்களுக்கு 1.5%, தோட்டக்கலை பயிர்களுக்கு 5.0%. மீதி முழு பிரீமியத்தையும் அரசே மானியமாக செலுத்துகிறது.",
                "eligibility": "அறிவிக்கப்பட்ட பகுதியில் அறிவிக்கப்பட்ட பயிர்களை சாகுபடி செய்யும் அனைத்து விவசாயிகள்.",
                "docs": ["ஆதார் அட்டை", "நில பட்டா / சிட்டா", "பயிர் சாகுபடி சான்றிதழ் (VAO அடங்கல்)", "வங்கி பாஸ்புக் நகல்"],
                "online": "தேசிய பயிர் காப்பீட்டு போர்ட்டல் (pmfby.gov.in)",
                "offline": "உள்ளூர் PACS சங்கம் / பொது இ-சேவை மையம் (CSC) / வணிக வங்கிகள்."
            },
            "PM-KUSUM": {
                "name": "பிஎம்-குசும் சூரிய ஒளி பாசன பம்ப் திட்டம் (PM-KUSUM)",
                "summary": "விவசாய பாசனத்திற்கு சோலார் பம்ப் அமைத்தல் மற்றும் மின் இணைப்பு பெற்ற பம்புகளை சோலார் மயமாக்குவதற்கு 60% வரை அரசு மானியம் வழங்கும் திட்டம்.",
                "benefit": "60% மொத்த மூலதன மானியம் (30% மத்திய அரசு + 30% மாநில அரசு). விவசாயி பங்கு 10% மட்டுமே; மீதி 30% வங்கி கடன் வசதி.",
                "eligibility": "விவசாய நிலம் மற்றும் கிணறு/போர்வெல் நீர் ஆதாரம் உள்ள விவசாயிகள் மற்றும் PACS சங்கங்கள்.",
                "docs": ["ஆதார் அட்டை", "பட்டா / நில ஆவணம்", "வங்கி பாஸ்புக்", "தற்போதுள்ள மின் இணைப்பு ஆவணம் (பொருந்தினால்)"],
                "online": "TEDA தமிழ்நாடு எரிசக்தி மேம்பாட்டு முகமை போர்ட்டல் (teda.in)",
                "offline": "மாவட்ட புதுப்பிக்கத்தக்க எரிசக்தி முகமை (TEDA) / மின்வாரிய கிராமப்புற அலுவலகம் / PACS."
            }
        }

        # Comprehensive Hindi Scheme Translations
        SCHEME_MAP_HI = {
            "MIDH": {
                "name": "एकीकृत बागवानी विकास मिशन (MIDH / राष्ट्रीय बागवानी मिशन)",
                "summary": "सब्जी, टमाटर के प्रमाणित हाइब्रिड बीज, पॉलीहाउस, ड्रिप सिंचाई और फलोद्यान हेतु 50% तक सरकारी अनुदान प्रदान करने की योजना।",
                "benefit": "प्रमाणित सब्जी एवं टमाटर बीज और प्रो-ट्रे पौध पर 50% तक सब्सिडी; पॉलीहाउस/शेडनेट निर्माण पर 50% सब्सिडी।",
                "eligibility": "सब्जी, फल एवं बागवानी उत्पादक सभी किसान व सहकारी समितियां।",
                "docs": ["आधार कार्ड", "भूमि स्वामित्व अभिलेख (खसरा/खतौनी)", "बैंक पासबुक", "ब्लॉक कृषि प्रमाण पत्र"],
                "online": "MIDH पोर्टल (midh.gov.in)",
                "offline": "ब्लॉक कृषि विस्तार केंद्र (AEC) / सहायक निदेशक बागवानी कार्यालय / स्थानीय पैक्स (PACS)।"
            },
            "NFSM": {
                "name": "राष्ट्रीय खाद्य सुरक्षा मिशन (NFSM - प्रमाणित बीज वितरण)",
                "summary": "दलहन, तिलहन, मोटे अनाज एवं धान के प्रमाणित बीजों पर 50% तक सरकारी अनुदान एवं मुफ्त बीज मिनीकिट वितरण।",
                "benefit": "प्रमाणित बीजों पर 50% सब्सिडी (₹25 से ₹50 प्रति किग्रा तक अनुदान); निःशुल्क बीज मिनीकिट।",
                "eligibility": "सभी लघु, सीमांत एवं बड़े किसान।",
                "docs": ["आधार कार्ड", "खतौनी/जमाबंदी", "बैंक पासबुक"],
                "online": "प्रत्यक्ष लाभ अंतरण (DBT) कृषि पोर्टल",
                "offline": "ब्लॉक कृषि विस्तार केंद्र / प्राथमिक कृषि साख समिति (PACS)।"
            }
        }

        if language == "ta":
            t_data = SCHEME_MAP_TA.get(code, {})
            disp_name = t_data.get("name", name)
            disp_summary = t_data.get("summary", summary)
            disp_benefit = t_data.get("benefit", benefit)
            disp_eligibility = t_data.get("eligibility", eligibility)
            disp_offline = t_data.get("offline", offline_mode)
            disp_online = t_data.get("online", online_mode)
            docs_list = t_data.get("docs", [
                "விண்ணப்பதாரரின் ஆதார் அட்டை (e-KYC)",
                "நில உரிமை ஆவணம் (பட்டா / சிட்டா நகல்)",
                "ஆதார் இணைக்கப்பட்ட வங்கி கணக்கு பாஸ்புக் (DBT)",
                "கிராம நிர்வாக அலுவலர் (VAO) பயிர் சாகுபடி சான்றிதழ்"
            ])
            docs_formatted = "\n".join([f"  - {d}" for d in docs_list])

            sections = [f"### 📜 {disp_name}\n"]
            if is_asking_seed:
                sections.append(
                    "**🌱 சான்றளிக்கப்பட்ட விதை மற்றும் நாற்றுகள் பெறும் இடங்கள் (Where to Collect):**\n"
                    "- **வட்டார வேளாண்மை விரிவாக்க மையம் (AEC) / தோட்டக்கலை உதவி இயக்குனர் அலுவலகம்:** தக்காளி மற்றும் காய்கறி விதைகள் 50% அரசு மானியத்தில் பெறலாம்.\n"
                    "- **தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACS / PMKSK):** தரமான சான்றளிக்கப்பட்ட விதை இருப்பு மையம்.\n"
                    "- **அரசு தோட்டக்கலை பண்ணை (State Horticulture Farm):** குழித்தட்டு நாற்றுகள் (Pro-tray Seedlings).\n"
                )
                sections.append(f"**💰 நிதி உதவி மற்றும் மானிய விபரம்:**\n{disp_benefit}\n")
                sections.append(f"**📝 பதிவு மற்றும் பெறும் முறை:** ஆன்லைன்: [{disp_online}]({portal}) | நேரடி: {disp_offline}\n")
            elif is_asking_subsidy:
                sections.append(f"**💰 நிதி உதவி மற்றும் மானிய விபரம்:**\n{disp_benefit}\n")
                sections.append(f"**📌 திட்ட விளக்கம்:**\n{disp_summary}\n")
            elif is_asking_docs:
                sections.append(f"**📋 தேவையான ஆவணங்கள் சரிபார்ப்புப் பட்டியல்:**\n{docs_formatted}\n")
                sections.append(f"**💰 நிதி உதவி மற்றும் மானியம்:**\n{disp_benefit}\n")
            elif is_asking_eligibility:
                sections.append(f"**🎯 தகுதி வரம்புகள்:**\n{disp_eligibility}\n")
                sections.append(f"**💰 நிதி உதவி:**\n{disp_benefit}\n")
            elif is_asking_apply:
                sections.append(f"**📝 விண்ணப்பிக்கும் முறை:**\n- **ஆன்லைன் பதிவு:** {disp_online} (இணையதளம்: [{portal}]({portal}))\n- **நேரடி விண்ணப்பம்:** {disp_offline}\n")
                sections.append(f"**📋 தேவையான ஆவணங்கள்:**\n{docs_formatted}\n")
            else:
                sections.append(f"**📌 திட்ட விளக்கம்:**\n{disp_summary}\n")
                sections.append(f"**💰 நிதி உதவி மற்றும் மானிய விபரம்:**\n{disp_benefit}\n")
                sections.append(f"**📋 தேவையான ஆவணங்கள்:**\n{docs_formatted}\n")
                sections.append(f"**📝 விண்ணப்பிக்கும் முறை:**\n- **ஆன்லைன்:** {disp_online} (இணையதளம்: [{portal}]({portal}))\n- **நேரடி:** {disp_offline}\n")

            sections.append(f"🏛️ **அரசாணை மற்றும் சட்டப்பிரிவு மேற்கோள்கள்:** {', '.join(citations)}")
            return "\n".join(sections)

        elif language == "hi":
            t_data = SCHEME_MAP_HI.get(code, {})
            disp_name = t_data.get("name", name)
            disp_summary = t_data.get("summary", summary)
            disp_benefit = t_data.get("benefit", benefit)
            disp_eligibility = t_data.get("eligibility", eligibility)
            disp_offline = t_data.get("offline", offline_mode)
            disp_online = t_data.get("online", online_mode)
            docs_list = t_data.get("docs", [
                "आधार कार्ड (e-KYC अनिवार्य)",
                "भूमि स्वामित्व दस्तावेज (खसरा/खतौनी/जमाबंदी)",
                "आधार लिंक बैंक खाता पासबुक (DBT)",
                "पटवारी/कृषि अधिकारी बुवाई प्रमाण पत्र"
            ])
            docs_formatted = "\n".join([f"  - {d}" for d in docs_list])

            sections = [f"### 📜 {disp_name}\n"]
            if is_asking_seed:
                sections.append(
                    "**🌱 प्रमाणित बीज एवं पौध वितरण केंद्र (Where to Collect):**\n"
                    "- **ब्लॉक कृषि विस्तार केंद्र (AEC) / बागवानी डिपो:** प्रमाणित हाइब्रिड सब्जी/टमाटर के बीज 50% सरकारी अनुदान पर उपलब्ध।\n"
                    "- **स्थानीय प्राथमिक कृषि साख समिति (PACS / PMKSK):** प्रमाणित बीज कोटा वितरण केंद्र।\n"
                    "- **राजकीय बागवानी फार्म एवं नर्सरी:** प्रो-ट्रे पौध एवं उन्नत किस्में।\n"
                )
                sections.append(f"**💰 वित्तीय लाभ एवं अनुदान:**\n{disp_benefit}\n")
                sections.append(f"**📝 आवेदन एवं पंजीयन:** ऑनलाइन: [{disp_online}]({portal}) | ऑफ़लाइन: {disp_offline}\n")
            elif is_asking_subsidy:
                sections.append(f"**💰 वित्तीय लाभ एवं अनुदान सहायता:**\n{disp_benefit}\n")
                sections.append(f"**📌 योजना विवरण:**\n{disp_summary}\n")
            elif is_asking_docs:
                sections.append(f"**📋 आवश्यक दस्तावेज़ चेकलिस्ट:**\n{docs_formatted}\n")
                sections.append(f"**💰 वित्तीय लाभ:**\n{disp_benefit}\n")
            elif is_asking_eligibility:
                sections.append(f"**🎯 पात्रता मानदंड:**\n{disp_eligibility}\n")
                sections.append(f"**💰 वित्तीय लाभ:**\n{disp_benefit}\n")
            elif is_asking_apply:
                sections.append(f"**📝 आवेदन प्रक्रिया:**\n- **ऑनलाइन आवेदन:** {disp_online} (पोर्टल: [{portal}]({portal}))\n- **ऑफ़लाइन आवेदन:** {disp_offline}\n")
                sections.append(f"**📋 आवश्यक दस्तावेज़:**\n{docs_formatted}\n")
            else:
                sections.append(f"**📌 योजना सारांश:**\n{disp_summary}\n")
                sections.append(f"**💰 वित्तीय लाभ एवं अनुदान:**\n{disp_benefit}\n")
                sections.append(f"**📋 आवश्यक दस्तावेज़:**\n{docs_formatted}\n")
                sections.append(f"**📝 आवेदन प्रक्रिया:**\n- **ऑनलाइन:** {disp_online} (पोर्टल: [{portal}]({portal}))\n- **ऑफ़लाइन:** {disp_offline}\n")

            sections.append(f"🏛️ **सत्यापित आधिकारिक संदर्भ:** {', '.join(citations)}")
            return "\n".join(sections)

        else:
            docs_formatted = "\n".join([f"  - {d}" for d in docs])
            sections = [f"### 📜 {name}\n"]
            if is_asking_subsidy:
                sections.append(f"**💰 Financial Benefit & Subsidy Slabs:**\n{benefit}\n")
                sections.append(f"**📌 Scheme Overview:**\n{summary}\n")
            elif is_asking_docs:
                sections.append(f"**📋 Mandatory Document Checklist:**\n{docs_formatted}\n")
                sections.append(f"**💰 Financial Benefit:**\n{benefit}\n")
            elif is_asking_eligibility:
                sections.append(f"**🎯 Eligibility Criteria:**\n{eligibility}\n")
                sections.append(f"**💰 Financial Benefit:**\n{benefit}\n")
            elif is_asking_apply:
                sections.append(f"**📝 Application Workflow:**\n- **Online Registration:** {online_mode} (Official Portal: [{portal}]({portal}))\n- **Offline Submission:** {offline_mode}\n")
                sections.append(f"**📋 Required Documents:**\n{docs_formatted}\n")
            else:
                sections.append(f"**📌 Scheme Overview:**\n{summary}\n")
                sections.append(f"**💰 Financial Benefit & Subsidy Slabs:**\n{benefit}\n")
                sections.append(f"**📋 Mandatory Document Checklist:**\n{docs_formatted}\n")
                sections.append(f"**📝 Application Workflow:**\n- **Online:** {online_mode} (Official Portal: [{portal}]({portal}))\n- **Offline:** {offline_mode}\n")

            sections.append(f"🏛️ **Verified Official Citations:** {', '.join(citations)}")
            return "\n".join(sections)
