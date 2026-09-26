"""
Specialized Financial & Credit Literacy Sub-Model Engine for Cooperative AI Portal.
Handles:
- KCC Limit Calculation (Scale of Finance, 10% household, 20% maintenance, 5-year revolving credit)
- Modified Interest Subvention Scheme (7% base rate, 3% Prompt Repayment Incentive, 4% effective interest)
- Collateral-free limits (₹1.60L / ₹2.00L) & allied sector credit (₹2.00L)
- Fair Lending Practices (zero fees up to ₹3 Lakh, mandatory 15-day title deed release under ₹5,000/day penalty)
- Digital Banking Safety (AePS, Micro-ATMs, 2FA biometric security)
- NPCI Aadhaar Mapper DBT Seeding
- Natural Calamity Loan Restructuring & CIBIL Protection
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings

class FinancialLiteracyEngine:
    def __init__(self):
        self.fin_catalog: List[Dict[str, Any]] = []
        self._load_catalog()

    def _load_catalog(self):
        fin_path = os.path.join(settings.DATABASE_PATH, "financial", "financial_literacy.json")
        if os.path.exists(fin_path):
            try:
                with open(fin_path, "r", encoding="utf-8") as f:
                    self.fin_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading financial catalog: {e}")

    def find_matching_topics(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored = []

        triggers = {
            "FIN_SCALE_OF_FINANCE_CALCULATION": ["scale of finance", "limit calculation", "kcc formula", "5 year sanction", "dltc", "स्केल ऑफ फाइनेंस", "क्रेडिट लिमिट गणना", "அளவீட்டு முறை", "రుణ పరిమితి గణన"],
            "FIN_KCC_SCALE_OF_FINANCE": ["scale of finance", "limit calculation", "kcc formula", "5 year sanction", "dltc"],
            "FIN_INTEREST_SUBVENTION_4_PERCENT": ["4%", "4 percent", "interest subvention", "prompt repayment", "pri", "7%", "3%", "effective interest", "4 प्रतिशत ब्याज", "ब्याज छूट", "4 சதவீத வட்டி", "4 శాతం వడ్డీ"],
            "FIN_INTEREST_SUBVENTION_4PERCENT": ["4%", "4 percent", "interest subvention", "prompt repayment", "pri", "7%"],
            "FIN_TITLE_DEED_RELEASE_COMPENSATION": ["title deed", "no dues", "noc", "release documents", "5000 per day", "5,000", "penalty", "original documents", "land documents", "एनओसी", "टाइटिल डीड", "दस्तावेज़", "நோ டியூஸ்", "நில ஆவணம்", "నో డ్యూస్"],
            "FIN_FAIR_LENDING_15DAY_DOCS": ["title deed", "no dues", "noc", "release documents", "5000 per day"],
            "FIN_AEPS_MICRO_ATM_SAFETY": ["aeps", "micro atm", "biometric safety", "fingerprint scam", "two factor", "2fa", "माइक्रो एटीएम", "बायोमेट्रिक सुरक्षा", "கைரேகை பாதுகாப்பு"],
            "FIN_DBT_AADHAAR_SEEDING_VS_LINKING": ["npci mapper", "dbt seeding", "aadhaar seeding", "dbt failure", "apb", "डीबीटी सीडिंग", "एनपीसीआई", "டிபிடி இணைப்பு", "ఆధార్ సీడింగ్"],
            "FIN_NPCI_DBT_SEEDING": ["npci mapper", "dbt seeding", "aadhaar seeding", "dbt failure"],
            "FIN_CIBIL_CALAMITY_RESTRUCTURING": ["cibil", "credit score", "restructuring", "calamity loan", "moratorium", "npa", "ऋण पुनर्गठन", "सिबिल स्कोर", "கடன் மறுசீரமைப்பு"]
        }

        q_tokens = set(re.findall(r'\w+', q_lower))

        for item in self.fin_catalog:
            code = item.get("topic_code", "")
            kw_list = triggers.get(code, [])
            score = 0.0

            # 1. Trigger phrase match
            for kw in kw_list:
                if kw in q_lower:
                    score += 6.0 if " " in kw else 3.0

            # 2. Title & Code match
            title = (item.get("title", "") + " " + code).lower()
            if code.lower() in q_lower:
                score += 8.0
            for tok in q_tokens:
                if len(tok) > 2 and tok in title:
                    score += 2.0

            # 3. Summary & Breakdown match
            summary = item.get("summary", "").lower()
            for tok in q_tokens:
                if len(tok) > 3 and tok in summary:
                    score += 1.0

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

        return {
            "matched_topics": [t.get("title") for t in matched],
            "primary_topic": primary,
            "guidance_text": guidance_text,
            "citations": primary.get("citations", []),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_response(self, item: Dict[str, Any], language: str) -> str:
        title = item.get("title", "Credit & Financial Guidance")
        code = item.get("topic_code", "")
        summary = item.get("summary", "")
        citations = ", ".join(item.get("citations", []))

        # Check for Scale of Finance Breakdown
        if "formula_breakdown" in item:
            if language == "ta":
                return (
                    f"### 🧮 கிசான் கிரெடிட் கார்டு (KCC) கடன் வரம்பு கணக்கீட்டு முறை ({code})\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n"
                    f"மாவட்ட அளவிலான தொழில்நுட்பக் குழு (DLTC) நிர்ணயிக்கும் பயிர் சாகுபடி செலவு அடிப்படையில், விவசாயிகளுக்கு 5 ஆண்டுகளுக்கான சுழல் கடன் வரம்பு நிர்ணயிக்கப்படுகிறது.\n\n"
                    f"**📐 நிலையான கணக்கீட்டு சூத்திரங்கள்:**\n"
                    f"• **1-ஆம் ஆண்டு கடன் வரம்பு (Year 1 Limit)** = (பயிர் சாகுபடி பரப்பளவு × DLTC பயிர் செலவு) + வீட்டுச் செலவுகளுக்கு 10% + பயிர் பராமரிப்பு/காப்பீட்டிற்கு 20%.\n"
                    f"• **அடுத்தடுத்த ஆண்டுகள் (Years 2 to 5)** = ஒவ்வொரு ஆண்டும் 10% கடன் வரம்பு தானாக உயர்த்தப்படும்.\n"
                    f"• **5-ஆம் ஆண்டு மொத்த வரம்பு (5th Year Sanction Limit)** = 1-ஆம் ஆண்டு வரம்பு + 50% கூடுதல் வரம்பு.\n"
                    f"• **பிணையில்லா கடன் (Collateral-Free Limit)** = ₹1.60 லட்சம் வரை நில ஆவணம் அல்லது அடமானம் தேவையில்லை (RBI விதி).\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட நபார்டு (NABARD) & RBI வழிகாட்டுதல்கள்:** {citations}"
                )
            elif language == "hi":
                return (
                    f"### 🧮 किसान क्रेडिट कार्ड (KCC) ऋण सीमा गणना सूत्र ({code})\n\n"
                    f"**📌 सामान्य विवरण:**\n"
                    f"जिला स्तरीय तकनीकी समिति (DLTC) द्वारा निर्धारित स्केल ऑफ फाइनेंस के आधार पर किसानों को 5 वर्ष के लिए परिक्रामी साख सीमा (Revolving Credit Limit) स्वीकृत की जाती है।\n\n"
                    f"**📐 मानक गणना सूत्र:**\n"
                    f"• **प्रथम वर्ष की ऋण सीमा** = (फसल क्षेत्र × DLTC वित्त पैमाना) + 10% घरेलू उपभोग + 20% फसल कटाई एवं रखरखाव व्यय।\n"
                    f"• **द्वितीय से पंचम वर्ष** = प्रत्येक वर्ष लागत वृद्धि हेतु 10% की स्वचालित वृद्धि।\n"
                    f"• **5 वर्षीय कुल स्वीकृत सीमा** = प्रथम वर्ष की सीमा का 150%।\n"
                    f"• **जमानत-मुक्त सीमा (Collateral-Free Limit)** = ₹1.60 लाख तक बिना किसी भूमि बंधक के शून्य जमानत पर ऋण।\n\n"
                    f"🏛️ **सत्यापित नाबार्ड एवं आरबीआई दिशानिर्देश:** {citations}"
                )
            else:
                breakdown = "\n".join([f"  - {f}" for f in item["formula_breakdown"]])
                return (
                    f"### 🧮 {title} ({code})\n\n"
                    f"**Overview:**\n{summary}\n\n"
                    f"**📐 Standard Calculation Formulas:**\n{breakdown}\n\n"
                    f"🏛️ **Verified NABARD & RBI Standards:** {citations}"
                )

        # Check for Financial Mechanics (4% Interest Subvention MISS)
        elif "financial_mechanics" in item or code in ["FIN_INTEREST_SUBVENTION_4_PERCENT", "FIN_INTEREST_SUBVENTION_4PERCENT"]:
            if language == "ta":
                return (
                    f"### 💰 திருத்தப்பட்ட வட்டி மானியத் திட்டம் (MISS): 4% நிகர பயிர்க்கடன் வட்டி ({code})\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n"
                    f"மத்திய அரசின் வட்டி மானியத் திட்டத்தின் கீழ், விவசாயிகள் வங்கிகள் மற்றும் தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கங்கள் (PACS) மூலம் பெறும் **₹3.00 லட்சம் வரையிலான குறுகிய கால பயிர்க்கடன்களுக்கு ஆண்டுக்கு 4% மட்டுமே நிகர வட்டி** வசூலிக்கப்படுகிறது.\n\n"
                    f"**📊 ஒழுங்குபடுத்தப்பட்ட வட்டி விகிதங்கள் மற்றும் மானியங்கள்:**\n"
                    f"• **அடிப்படை கடன் வட்டி விகிதம் (Benchmark Lending Rate)**: வங்கிகள் மற்றும் PACS சங்கங்களின் சட்டப்பூர்வ கடன் வட்டி 7.00% ஆகும்.\n"
                    f"• **மத்திய அரசு வட்டி மானியம் (Base Subvention)**: மத்திய அரசு கடன் வழங்கும் வங்கிகளுக்கு 1.50% நேரடி வட்டி மானியம் வழங்குகிறது.\n"
                    f"• **சரியான நேரத்தில் திரும்பச் செலுத்தும் சலுகை (Prompt Repayment Incentive - PRI)**: கடன் பெற்ற 1 வருடத்திற்குள் கடனை திருப்பிச் செலுத்தும் விவசாயிகளுக்கு கூடுதலாக 3.00% வட்டி தள்ளுபடி வழங்கப்படுகிறது.\n"
                    f"• **விவசாயி செலுத்த வேண்டிய நிகர வட்டி (Net Effective Rate)**: 7.00% - 3.00% = **ஆண்டுக்கு 4.00% மட்டுமே** (அதிகபட்சம் ₹3.00 லட்சம் கடன் வரை).\n"
                    f"• **பிணையில்லா கடன் வரம்பு (Collateral-Free Limit)**: ₹1.60 லட்சம் வரையிலான கடன்களுக்கு எந்தவித நில ஆவணம் அல்லது அடமானமும் தேவையில்லை.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட RBI & மத்திய வேளாண் அமைச்சக அரசாணை:** {citations}"
                )
            elif language == "hi":
                return (
                    f"### 💰 संशोधित ब्याज अनुदान योजना (MISS): 4% प्रभावी फसल ऋण दर ({code})\n\n"
                    f"**📌 सामान्य विवरण:**\n"
                    f"केंद्र सरकार की संशोधित ब्याज अनुदान योजना के तहत किसानों को बैंकों एवं पैक्स (PACS) के माध्यम से **₹3.00 लाख तक का अल्पकालिक फसल ऋण मात्र 4% प्रति वर्ष की प्रभावी ब्याज दर** पर उपलब्ध कराया जाता है।\n\n"
                    f"**📊 विनियमित ब्याज दरें एवं अनुदान विवरण:**\n"
                    f"• **मानक ऋण ब्याज दर (Benchmark Lending Rate)**: बैंक/पैक्स 7.00% वार्षिक की वैधानिक दर पर ऋण स्वीकृत करते हैं।\n"
                    f"• **आधारभूत ब्याज अनुदान**: केंद्र सरकार वित्तीय संस्थाओं को 1.50% की प्रत्यक्ष ब्याज सब्सिडी देती है।\n"
                    f"• **समय पर पुनर्भुगतान प्रोत्साहन (PRI)**: 1 वर्ष की निर्धारित अवधि के भीतर ऋण चुकाने वाले किसानों को 3.00% की अतिरिक्त ब्याज छूट मिलती है।\n"
                    f"• **किसान के लिए प्रभावी शुद्ध ब्याज दर**: 7.00% - 3.00% = **मात्र 4.00% प्रति वर्ष** (अधिकतम ₹3.00 लाख ऋण सीमा)।\n"
                    f"• **जमानत-मुक्त सीमा (Collateral-Free Limit)**: ₹1.60 लाख तक के ऋण पर शून्य बंधक/जमानत का वैधानिक नियम लागू है।\n\n"
                    f"🏛️ **सत्यापित आरबीआई एवं कृषि मंत्रालय दिशानिर्देश:** {citations}"
                )
            else:
                mechanics = "\n".join([f"  - {m}" for m in item["financial_mechanics"]])
                return (
                    f"### 💰 {title} ({code})\n\n"
                    f"**Overview:**\n{summary}\n\n"
                    f"**📊 Regulated Interest Rates & Subventions:**\n{mechanics}\n\n"
                    f"🏛️ **Verified RBI & MoA&FW Directives:** {citations}"
                )

        # Check for Statutory Rules (e.g. Title Deed 15-30 days & ₹5,000/day penalty)
        elif "statutory_rules" in item:
            if language == "ta":
                return (
                    f"### ⚖️ கடன் முடிந்தவுடன் 15 நாட்களில் நில ஆவணங்களை திரும்பப் பெறும் உரிமை ({code})\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n"
                    f"விவசாயி முழு பயிர்க்கடனை திரும்பச் செலுத்திய **15 நாட்களுக்குள் அசல் நில ஆவணங்கள் மற்றும் தடையில்லா சான்றிதழை (NOC)** வங்கி திரும்ப வழங்க வேண்டும் என்று ரிசர்வ் வங்கி (RBI) உத்தரவிட்டுள்ளது.\n\n"
                    f"**📜 சட்டப்பூர்வ உரிமைகள் & ₹5,000/நாள் அபராத வழிகாட்டுதல்கள்:**\n"
                    f"• **15 நாள் காலக்கெடு**: கடன் கணக்கு முடிவடைந்த 15 நாட்களுக்குள் அனைத்து அசல் பத்திரங்களும் விடுவிக்கப்பட வேண்டும்.\n"
                    f"• **வங்கி மீதான இழப்பீடு**: 15 நாட்களுக்கு மேல் தாமதமாகும் ஒவ்வொரு நாளுக்கும் **நாளைக்கு ₹5,000 வீதம் விவசாயிக்கு வங்கி இழப்பீடு** வழங்க வேண்டும்.\n"
                    f"• **ஆவணம் தொலைந்தால் பொறுப்பு**: ஆவணம் தொலைந்தால் வங்கி தனது சொந்த செலவில் நகல் ஆவணம் பெற்றுத் தருவதுடன், 30 நாட்கள் கூடுதல் அவகாசத்திற்குப் பிறகு தினசரி ₹5,000 இழப்பீடு வழங்க வேண்டும்.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட RBI நியாயமான கடன் வழங்கல் வழிகாட்டுதல்கள்:** {citations}"
                )
            elif language == "hi":
                return (
                    f"### ⚖️ ऋण चुकता होने पर 15 दिनों में मूल दस्तावेज वापसी का अधिकार ({code})\n\n"
                    f"**📌 सामान्य विवरण:**\n"
                    f"आरबीआई के निष्पक्ष ऋण दिशा-निर्देशों के अनुसार ऋण पूर्ण चुकता होने के **15 दिनों के भीतर बैंक द्वारा मूल दस्तावेज एवं अनापत्ति प्रमाण पत्र (NOC)** लौटाना अनिवार्य है।\n\n"
                    f"**📜 वैधानिक अधिकार एवं ₹5,000/दिन मुआवजा निर्देश:**\n"
                    f"• **15 दिवसीय अनिवार्य समय-सीमा**: ऋण बंद होने के 15 दिनों में सभी चल/अचल संपत्ति के मूल दस्तावेज रिलीज करने होंगे।\n"
                    f"• **बैंक पर विलंब मुआवजा**: 15 दिनों के बाद विलंब होने पर बैंक द्वारा किसान को **₹5,000 प्रतिदिन की दर से क्षतिपूर्ति** का भुगतान किया जाएगा।\n"
                    f"• **दस्तावेज खोने पर उत्तरदायित्व**: दस्तावेज खोने पर बैंक अपने खर्च पर डुप्लीकेट दस्तावेज प्राप्त करेगा तथा अतिरिक्त विलंब पर मुआवजा देगा।\n\n"
                    f"🏛️ **सत्यापित आरबीआई फेयर लेंडिंग निर्देश:** {citations}"
                )
            else:
                rules = "\n".join([f"  - {r}" for r in item["statutory_rules"]])
                return (
                    f"### ⚖️ {title} ({code})\n\n"
                    f"**Overview:**\n{summary}\n\n"
                    f"**📜 Statutory Rights & Penalty Directives:**\n{rules}\n\n"
                    f"🏛️ **Verified RBI Fair Lending Directives:** {citations}"
                )

        # Check for Safety Norms (AePS)
        elif "safety_norms" in item:
            if language == "ta":
                return (
                    f"### 🔒 ஆதார் வழி பணப்பரிவர்த்தனை (AePS) மற்றும் மைக்ரோ-ஏடிஎம் பாதுகாப்பு ({code})\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n"
                    f"கிராமப்புறங்களில் பயோமெட்ரிக் கைரேகை மோசடிகளைத் தடுக்க, NPCI மற்றும் RBI வழிகாட்டுதல்களின்படி இரண்டு அடுக்கு பாதுகாப்பு முறை (2FA) அமல்படுத்தப்பட்டுள்ளது.\n\n"
                    f"**🛡️ பயோமெட்ரிக் மற்றும் மைக்ரோ-ஏடிஎம் பாதுகாப்பு விதிகள்:**\n"
                    f"• **முகவர் நேரடி சரிபார்ப்பு**: ஒவ்வொரு பரிவர்த்தனைக்கும் முன் சேவை மைய முகவர் தனது சொந்த பயோமெட்ரிக் பதிவை உறுதி செய்ய வேண்டும்.\n"
                    f"• **ஒருமுறை கைரேகை விதி**: வெற்றிகரமான ஒரே ஒரு பரிவர்த்தனைக்கு மட்டுமே ஒருமுறை கைரேகை வைக்க வேண்டும்; தோல்வியுற்றால் ரசீதை சரிபார்க்கவும்.\n"
                    f"• **கட்டாய ரசீது**: மைக்ரோ-ஏடிஎம் பரிவர்த்தனையின் போது அச்சிடப்பட்ட ரசீது அல்லது உடனடி எஸ்எம்எஸ் பெறுவது கட்டாயம்.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட NPCI & RBI பாதுகாப்பு விதிகள்:** {citations}"
                )
            elif language == "hi":
                return (
                    f"### 🔒 आधार सक्षम भुगतान प्रणाली (AePS) एवं माइक्रो-एटीएम सुरक्षा ({code})\n\n"
                    f"**📌 सामान्य विवरण:**\n"
                    f"ग्रामीण क्षेत्रों में बायोमेट्रिक क्लोनिंग एवं धोखाधड़ी की रोकथाम हेतु NPCI द्वारा अनिवार्य दो-चरणीय बायोमेट्रिक प्रमाणीकरण (2FA) लागू किया गया है।\n\n"
                    f"**🛡️ बायोमेट्रिक एवं माइक्रो-एटीएम सुरक्षा नियम:**\n"
                    f"• **व्यापार प्रतिनिधि का 2FA सत्यापन**: ग्राहक के लेनदेन से पूर्व बीसी/एजेंट का बायोमेट्रिक सत्यापन अनिवार्य है।\n"
                    f"• **एकल लेनदेन बायोमेट्रिक**: प्रति लेनदेन केवल एक बार फिंगरप्रिंट दें; दोहराव से बचें।\n"
                    f"• **अनिवार्य मुद्रित रसीद**: प्रत्येक निकासी के बाद तुरंत मुद्रित रसीद एवं बैंक बैलेंस एसएमएस प्राप्त करें।\n\n"
                    f"🏛️ **सत्यापित एनपीसीआई एवं आरबीआई सुरक्षा मानक:** {citations}"
                )
            else:
                norms = "\n".join([f"  - {s}" for s in item["safety_norms"]])
                return (
                    f"### 🔒 {title} ({code})\n\n"
                    f"**Overview:**\n{summary}\n\n"
                    f"**🛡️ Biometric & Micro-ATM Safety Rules:**\n{norms}\n\n"
                    f"🏛️ **Verified NPCI & RBI Directives:** {citations}"
                )

        # Check for Key Differences (DBT Seeding vs Linking)
        elif "key_differences" in item:
            if language == "ta":
                return (
                    f"### 🔄 அரசு மானியத்திற்கான NPCI ஆதார் மேப்பர் இணைப்பு (DBT Seeding) ({code})\n\n"
                    f"**📌 பொதுவான விளக்கம்:**\n"
                    f"வங்கி கணக்கில் ஆதார் இணைப்பது (Aadhaar Linking) வேறு; அரசின் PM-KISAN, பயிர் காப்பீடு போன்ற நேரடி பணப்பரிமாற்றம் (DBT) பெற **NPCI மேப்பரில் ஆதார் விதைப்பு (Aadhaar Seeding)** செய்வது கட்டாயமாகும்.\n\n"
                    f"**🔍 நேரடி பயன் பரிமாற்றம் (DBT) முக்கிய வழிகாட்டுதல்கள்:**\n"
                    f"• **ஆதார் இணைப்பு (Linking)**: வங்கி கணக்குடன் கேஒய்சி (KYC) செய்வதற்கு மட்டுமே பயன்படுகிறது.\n"
                    f"• **ஆதார் விதைப்பு (NPCI Seeding)**: அரசு அனுப்பும் பணம் தானாக வந்து சேர NPCI சர்வரில் ஒரு வங்கிக் கணக்கு முன்னுரிமை பெற்றிருக்க வேண்டும்.\n"
                    f"• **நிலை சரிபார்ப்பு**: UIDAI இணையதளத்தில் அல்லது உங்கள் வங்கி கிளையில் DBT Seeding Status சரிபார்க்கலாம்.\n\n"
                    f"🏛️ **சரிபார்க்கப்பட்ட NPCI & நிதி அமைச்சக நெறிமுறைகள்:** {citations}"
                )
            elif language == "hi":
                return (
                    f"### 🔄 डीबीटी हेतु एनपीसीआई आधार सीडिंग बनाम लिंकिंग ({code})\n\n"
                    f"**📌 सामान्य विवरण:**\n"
                    f"बैंक खाते में केवल आधार जोड़ना (Linking) पर्याप्त नहीं है; पीएम-किसान एवं बीमा जैसी सरकारी सब्सिडी प्राप्त करने के लिए **एनपीसीआई आधार मैपर पर सीडिंग (DBT Seeding)** अनिवार्य है।\n\n"
                    f"**🔍 प्रत्यक्ष लाभ अंतरण (DBT) मुख्य दिशानिर्देश:**\n"
                    f"• **आधार लिंकिंग**: केवल बैंक स्तर पर केवाईसी पहचान हेतु प्रयुक्त होती है।\n"
                    f"• **आधार सीडिंग (NPCI Mapping)**: आधार भुगतान ब्रिज (APB) के माध्यम से सरकारी सब्सिडी सीधे खाते में अंतरित होती है।\n"
                    f"• **सीडिंग स्थिति जांच**: myaadhaar.uidai.gov.in पर जाकर 'Bank Seeding Status' सत्यापित करें।\n\n"
                    f"🏛️ **सत्यापित एनपीसीआई एवं वित्त मंत्रालय दिशानिर्देश:** {citations}"
                )
            else:
                diffs = "\n".join([f"  - {d}" for d in item["key_differences"]])
                return (
                    f"### 🔄 {title} ({code})\n\n"
                    f"**Overview:**\n{summary}\n\n"
                    f"**🔍 Direct Benefit Transfer (DBT) Directives:**\n{diffs}\n\n"
                    f"🏛️ **Verified NPCI & MoF Guidelines:** {citations}"
                )

        # Default fallback
        if language == "ta":
            return (
                f"### 💳 {title} ({code})\n\n"
                f"**📌 பொதுவான விளக்கம்:**\n{summary}\n\n"
                f"🏛️ **சரிபார்க்கப்பட்ட அரசு மற்றும் நிதி ஆதாரங்கள்:** {citations}"
            )
        elif language == "hi":
            return (
                f"### 💳 {title} ({code})\n\n"
                f"**📌 सामान्य विवरण:**\n{summary}\n\n"
                f"🏛️ **सत्यापित आधिकारिक वित्तीय स्रोत:** {citations}"
            )
        else:
            return (
                f"### 💳 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"🏛️ **Verified Financial Sources:** {citations}"
            )
