"""
Exhaustive Multilingual Intent Classifier & Multi-Domain Fusion Orchestrator.
Supports 5 core sub-classes:
1. pacs_pmfby (PACS Services & PMFBY Crop Insurance / 72h Calamity)
2. farmer_scheme (PM-KISAN, AIF, PM-KUSUM, SMAM, PKVY, Subsidies)
3. grievance (Complaints, Bribes, Rejections, Sec 19 Appeals, Escalation)
4. cooperative_law (MSCS Act 2023, Bylaws, Sec 45 Election, Sec 84 Arbitration)
5. financial_literacy (KCC 4% Interest Subvention, Scale of Finance, AEPS)
"""
import re
from typing import Dict, Any, List, Optional

class IntentClassifier:
    def __init__(self):
        # Exhaustive Domain Keyword & Multilingual Pattern Registry
        self.domain_keywords: Dict[str, List[str]] = {
            "pacs_pmfby": [
                # PMFBY & Crop Insurance signatures
                "pmfby", "fasal bima", "fasalbima", "crop insurance", "crop loss", "crop damage",
                "damaged crop", "damaged crops", "ruined crop", "ruined crops", "destroyed crop", "destroyed crops",
                "crops destroyed", "crop destroyed", "crops got destroyed", "crops got desteroyed", "desteroyed",
                "standing crop", "harvest loss", "lost crops", "lost my crops", "crop failure", "crops failure",
                "post harvest", "post-harvest loss", "cut and spread", "hailstorm", "flood damage", "rain damage",
                "heavy rain", "heavy rains", "heavy rainfall", "rain", "rains", "rainfall", "excess rain", "excess rainfall",
                "flood", "flooding", "flash flood", "inundation", "waterlogging", "submerged", "drought", "dry spell", "unseasonal rain",
                "unseasonal rains", "cyclone", "pest attack", "locust", "disease outbreak",
                "landslide", "cloud burst", "natural fire", "lightning", "72 hours", "72-hour", "72 hour",
                "72hrs", "72 hrs", "within 72", "localized calamity", "crop cutting experiment", "cce",
                "claim form", "crop claim", "insurance claim", "insurance company", "ncip", "ncip portal",
                "crop insurance app", "crop destruction", "survey number", "insurance docket",
                "insurance policy", "intimation", "claim status", "aic", "hsg", "crop survey",
                # Multilingual PMFBY (Hindi, Tamil, Telugu, Marathi, Kannada, Bengali, Gujarati, Punjabi)
                "फसल बीमा", "ओलावृष्टि", "बाढ़", "सूखा", "72 घंटे", "फसल नुकसान", "बीमा क्लेम", "अतिवृष्टि", "फसल क्षति", "जलभराव", "कीट प्रकोप", "दावा", "बारिश", "भारी बारिश",
                "பயிர் காப்பீடு", "பயிர் சேதம்", "ஆலங்கட்டி மழை", "வெள்ளம்", "72 மணி நேரம்", "பயிர் இழப்பு", "வறட்சி", "காப்பீட்டு கோரிக்கை", "மழை", "கனமழை", "பயிர் அழிந்தது",
                "పంట భీమా", "పంట నష్టం", "వడగళ్ళు", "వరదలు", "72 గంటలు", "పంట బీమా క్లెయిమ్", "కరువు", "నష్టపరిహారం", "వర్షం", "భారీ వర్షాలు",
                "पिक विमा", "गारपीट", "अतिवृष्टी", "पिकांचे नुकसान", "विमा दावा", "72 तास", "दुष्काळ", "कीड", "पाऊस", "मुसळधार पाऊस", "फसल विमा", "पीक विमा",
                "ಬೆಳೆ ವಿಮೆ", "ಬೆಳೆ ಹಾನಿ", "ಆಲಿಕಲ್ಲು ಮಳೆ", "ನೆರೆ", "72 ಗಂಟೆ", "ವಿಮೆ ಕ್ಲೈಮ್", "ಮಳೆ",
                "ফসল বিমা", "শস্য বীমা", "বন্যা", "শিলাবৃষ্টি", "খরা", "৭২ ঘণ্টা", "ক্ষতিপূরণ", "বৃষ্টি",
                "પાક વીમો", "કમોસમી વરસાદ", "કરા", "પૂર", "૭૨ કલાક", "પાક નુકસಾನ", "વરસાદ",
                "ਫ਼ਸਲ ਬੀਮਾ", "ਗੜੇਮਾਰੀ", "ਹੜ੍ਹ", "ਸੋਕਾ", "72 ਘੰਟੇ", "ਮੀਂਹ",
                # PACS Core Services & Operations signatures
                "pacs", "primary agricultural credit society", "primary agriculture", "society secretary",
                "pacs secretary", "pacs president", "society president", "managing committee", "pacs membership",
                "share capital", "nominal member", "regular member", "fertilizer quota", "fertilizer distribution",
                "urea supply", "urea bag", "dap quota", "dap supply", "npk fertilizer", "mop", "seed distribution",
                "certified seeds", "grain procurement", "msp procurement", "paddy procurement", "wheat procurement",
                "custom hiring center", "custom hiring", "chc", "tractor rental", "harvester rental", "drone rental",
                "farm implement", "pacs computerization", "pacs erp", "nabard erp", "cold storage rental",
                "godown rental", "warehouse receipt", "wrda", "model bye-laws", "model bylaws", "common service center",
                "csc in pacs", "pmksk", "pradhan mantri kisan samriddhi kendra", "jan aushadhi kendra",
                "generic medicine", "lpg distributorship in pacs", "petrol pump pacs",
                # Multilingual PACS
                "पैक्स", "सहकारी समिति", "खाद", "यूरिया", "डीएपी", "ट्रैक्टर किराया", "कस्टम हायरिंग", "सोसायटी सचिव", "शेयर पूंजी", "पैक्स सदस्यता",
                "கூட்டுறவு சங்கம்", "உரம்", "யூரியா", "வாடகை டிராக்டர்", "சங்க செயலாளர்", "பங்கு மூலதனம்",
                "ప్రాథమిక వ్యవసాయ సహకార సంఘం", "ఎరువులు", "యూరియా", "సొసైటీ సెక్రటరీ", "సభ్యత్వం",
                "प्राथमिक कृषी पतसंस्था", "खते", "युरिया", "सोसायटी सचिव", "भाग भांडवल", "कस्टम हायरिंग",
                "ಪ್ರಾಥಮಿಕ ಕೃಷಿ ಪತ್ತಿನ ಸಹಕಾರ ಸಂಘ", "ಗೊಬ್ಬರ", "ಕಾರ್ಯದರ್ಶಿ"
            ],
            "farmer_scheme": [
                "pm-kisan", "pmkisan", "pm kisan", "kisan samman nidhi", "samman nidhi", "pmkisan.gov.in",
                "installment", "four monthly installment", "6000", "₹6,000", "2000", "₹2,000", "17th installment",
                "18th installment", "19th installment", "ekyc", "e-kyc", "land seeding", "npci seeding",
                "dbt mapping", "aif", "agri infra fund", "agriculture infrastructure fund", "cold storage subsidy",
                "godown subsidy", "sorting grading", "silo subsidy", "pm-kusum", "pm kusum", "kusum component a",
                "kusum component b", "kusum component c", "solar pump", "solar subsidy", "solar tubewell",
                "solar water pump", "60% subsidy", "smam", "sub-mission on agricultural mechanization",
                "farm mechanization", "tractor subsidy", "drone subsidy", "kisan drone", "combine harvester subsidy",
                "power tiller subsidy", "pkvy", "paramparagat krishi", "paramparagat krishi vikas yojana",
                "natural farming", "organic farming grant", "bhartiya prakritik krishi paddhati", "bpkp",
                "fertilizer subsidy", "dbt fertilizer", "myscheme", "myscheme portal", "nabard subsidy",
                "soil health card", "shc", "per drop more crop", "micro irrigation subsidy", "drip irrigation subsidy",
                "sprinkler subsidy", "pmksy", "farmer scheme", "farmer subsidy", "subsidy", "grant", "yojana",
                "krishi yojana", "sarkari yojana", "state subsidy", "borewell", "farm pond", "drip", "sprinkler",
                "electricity", "power cut", "power supply", "pump set", "solar motor", "electric motor", "agricultural power",
                "tomato", "seeds", "seed", "sowing", "sow", "tomato seeds", "vegetable seeds", "seedling", "seedlings", "horticulture", "midh", "nfsm", "polyhouse", "orchard", "fruit crops", "certified seed",
                "पीएम किसान", "किसान सम्मान निधि", "पीएम कुसुम", "सोलर पंप", "सब्सिडी", "अनुदान", "किस्त", "ई-केवाईसी", "टमाटर", "टमाटर के बीज", "सब्जी बीज", "बीज वितरण", "बागवानी",
                "कृषि अवसंरचना कोष", "प्राकृतिक खेती", "कृषि यंत्र सब्सिडी", "ड्रिप सिंचाई", "मृदा स्वास्थ्य कार्ड", "पानी की समस्या", "सिंचाई पानी", "बिजली की समस्या",
                "திட்டம்", "விவசாய மானியம்", "சோலார் பம்ப்", "பிஎம் கிசான்", "தவணை", "இயற்கை விவசாயம்", "தண்ணீர் பிரச்சனை", "பாசன நீர்", "சொட்டு நீர் பாசனம்", "மின்வெட்டு", "மின்சாரம்",
                "தக்காளி", "தக்காளி விதை", "விதை", "விதைகள்", "நாற்று", "காய்கறி", "விதைக்க", "தோட்டக்கலை", "சான்றளிக்கப்பட்ட விதை",
                "పథకం", "రైతు సబ్సిడీ", "సౌర పంపు", "పీఎం కిసాన్", "వాయిదా", "సహజ వ్యవసాయం", "నీటి సమస్య", "సాగునీరు", "విద్యుత్ సమస్య", "విత్తనాలు", "టమాట విత్తనాలు",
                "कृषी योजना", "सौर पंप", "अनुदान योजना", "हप्ता", "सेंद्रिय शेती", "ठिबक सिंचन", "पाण्याची समस्या", "वीज समस्या"
            ],
            "grievance": [
                # Grievances, Disputes, Rejections & Statutory Escalation
                "complaint", "file complaint", "register grievance", "lodge grievance", "reject", "rejected", "rejecting",
                "rejection", "refusal", "refused", "refuse", "refusing", "deny", "denied", "denies", "denying",
                "delay", "delayed", "delaying", "delayed payout", "delayed claim", "deliberately delaying",
                "not paid", "not giving", "not provided", "not accepted", "refuses to", "refusing to", "pending loan",
                "water problem", "water not coming", "canal water", "water dispute", "water supply", "drinking water", "panchayat water",
                "charging extra", "extra money", "extra charge", "extra cost", "more money", "above price", "high price", "overpriced", "fertilizer price",
                "bribe", "demanding bribe", "asked for money", "corruption", "fraud", "embezzlement", "harassment", "misconduct", "nepotism", "cheating", "cut", "commission",
                "overcharging", "above mrp", "mrp", "black marketing", "forced", "bundling", "tagging", "tie-in",
                "no dues", "noc", "title deed", "land deed", "mortgage release", "return documents", "unauthorized deduction", "hidden charges",
                "tampering", "voter list", "electoral roll", "removed name", "where to complain", "who will pay", "how to appeal",
                "arcs", "assistant registrar", "assistant registrar of cooperative societies", "drcs",
                "deputy registrar", "jrcs", "joint registrar", "rcs", "registrar of cooperative societies",
                "central registrar", "section 19", "sec 19", "appeal", "statutory appeal", "statutory sla",
                "citizen charter", "deemed membership", "tribunal", "cooperative tribunal", "grievance redressal",
                "ombudsman", "cooperative ombudsman", "banking ombudsman", "officer recommendation",
                "escalate", "escalation", "unjust", "arbitrary", "show cause notice", "dgrc", "sgrc",
                "district grievance redressal committee", "state grievance committee", "dispute", "investigation",
                # Aadhaar Card Updates, Corrections & Citizen Service Grievances
                "aadhar", "aadhaar", "aadhar card", "aadhaar card", "change my name", "change name", "change address",
                "update address", "update my address", "update name", "where i can go", "whom i need to meet", "where can i go",
                "whom do i meet", "who to meet", "aadhar update", "aadhaar update", "correction in aadhar", "aadhar correction",
                "aadhaar correction", "ask center", "aadhaar seva kendra",
                # Multilingual Grievance
                "शिकायत", "अपील", "रद्द", "अस्वीकार", "मना कर दिया", "मना किया", "नहीं ले रहा", "नहीं दिया", "नहीं दे रहा", "देरी", "रिश्वत", "घूस", "भ्रष्टाचार", "गबन", "जबरन", "अधिक पैसे", "कमीशन", "शिकायत कहाँ करें", "पानी की समस्या", "नहर का पानी",
                "सहायक निबंधक", "अधिकारी", "निवारण", "धारा 19", "लोकपाल", "न्यायाधिकरण", "आधार कार्ड", "नाम बदलना", "पता बदलना", "आधार सुधार", "आधार केंद्र",
                "புகார்", "மேல்முறையீடு", "நிராகரிப்பு", "தாமதம்", "இழுத்தடிக்கிறார்கள்", "முறையிடுவது", "லஞ்சம்", "அதிகாரி", "பிரிவு 19", "முறையீடு", "கூடுதல் விலை", "தண்ணீர் பிரச்சனை", "குடிநீர் பிரச்சனை", "வாய்க்கால் தண்ணீர்",
                "ஆதார் கார்டு", "ஆதார் பெயர் மாற்றம்", "முகவரி மாற்றம்", "ஆதார் திருத்தம்", "ஆதார் அட்டை", "எங்கு செல்ல வேண்டும்", "யாரை சந்திக்க வேண்டும்",
                "ఫిర్యాదు", "అప్పీల్", "తిరస్కరణ", "ఆలస్యం", "అవినీతి", "లంచం", "అధికారి", "సెక్షన్ 19", "ఎక్కడ ఫిర్యాదు చేయాలి", "నీటి సమస్య", "ఆధార్ కార్డు", "పేరు మార్పు", "చిరునామా మార్పు",
                "तक्रार", "अपील", "नाकारले", "विलंब", "लाच", "सहकार निबंधक", "भ्रष्टाचार", "चौकशी", "तक्रार कुठे करावी", "काळाबाजार", "पाण्याची समस्या", "आधार कार्ड", "नाव बदलणे", "पत्ता बदलणे"
            ],
            "cooperative_law": [
                # Legal Legislation & Governance
                "mscs act", "mscs act 2023", "mscs act 2002", "multi-state cooperative societies act",
                "multi state cooperative societies", "cooperative amendment act 2023", "amendment",
                "state cooperative societies act", "cooperative law", "cooperative legislation", "bylaw",
                "bye-law", "model bylaw", "board of directors", "managing committee", "agm", "annual general meeting",
                "special general meeting", "sgm", "quorum", "voting right", "voting rights", "one member one vote",
                "election dispute", "audit", "statutory audit", "concurrent audit", "inquiry", "inspection under act",
                "supersession", "board suspension", "disqualification of director", "section 20", "section 43",
                "section 45", "section 84", "arbitration", "arbitrator", "cooperative election authority",
                "cea", "liquidation", "winding up", "administrator",
                # Multilingual Law
                "कानून", "अधिनियम", "धारा", "उप-नियम", "वार्षिक आम बैठक", "चुनाव", "धारा 45", "धारा 84", "मध्यस्थता", "मतदान अधिकार",
                "சட்டம்", "பிரிவு", "துணை விதிகள்", "தேர்தல்", "நடுவர் மன்றம்", "பொதுக்குழு",
                "చట్టం", "సెక్షన్", "నియమావళి", "ఎన్నికలు", "మధ్యవర్తిత్వం", "ఓటింగ్ హక్కు",
                "सहकारी कायदा", "पोटनियम", "निवडणूक", "लवाद", "सर्वसाधारण सभा", "कायदेशीर कलम"
            ],
            "financial_literacy": [
                # Credit & Financial Education
                "kcc", "kisan credit card", "interest subvention", "4% interest", "4 percent", "4%",
                "7% interest", "7 percent", "3% subvention", "prompt repayment", "prompt repayment subvention",
                "crop loan", "short term loan", "st crop loan", "scale of finance", "district level technical committee",
                "dltc", "working capital", "moratorium", "nabard interest", "collateral free loan", "1.6 lakh",
                "3 lakh", "effective interest", "loan waiver", "aeps", "micro atm", "savings rate",
                "credit limit", "passbook", "banking safety", "micro finance", "biometric authentication",
                "dbt failure", "npci mapping", "aadhaar seeding", "overdue interest", "compound interest",
                "title deed", "land documents", "loan repayment", "return documents", "5000 per day", "fair practices",
                "zero fee", "zero processing fee", "no dues certificate", "cibil", "credit score", "npci mapper",
                # Multilingual Finance
                "केसीसी", "किसान क्रेडिट कार्ड", "ऋण", "ब्याज दर", "ब्याज छूट", "4 प्रतिशत", "स्केल ऑफ फाइनेंस", "माइक्रो एटीएम", "दस्तावेज़ वापसी", "नो ड्यूज",
                "கிசான் கிரெடிட் கார்டு", "பயிர் கடன்", "வட்டி மானியம்", "4 சதவீத வட்டி", "வங்கி பாதுகாப்பு", "உரிமை ஆவணம்",
                "కిసాన్ క్రెడిట్ కార్డ్", "పంట రుణం", "వడ్డీ రాయితీ", "4 శాతం వడ్డీ", "రుణ పరిమితి",
                "किसान क्रेडिट कार्ड", "कर्ज", "व्याज दर", "व्याज सवलत", "पत मर्यादा"
            ],
            "general": [
                # Greetings, identity and general assistance (no scheme / legal intent)
                "hello", "hi ", "hey", "namaste", "namaskar", "vanakkam", "good morning", "good evening",
                "good afternoon", "thanks", "thank you", "who are you", "what are you", "what can you do",
                "how can you help", "help me", "help", "start", "guide me", "what is this", "about this",
                "नमस्ते", "नमस्कार", "धन्यवाद", "வணக்கம்", "நன்றி", "நீங்கள் யார்", "ధన్యవాదాలు",
                "ನಮಸ್ಕಾರ", "धन्यवाद", "hej", "ssup",
            ]
        }

    def classify(self, query: str) -> Dict[str, Any]:
        cleaned_query = query.lower()
        raw_scores: Dict[str, int] = {domain: 0 for domain in self.domain_keywords}
        
        # 1. Exact phrase and token pattern matching
        for domain, keywords in self.domain_keywords.items():
            for kw in keywords:
                if kw in cleaned_query:
                    weight = 4 if " " in kw else 2
                    raw_scores[domain] += weight
                else:
                    pattern = r'\b' + re.escape(kw) + r'\b'
                    if re.search(pattern, cleaned_query):
                        weight = 5 if " " in kw else 3
                        raw_scores[domain] += weight

        # 2. Critical context boosters
        # 72-hour crop loss emergency booster
        if any(w in cleaned_query for w in ["pmfby", "fasal bima", "hailstorm", "flood", "72 hour", "72-hour", "72hr", "crop loss", "crop damage", "crops damaged", "crops destroyed", "crop destroyed", "crops got desteroyed", "desteroyed", "heavy rain", "rain", "rains", "rainfall", "excess rain", "waterlogging", "inundation", "cyclone", "पिक विमा", "பயிர் காப்பீடு", "बೆಳೆ ವಿಮೆ", "பயிர் சேதம்"]):
            raw_scores["pacs_pmfby"] += 6

        # Grievance / dispute booster (only for actual complaints/violations)
        if any(w in cleaned_query for w in ["reject", "refuse", "bribe", "corruption", "not given", "delayed loan", "overcharg", "bundling", "cheated", "fraud", "complaint", "harassment", "शिकायत", "புகார்", "லஞ்சம்", "மோசம்", "तक्रार"]):
            raw_scores["grievance"] += 5

        # Financial literacy booster
        if any(w in cleaned_query for w in ["4%", "4 percent", "interest rate", "scale of finance", "kcc limit", "ब्याज दर", "वட்டி"]):
            raw_scores["financial_literacy"] += 4

        # Cooperative Law booster
        if any(w in cleaned_query for w in ["section 45", "section 84", "section 19", "mscs", "arbitration", "election authority", "धारा 45", "धारा 84"]):
            raw_scores["cooperative_law"] += 5

        # Farmer Scheme booster
        if any(w in cleaned_query for w in ["pm-kisan", "pmkisan", "kusum", "solar pump", "aif", "subsidy", "सब्सिडी", "पीएम किसान"]):
            raw_scores["farmer_scheme"] += 4

        # Greeting / small-talk booster
        if any(w in cleaned_query for w in ["hello", "hi", "hey", "namaste", "thanks", "thank you", "who are you",
                                             "what can you do", "help", "नमस्ते", "வணக்கம்", "नमस्कार"]):
            raw_scores["general"] += 5

        # 3. Determine active domains and multi-domain fusion activation
        sorted_domains = sorted(raw_scores.items(), key=lambda x: x[1], reverse=True)
        top_domain, top_score = sorted_domains[0]

        active_domains = []
        for dom, score in sorted_domains:
            # Active if score >= 3, or significant relative weight to top domain
            if score >= 3 or (top_score > 0 and score >= max(3, top_score * 0.35)):
                active_domains.append(dom)

        if not active_domains:
            # No scheme/law/insurance signal at all — treat as a general chat inquiry.
            # NEVER default to farmer_scheme (that was the PM-KISAN-everything bug).
            active_domains = ["general"]

        confidence = min(round((top_score / 14.0), 2), 0.99) if top_score > 0 else 0.50

        # 4. Extract rich entity slots
        extracted_entities = self._extract_slots(cleaned_query)

        return {
            "primary_domain": active_domains[0],
            "active_domains": active_domains,
            "is_multi_domain": len(active_domains) > 1,
            "domain_count": len(active_domains),
            "confidence": confidence,
            "domain_scores": raw_scores,
            "extracted_slots": extracted_entities,
            "raw_query": query
        }

    def _extract_slots(self, text: str) -> Dict[str, Any]:
        slots: Dict[str, Any] = {}
        
        # Calamity detection
        calamities = [
            "hailstorm", "flood", "inundation", "drought", "unseasonal rain",
            "cyclone", "pest attack", "fire", "landslide", "cloud burst",
            "ओलावृष्टि", "बाढ़", "सूखा", "गारपीट", "வெள்ளம்", "ನೆರೆ", "বন্যা", "પૂર", "ਹੜ੍ਹ"
        ]
        for c in calamities:
            if c in text:
                slots["calamity_type"] = c
                break

        # Crop detection
        crops = [
            "wheat", "paddy", "rice", "mustard", "cotton", "sugarcane", "soybean",
            "maize", "groundnut", "gram", "potato", "onion", "chana", "bajra", "jowar",
            "गेहूं", "धान", "चावल", "सरसों", "कपास", "गन्ना", "सोयाबीन"
        ]
        for crop in crops:
            if crop in text:
                slots["crop_name"] = crop
                break

        # Urgency & 72h window detection
        if any(w in text for w in ["yesterday", "today", "72 hours", "72-hour", "72hrs", "urgent", "damage", "ruined", "destroyed", "72 घंटे", "72 மணி", "72 तास"]):
            slots["urgency"] = "critical_72h"

        # Authority touchpoint detection
        if any(w in text for w in ["secretary", "pacs secretary", "society secretary", "पैक्स सचिव", "சங்க செயலாளர்"]):
            slots["touchpoint"] = "PACS Secretary"
        elif any(w in text for w in ["arcs", "assistant registrar", "सहायक निबंधक"]):
            slots["touchpoint"] = "ARCS (Assistant Registrar)"
        elif any(w in text for w in ["drcs", "deputy registrar", "उप निबंधक"]):
            slots["touchpoint"] = "DRCS (Deputy Registrar)"
        elif any(w in text for w in ["dgrc", "grievance committee", "district committee"]):
            slots["touchpoint"] = "DGRC (District Grievance Committee)"
        elif any(w in text for w in ["ombudsman", "tribunal"]):
            slots["touchpoint"] = "Cooperative Ombudsman / Tribunal"

        # Scheme identification
        if "pm-kisan" in text or "pmkisan" in text or "samman nidhi" in text or "किसान सम्मान" in text:
            slots["scheme_identified"] = "PM-KISAN"
        elif "pmfby" in text or "fasal bima" in text or "crop insurance" in text or "फसल बीमा" in text:
            slots["scheme_identified"] = "PMFBY"
        elif "kusum" in text or "solar pump" in text or "सोलर पंप" in text:
            slots["scheme_identified"] = "PM-KUSUM"
        elif "kcc" in text or "kisan credit card" in text or "केसीसी" in text:
            slots["scheme_identified"] = "KCC"
        elif "aif" in text or "agri infra" in text or "infrastructure fund" in text:
            slots["scheme_identified"] = "AIF"

        # Financial values
        if "4%" in text or "4 percent" in text:
            slots["interest_rate_inquired"] = "4% (Prompt Repayment)"
        elif "6000" in text or "₹6,000" in text:
            slots["benefit_amount"] = "₹6,000 / year"

        return slots
