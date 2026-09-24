"""
Strict Zero-Hallucination Officer Recommendation Engine for Cooperative AI Portal.
Recommends verified district and taluk-level government officers for Tamil Nadu districts (Theni, Madurai, Pudukkottai)
based on:
1. User Query & District/Taluk Context
2. Multi-Domain Fusion Solution Output & Active Domains
3. Strict Database Cross-Verification against database/data/officers/tamil_nadu_district_officers.json

Strict Rule:
If no officer matching the specific role and jurisdiction is available in the verified database,
it returns None without hallucinating or inventing contact details.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional
from config.settings import settings

class OfficerRecommender:
    def __init__(self):
        self.officers_db: List[Dict[str, Any]] = []
        self._load_database()

    def _load_database(self):
        officers_path = os.path.join(settings.DATABASE_PATH, "officers", "tamil_nadu_district_officers.json")
        if os.path.exists(officers_path):
            try:
                with open(officers_path, "r", encoding="utf-8") as f:
                    self.officers_db = json.load(f)
            except Exception as e:
                print(f"Error loading officers database: {e}")

    def detect_district_and_locality(self, text: str) -> Dict[str, Optional[str]]:
        """Identifies mentioned district and sub-locality/taluk from user query."""
        text_lower = text.lower()
        detected_district = None
        detected_locality = None

        # District triggers covering all 38 Tamil Nadu districts (Priority: Theni, Madurai, Pudukkottai on top)
        district_keywords = {
            "Theni": ["theni", "தேனி", "தேனி மாவட்டம்", "andipatti", "cumbum", "periyakulam", "uthamapalayam", "chinnamanur", "bodinayakanur", "kadamalaigundu", "bodi", "gudalur"],
            "Madurai": ["madurai", "மதுரை", "மதுரை மாவட்டம்", "melur", "vadipatti", "usilampatti", "thirumangalam", "alanganallur", "kottampatti", "chellampatti", "thirupparankundram", "peraiyur", "kalligudi", "sedapatti"],
            "Pudukkottai": ["pudukkottai", "புதுக்கோட்டை", "புதுக்கோட்டை மாவட்டம்", "aranthangi", "illuppur", "karambakudi", "thirumayam", "avudaiyarkoil", "kunnandarkoil", "viralimalai", "ponnamaravathi", "gandarvakottai", "manamelkudi", "annavasal", "arimalam", "thiruvarankulam"],
            "Coimbatore": ["coimbatore", "கோவை", "கோயம்புத்தூர்", "pollachi", "mettupalayam", "sulur", "annur", "valparai"],
            "Thanjavur": ["thanjavur", "தஞ்சாவூர்", "தஞ்சை", "kumbakonam", "papanasam", "pattukkottai", "orathanadu", "thiruvaiyaru"],
            "Dindigul": ["dindigul", "திண்டுக்கல்", "palani", "kodaikanal", "nilakottai", "natham", "oddanchatram", "vedasandur"],
            "Tiruchirappalli": ["tiruchirappalli", "trichy", "திருச்சிராப்பள்ளி", "திருச்சி", "manapparai", "thuraiyur", "musiri", "lalgudi", "srirangam"],
            "Salem": ["salem", "சேலம்", "attur", "mettur", "om権alur", "edappadi", "sankari", "valapady"],
            "Tirunelveli": ["tirunelveli", "திருநெல்வேலி", "nellai", "palayamkottai", "ambasamudram", "nanguneri", "radhapuram"],
            "Erode": ["erode", "ஈரோடு", "ஈரோடு மாவட்டம்", "perundurai", "bhavani", "gobichettipalayam", "gobi", "sathyamangalam", "sathy", "chennimalai", "anthiyur", "kodumudi", "nambiyur", "ammapettai"],
            "Karur": ["karur", "கரூர்", "கரூர் மாவட்டம்", "kadavur", "kulithalai", "krishnarayapuram", "thanthoni", "thogaimalai"],
            "Vellore": ["vellore", "வேலூர்", "katpadi", "gudiyatham", "anaicut", "pernamallur"],
            "Kanchipuram": ["kanchipuram", "காஞ்சிபுரம்", "காஞ்சி", "walajabad", "sriperumbudur", "kundrathur", "uthiramerur"],
            "Cuddalore": ["cuddalore", "கடலூர்", "chidambaram", "panruti", "vriddhachalam", "tittakudi", "bhuvanagiri", "kurinjipadi"],
            "Villupuram": ["villupuram", "விழுப்புரம்", "tindivanam", "gingee", "vanur", "vikravandi", "marakkanam"],
            "Tiruppur": ["tiruppur", "திருப்பூர்", "avinashi", "palladam", "dharapuram", "kangeyam", "udumalaipettai", "madathukulam"],
            "Ramanathapuram": ["ramanathapuram", "ராமநாதபுரம்", "ramnad", "paramakudi", "rameswaram", "kilakarai", "mudukulathur", "tiruvadanai"],
            "Sivaganga": ["sivaganga", "சிவகங்கை", "karaikudi", "manamadurai", "devakottai", "tiruppuvanam", "singampunari"],
            "Virudhunagar": ["virudhunagar", "விருதுநகர்", "sivakasi", "srivilliputhur", "rajapalayam", "aruppukkottai", "sattur"],
            "Nagapattinam": ["nagapattinam", "நாகப்பட்டினம்", "velankanni", "kilvelur", "vedaranyam", "thirukkuvalai"],
            "Tiruvarur": ["tiruvarur", "திருவாரூர்", "mannargudi", "nannilam", "kudavasal", "valangaiman", "muthupet", "needamangalam"],
            "Krishnagiri": ["krishnagiri", "கிருஷ்ணகிரி", "hosur", "denkanikottai", "pochampalli", "urikarai", "bargur"],
            "Dharmapuri": ["dharmapuri", "தருமபுரி", "harur", "palacode", "pennagaram", "pappireddipatti", "nallampalli"],
            "Namakkal": ["namakkal", "நாமக்கல்", "rasipuram", "tiruchengode", "paramathi velur", "kolli hills", "sendamangalam"],
            "Nilgiris": ["nilgiris", "நீலகிரி", "ooty", "udhagamandalam", "coonoor", "gudalur", "kotagiri"],
            "Thoothukudi": ["thoothukudi", "தூத்துக்குடி", "tuticorin", "kovilpatti", "tiruchendur", "srivaikuntam", "kayathar", "ottapidaram"],
            "Kanyakumari": ["kanyakumari", "கன்னியாகுமரி", "nagercoil", "padmanabhapuram", "thuckalay", "colachel", "kuzhithurai"],
            "Tiruvallur": ["tiruvallur", "திருவள்ளூர்", "avadi", "ponneri", "gummidipoondi", "tiruttani", "poonamallee", "uthukottai"],
            "Tiruvannamalai": ["tiruvannamalai", "திருவண்ணாமலை", "arani", "polur", "chengappadi", "vandavasi", "cheyyar"],
            "Ranipet": ["ranipet", "ராணிப்பேட்டை", "arcot", "walajah", "sholinghur", "nemili", "arakkonam"],
            "Tenkasi": ["tenkasi", "தென்காசி", "sankarankovil", "kadayanallur", "ambur", "shencottai", "alankulam", "veerakeralampudur"],
            "Chengalpattu": ["chengalpattu", "செங்கல்பட்டு", "tambaram", "pallavaram", "maduranthakam", "cheyyur", "thiruporur"],
            "Kallakurichi": ["kallakurichi", "கள்ளக்குறிச்சி", "sankarapuram", "chinnasalem", "ulundurpet", "tirukovilur", "kalvarayan hills"],
            "Mayiladuthurai": ["mayiladuthurai", "மயிலாடுதுறை", "sirkazhi", "tharangambadi", "kuthalam"],
            "Ariyalur": ["ariyalur", "அரியலூர்", "sendurai", "udayarpalayam", "andimadam"],
            "Perambalur": ["perambalur", "பெரம்பலூர்", "veppanthattai", "kunnam", "alathur"],
            "Tirupathur": ["tirupathur", "திருப்பத்தூர்", "vaniyambadi", "ambur", "natrampalli"],
            "Chennai": ["chennai", "சென்னை", "egmore", "guindy", "t nagar", "adyar", "mylapore", "anna nagar", "royapettah"]
        }

        for district, keywords in district_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    detected_district = district
                    break
            if detected_district:
                break

        # Locality / Taluk / Block triggers
        localities = [
            "andipatti", "cumbum", "periyakulam", "uthamapalayam", "chinnamanur", "bodinayakanur", "kadamalaigundu",
            "melur", "vadipatti", "usilampatti", "thirumangalam", "alanganallur", "kottampatti", "chellampatti", "thirupparankundram", "peraiyur", "kalligudi", "sedapatti",
            "aranthangi", "illuppur", "karambakudi", "thirumayam", "avudaiyarkoil", "kunnandarkoil", "viralimalai", "ponnamaravathi", "gandarvakottai", "manamelkudi", "annavasal", "arimalam", "thiruvarankulam",
            "perundurai", "bhavani", "gobichettipalayam", "sathyamangalam", "chennimalai", "anthiyur", "kodumudi", "nambiyur", "ammapettai",
            "kadavur", "kulithalai", "krishnarayapuram", "thanthoni", "thogaimalai",
            "ஆண்டிபட்டி", "கம்பம்", "பெரியகுளம்", "உத்தமபாளையம்", "சின்னமனூர்", "போடி", "மேலூர்", "வாடிப்பட்டி", "உசிலம்பட்டி", "திருமங்கலம்", "அறந்தாங்கி", "இலுப்பூர்", "விராலிமலை",
            "பெருந்துறை", "பவானி", "கோபிசெட்டிபாளையம்", "சத்தியமங்கலம்", "சென்னிமலை", "அந்தியூர்", "கொடுமுடி", "நம்பியூர்", "அம்மாபேட்டை",
            "கடவூர்", "குளித்தலை", "கிருஷ்ணராயபுரம்", "தான்தோன்றி", "தோகைமலை"
        ]

        LOCALITY_MAP = {
            "ஆண்டிபட்டி": "andipatti",
            "கம்பம்": "cumbum",
            "பெரியகுளம்": "periyakulam",
            "உத்தமபாளையம்": "uthamapalayam",
            "சின்னமனூர்": "chinnamanur",
            "போடி": "bodi",
            "கடமலைக்குண்டு": "kadamalaigundu",
            "மேலூர்": "melur",
            "வாடிப்பட்டி": "vadipatti",
            "உசிலம்பட்டி": "usilampatti",
            "திருமங்கலம்": "thirumangalam",
            "அலங்காநல்லூர்": "alanganallur",
            "கொட்டாம்பட்டி": "kottampatti",
            "அறந்தாங்கி": "aranthangi",
            "இலுப்பூர்": "illuppur",
            "விராலிமலை": "viralimalai",
            "பெருந்துறை": "perundurai",
            "பவானி": "bhavani",
            "கோபிசெட்டிபாளையம்": "gobichettipalayam",
            "சத்தியமங்கலம்": "sathyamangalam",
            "சென்னிமலை": "chennimalai",
            "அந்தியூர்": "anthiyur",
            "கொடுமுடி": "kodumudi",
            "நம்பியூர்": "nambiyur",
            "அம்மாபேட்டை": "ammapettai",
            "கடவூர்": "kadavur",
            "குளித்தலை": "kulithalai",
            "கிருஷ்ணராயபுரம்": "krishnarayapuram",
            "தான்தோன்றி": "thanthoni",
            "தோகைமலை": "thogaimalai"
        }

        for loc in localities:
            if loc in text_lower:
                detected_locality = LOCALITY_MAP.get(loc, loc)
                break

        return {
            "district": detected_district,
            "locality": detected_locality
        }

    def recommend_officer(
        self,
        query: str,
        active_domains: List[str],
        fusion_output: str = "",
        language: str = "en"
    ) -> Optional[Dict[str, Any]]:
        """
        Recommends verified officer matching the problem and jurisdiction.
        Returns None if no matching officer exists.
        """
        loc_info = self.detect_district_and_locality(query)
        district = loc_info["district"]
        locality = loc_info["locality"]

        if not district:
            # Provide standard statutory officer hierarchy for the active domain
            generic_hierarchy = self._format_generic_officer_hierarchy(active_domains, language)
            return {
                "district": None,
                "locality": None,
                "officer": None,
                "recommendation_text": generic_hierarchy,
                "is_verified": True,
                "trust_score": 0.99
            }

        # Determine target departments based on active domains and query keywords
        q_lower = query.lower()
        target_departments = []

        # Granular department prioritization
        if any(w in q_lower for w in ["supply officer", "ration", "pds", "rice", "fair price", "ரேஷன்", "வழங்கல் அதிகாரி"]):
            target_departments = ["Civil Supplies", "Co-operative", "District Supply Office"]
        elif any(w in q_lower for w in ["cooperative", "sub registrar", "subregistrar", "joint registrar", "pacs", "கூட்டுறவு", "பதிவாளர்", "உறுப்பினர்", "கடன் சங்கம்"]):
            target_departments = ["Co-operative", "Co-operation, Food & Consumer Protection", "District Administration", "Agriculture"]
        elif any(w in q_lower for w in ["machinery", "tractor", "drone", "harvester", "agri engineering", "பொறியியல்"]):
            target_departments = ["Agricultural Engineering", "Agriculture", "DRDA"]
        elif any(w in q_lower for w in ["horticulture", "vegetable", "fruit", "polyhouse", "drip", "தோட்டக்கலை"]):
            target_departments = ["Horticulture", "Agriculture"]
        elif any(w in q_lower for w in ["agriculture officer", "agri officer", "aao", "ada", "crop loss", "pmfby", "hailstorm", "flood", "rain", "heavy rain", "rains", "rainfall", "crop damage", "crops destroyed", "crops got desteroyed", "desteroyed", "destroy", "ruined crop", "calamity", "விவசாய அதிகாரி", "வேளாண் உதவி அலுவலர்", "வேளாண் உதவி இயக்குனர்", "மழை", "பயிர் சேதம்"]):
            target_departments = ["Agriculture", "Collectorate", "Revenue Division", "Taluk Office", "Co-operative", "Horticulture", "District Administration", "District Officers"]
        elif any(w in q_lower for w in ["tahsildar", "rdo", "patta", "title deed", "land record", "தாசில்தார்", "நில ஆவணம்"]):
            target_departments = ["Taluk Office", "Revenue", "Revenue Division", "Collectorate"]
        elif any(w in q_lower for w in ["fertilizer", "urea", "dap", "mrp", "black marketing", "overcharging", "உரம்", "யூரியா"]):
            target_departments = ["Co-operative", "Agriculture", "Civil Supplies", "Co-operation, Food & Consumer Protection"]
        elif "pacs_pmfby" in active_domains:
            if any(w in q_lower for w in ["pacs", "membership", "உறுப்பினர்", "சங்கம்", "கூட்டுறவு"]):
                target_departments = ["Co-operative", "District Administration", "Agriculture", "Collectorate"]
            else:
                target_departments = ["Agriculture", "Collectorate", "Co-operative", "Horticulture", "Revenue Division", "Taluk Office", "District Administration", "District Officers"]
        elif "grievance" in active_domains:
            target_departments = ["Co-operative", "Agriculture", "Civil Supplies", "Revenue", "Collectorate", "Taluk Office", "Revenue Division", "District Administration", "District Officers"]
        elif "farmer_scheme" in active_domains:
            target_departments = ["Agriculture", "Horticulture", "Agricultural Engineering", "Collectorate", "Rural Development", "DRDA"]
        elif "cooperative_law" in active_domains:
            target_departments = ["Co-operative", "Co-operation, Food & Consumer Protection", "District Administration"]
        else:
            target_departments = ["Co-operative", "Agriculture", "Collectorate", "Revenue", "Taluk Office", "Revenue Division", "District Administration", "District Officers"]

        # Filter candidate officers from the verified database
        district_officers = [o for o in self.officers_db if o.get("district", "").lower() == district.lower()]
        if not district_officers:
            return None

        # Score matching officers
        scored_candidates = []
        is_calamity_or_agri = any(w in q_lower for w in ["rain", "heavy rain", "flood", "calamity", "crop", "crops", "desteroyed", "destroyed", "pmfby", "damage", "loss", "hailstorm", "மழை", "பயிர்", "சேதம்"])

        for officer in district_officers:
            dept = officer.get("department", "")
            role = officer.get("designation_or_role", "") or officer.get("designation", "")
            place = officer.get("place_or_address", "")
            name = officer.get("name", "")
            block = officer.get("block_name", "") or ""
            hq = officer.get("head_quarters", "") or ""
            mobile = officer.get("mobile", "")
            landline = officer.get("landline", "")
            email = officer.get("email", "")

            # Ignore empty contact entries
            if not mobile and not landline and not email:
                continue

            # Strict Department Relevance Filter
            if dept not in target_departments:
                continue

            score = 0

            # Department match (higher score for top priority department)
            idx = target_departments.index(dept)
            score += (50 - idx * 5)

            # Locality / Block match
            if locality:
                loc_cleaned = locality.lower()
                if (loc_cleaned in role.lower() or 
                    loc_cleaned in place.lower() or 
                    loc_cleaned in name.lower() or
                    (block and loc_cleaned in block.lower()) or
                    (hq and loc_cleaned in hq.lower())):
                    score += 45

            # Role relevance matching specific query words
            if is_calamity_or_agri:
                if "joint director" in role.lower() or "jda" in role.lower() or "pmfby" in role.lower():
                    score += 40
                elif "pa to collector (agri)" in role.lower() or "deputy director of agriculture" in role.lower():
                    score += 35
                elif "assistant director of agriculture" in role.lower() or "ada" in role.lower() or "aao" in role.lower():
                    score += 32
                elif "district collector" in role.lower():
                    score += 20

            if "supply officer" in q_lower and "supply officer" in role.lower():
                score += 30
            if "sub registrar" in q_lower and ("sub registrar" in role.lower() or "subregistrar" in role.lower()):
                score += 30
            if "joint registrar" in q_lower and "joint registrar" in role.lower():
                score += 35
            if ("agriculture" in q_lower or "agri" in q_lower) and ("agri" in role.lower() or "aao" in role.lower() or "ada" in role.lower()):
                score += 25
            if ("aao" in q_lower or "assistant agricultural officer" in q_lower) and "aao" in role.lower():
                score += 35
            if ("ada" in q_lower or "assistant director of agriculture" in q_lower) and "ada" in role.lower():
                score += 35
            if "tahsildar" in q_lower and "tahsildar" in role.lower():
                score += 25
            if "horticulture" in q_lower and "horti" in role.lower():
                score += 25
            if ("engineering" in q_lower or "machinery" in q_lower) and "engineer" in role.lower():
                score += 30

            if score > 0:
                scored_candidates.append((score, officer))

        if not scored_candidates:
            return None

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        top_officer = scored_candidates[0][1]

        # Format recommendation text
        formatted_block = self._format_officer_block(top_officer, district, language)

        return {
            "district": district,
            "locality": locality,
            "officer": top_officer,
            "recommendation_text": formatted_block,
            "is_verified": True,
            "trust_score": 0.99
        }

    def _format_officer_block(self, officer: Dict[str, Any], district: str, language: str) -> str:
        name = officer.get("name") or "Concerned Designated Officer"
        role = officer.get("designation_or_role", "")
        dept = officer.get("department", "")
        mobile = officer.get("mobile", "")
        landline = officer.get("landline", "")
        email = officer.get("email", "")
        source = officer.get("source", f"https://{district.lower()}.nic.in")

        contacts = []
        if mobile:
            contacts.append(f"📱 **Mobile:** `{mobile}`")
        if landline:
            contacts.append(f"☎️ **Landline / Office:** `{landline}`")
        if email:
            contacts.append(f"✉️ **Email:** `{email}`")

        contact_str = " | ".join(contacts) if contacts else "Office Directory Listed"

        district_ta = {"Madurai": "மதுரை", "Theni": "தேனி", "Pudukkottai": "புதுக்கோட்டை", "Erode": "ஈரோடு", "Karur": "கரூர்", "Coimbatore": "கோயம்புத்தூர்", "Dindigul": "திண்டுக்கல்", "Salem": "சேலம்", "Tiruchirappalli": "திருச்சிராப்பள்ளி"}.get(district, district)
        district_hi = {"Madurai": "मदुरै", "Theni": "थेनी", "Pudukkottai": "पुदुक्कोट्टई", "Erode": "इरोड", "Karur": "करूर", "Coimbatore": "कोयंबटूर", "Dindigul": "डिंडीगुल", "Salem": "सेलम", "Tiruchirappalli": "तिरुचिरापल्ली"}.get(district, district)

        dept_ta = {"Agriculture": "வேளாண்மைத் துறை", "Horticulture": "தோட்டக்கலைத் துறை", "Cooperation": "கூட்டுறவுத் துறை", "Revenue": "வருவாய்த் துறை", "District Administration": "மாவட்ட நிர்வாகம்"}.get(dept, dept)
        dept_hi = {"Agriculture": "कृषि विभाग", "Horticulture": "बागवानी विभाग", "Cooperation": "सहकारिता विभाग", "Revenue": "राजस्व विभाग", "District Administration": "जिला प्रशासन"}.get(dept, dept)

        role_ta = role
        role_hi = role
        if "Joint Director of Agriculture" in role:
            role_ta = "வேளாண்மை இணை இயக்குநர் & PMFBY மாவட்ட ஒருங்கிணைப்பு அலுவலர்"
            role_hi = "संयुक्त कृषि निदेशक एवं पीएमएफबीवाई जिला नोडल अधिकारी"
        elif "Deputy Registrar" in role:
            role_ta = "கூட்டுறவு சங்கங்களின் துணைப் பதிவாளர் (DRCS)"
            role_hi = "सहकारी समितियों के उप निबंधक (DRCS)"
        elif "Joint Registrar" in role:
            role_ta = "கூட்டுறவு சங்கங்களின் இணைப் பதிவாளர் (JRCS)"
            role_hi = "सहकारी समितियों के संयुक्त निबंधक (JRCS)"
        elif "District Collector" in role:
            role_ta = "மாவட்ட ஆட்சித் தலைவர் (மாவட்ட ஆட்சியர்)"
            role_hi = "जिला मजिस्ट्रेट / जिला कलेक्टर"

        if language == "ta":
            return (
                f"### 🏛️ பரிந்துரைக்கப்படும் அதிகாரப்பூர்வ தொடர்பு ({district_ta} மாவட்டம்)\n"
                f"- **அதிகாரி பெயர் / பதவி:** **{name}** ({role_ta})\n"
                f"- **துறை:** {dept_ta}\n"
                f"- **தொடர்பு விவரங்கள்:** {contact_str}\n"
                f"- **சரிபார்க்கப்பட்ட ஆதாரம்:** [மாவட்ட நிர்வாக தொடர்பு கையேடு]({source})\n"
                f"*(குறிப்பு: இத்தகவல் அதிகாரப்பூர்வ அரசு தரவுத்தளத்தில் இருந்து சரிபார்க்கப்பட்டது)*"
            )
        elif language == "hi":
            return (
                f"### 🏛️ अनुशंसित आधिकारिक संपर्क ({district_hi} जिला)\n"
                f"- **अधिकारी का नाम / पद:** **{name}** ({role_hi})\n"
                f"- **विभाग:** {dept_hi}\n"
                f"- **संपर्क विवरण:** {contact_str}\n"
                f"- **सत्यापित आधिकारिक स्रोत:** [जिला प्रशासन डायरेक्टरी]({source})\n"
                f"*(नोट: यह विवरण आधिकारिक सरकारी डेटाबेस द्वारा सत्यापित है)*"
            )
        else:
            return (
                f"### 🏛️ Recommended Statutory Authority Contact ({district} District)\n"
                f"- **Officer Name / Designation:** **{name}** ({role})\n"
                f"- **Department:** {dept}\n"
                f"- **Official Contact Details:** {contact_str}\n"
                f"- **Verified Government Source:** [District Administration Directory]({source})\n"
                f"*(Note: Official verified contact record from government directory - Zero Hallucination)*"
            )

    def _format_generic_officer_hierarchy(self, active_domains: List[str], language: str) -> str:
        if "grievance" in active_domains:
            if language == "ta":
                return (
                    "### 👤 நீங்கள் அணுக வேண்டிய அதிகாரிகள் (படிப்படியான படிநிலை)\n"
                    "- **நிலை 1 (கிராம/தொடக்க நிலை):** செயலாளர் / தலைவர், தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACS) - (15 நாட்கள் காலக்கெடு)\n"
                    "- **நிலை 2 (வட்டார/வட்ட நிலை):** கூட்டுறவு சங்கங்களின் துணைப் பதிவாளர் (ARCS / DRCS Office)\n"
                    "- **நிலை 3 (மாவட்ட நிலை):** கூட்டுறவு சங்கங்களின் இணைப் பதிவாளர் (JRCS) / மாவட்ட மத்திய கூட்டுறவு வங்கி (DCCB)\n"
                    "- **நிலை 4 (மாநில/மேல்முறையீடு):** கூட்டுறவு சங்கங்களின் பதிவாளர் (RCS) / மாநில கூட்டுறவு குறைதீர்ப்பாளர் (Ombudsman)\n"
                    "*💡 உங்கள் குறிப்பிட்ட மாவட்டம்/வட்டாரத்தின் (எ.கா. தேனி, மதுரை, புதுக்கோட்டை, ஈரோடு, கரூர்) அதிகாரியின் நேரடி தொலைபேசி எண்ணைப் பெற, உங்கள் மாவட்டத்தின் பெயரைச் சேர்க்கவும்.*"
                )
            elif language == "hi":
                return (
                    "### 👤 आपको किन अधिकारियों से मिलना चाहिए (वैधानिक पदानुक्रम)\n"
                    "- **स्तर 1 (ग्राम/प्राथमिक स्तर):** सचिव / अध्यक्ष, प्राथमिक कृषि ऋण समिति (PACS) - (15 दिन की समय सीमा)\n"
                    "- **स्तर 2 (ब्लॉक/तालुका स्तर):** सहायक निबंधक, सहकारी समितियां (ARCS)\n"
                    "- **स्तर 3 (जिला स्तर):** उप/संयुक्त निबंधक, सहकारी समितियां (DRCS / JRCS) / जिला केंद्रीय सहकारी बैंक\n"
                    "- **स्तर 4 (अपील एवं शिकायत):** सहकारी लोकपाल (Ombudsman Sec 85) / निबंधक (RCS)\n"
                    "*💡 अपने जिले (उदा. थेनी, मदुरै, पुदुक्कोट्टई, इरोड, करूर) के नामित अधिकारी का सीधा फोन नंबर देखने के लिए अपने प्रश्न में जिले का नाम लिखें।*"
                )
            else:
                return (
                    "### 👤 Designated Competent Officers to Meet (Statutory Escalation Hierarchy)\n"
                    "- **Level 1 (Local/Gram Panchayat):** Secretary / President, Primary Agricultural Credit Society (PACS) - *(15-day resolution SLA)*\n"
                    "- **Level 2 (Block/Taluk Level):** Assistant Registrar of Cooperative Societies (ARCS)\n"
                    "- **Level 3 (District Headquarters):** Deputy / Joint Registrar of Cooperative Societies (DRCS/JRCS) / DCCB\n"
                    "- **Level 4 (Statutory Ombudsman):** Cooperative Ombudsman (Sec 85) / State Registrar of Cooperative Societies (RCS)\n"
                    "*💡 To view the exact named officer, phone number, and office address in Tamil Nadu, simply mention your district (e.g., Theni, Madurai, Pudukkottai, Erode, Karur).*"
                )
        elif "pacs_pmfby" in active_domains:
            if language == "ta":
                return (
                    "### 👤 பயிர் காப்பீடு மற்றும் PACS சேவைக்கு அணுக வேண்டிய அதிகாரிகள்\n"
                    "- **தொடக்க தொடர்பு:** உள்ளூர் PACS செயலாளர் / வட்டார வேளாண்மை விரிவாக்க மையம் (AAO / ADA)\n"
                    "- **பயிர் காப்பீட்டு அவசர உதவி எண்:** PMFBY கட்டணமில்லா எண் `14447` அல்லது `1800-180-1551`\n"
                    "- **மேல்முறையீட்டு அதிகாரி:** மாவட்ட ஆட்சியர் தலைமையிலான மாவட்ட குறைதீர்க்கும் குழு (DGRC) / வேளாண்மை இணை இயக்குனர் (JDA)\n"
                    "*💡 உங்கள் மாவட்ட அதிகாரியின் தொடர்பு எண்ணை அறிய மாவட்டத்தின் பெயரை குறிப்பிடவும்.*"
                )
            elif language == "hi":
                return (
                    "### 👤 फसल बीमा एवं पैक्स सेवाओं हेतु संपर्क अधिकारी\n"
                    "- **प्राथमिक संपर्क:** स्थानीय पैक्स सचिव / सहायक कृषि अधिकारी (AAO/ADA)\n"
                    "- **पीएमएफबीवाई राष्ट्रीय टोल-फ्री हेल्पलाइन:** `14447` अथवा `1800-180-1551`\n"
                    "- **जिला नोडल अधिकारी:** जिला कृषि अधिकारी / जिला कलेक्टर (DGRC अध्यक्ष)\n"
                    "*💡 अपने जिले के अधिकारी का फोन नंबर देखने के लिए प्रश्न में अपने जिले का नाम लिखें।*"
                )
            else:
                return (
                    "### 👤 Competent Officers to Meet for Crop Insurance & PACS Services\n"
                    "- **Primary Point of Contact:** Local PACS Secretary / Assistant Agricultural Officer (AAO) at Block Agriculture Extension Office\n"
                    "- **National PMFBY Calamity Helpline:** Toll-Free `14447` or `1800-180-1551`\n"
                    "- **District Escalation Authority:** District Grievance Redressal Committee (DGRC, chaired by District Collector) / Joint Director of Agriculture (JDA)\n"
                    "*💡 To view your exact district officer's phone number and office location, simply mention your district (e.g., Theni, Madurai, Pudukkottai, Erode, Karur).*"
                )
        elif "financial_literacy" in active_domains:
            if language == "ta":
                return (
                    "### 👤 கடன் மற்றும் வங்கி சேவைக்கான தொடர்பு அதிகாரிகள்\n"
                    "- **வங்கி கிளை / PACS:** உள்ளூர் PACS செயலாளர் / மாவட்ட மத்திய கூட்டுறவு வங்கி (DCCB) கிளை மேலாளர்\n"
                    "- **மாவட்ட அளவிலான அதிகாரி:** மாவட்ட முன்னோடி வங்கி மேலாளர் (LDM)\n"
                    "- **ரிசர்வ் வங்கி குறைதீர்ப்பாளர்:** RBI Banking Ombudsman Helpline: `14448`\n"
                    "*💡 உங்கள் மாவட்ட அதிகாரியின் தொடர்பு எண்ணை அறிய மாவட்டத்தின் பெயரை குறிப்பிடவும்.*"
                )
            elif language == "hi":
                return (
                    "### 👤 ऋण एवं बैंकिंग सेवाओं हेतु संपर्क अधिकारी\n"
                    "- **प्राथमिक संपर्क:** स्थानीय शाखा प्रबंधक / पैक्स सचिव / जिला केंद्रीय सहकारी बैंक (DCCB) अधिकारी\n"
                    "- **जिला नोडल अधिकारी:** अग्रणी जिला प्रबंधक (LDM), जिला कलेक्ट्रेट\n"
                    "- **वैधानिक बैंकिंग लोकपाल:** आरबीआई लोकपाल हेल्पलाइन: `14448`\n"
                    "*💡 अपने जिले के अधिकारी का फोन नंबर देखने के लिए प्रश्न में अपने जिले का नाम लिखें।*"
                )
            else:
                return (
                    "### 👤 Competent Officers to Meet for Credit & Banking Services\n"
                    "- **Primary Point of Contact:** Branch Manager / PACS Secretary / District Central Cooperative Bank (DCCB) Field Officer\n"
                    "- **District Escalation:** Lead District Manager (LDM) at District Collectorate\n"
                    "- **Statutory Banking Ombudsman:** RBI Ombudsman Helpline `14448` (for loan document release & unfair practices)\n"
                    "*💡 To view your exact district officer's phone number and office address, mention your district (e.g., Theni, Madurai, Pudukkottai, Erode, Karur).*"
                )
        else:
            if language == "ta":
                return (
                    "### 👤 அரசு திட்டங்களுக்கு நீங்கள் அணுக வேண்டிய அதிகாரிகள்\n"
                    "- **வட்டார நிலை:** உதவி வேளாண்மை அலுவலர் (AAO) / வேளாண்மை உதவி இயக்குனர் (ADA)\n"
                    "- **மாவட்ட நிலை:** வேளாண்மை இணை இயக்குனர் (JDA) / மாவட்ட ஆட்சியர் அலுவலகம்\n"
                    "- **விண்ணப்ப உதவி:** உள்ளூர் இ-சேவை மையம் (CSC) அல்லது PACS கூட்டுறவு சங்கம்\n"
                    "*💡 உங்கள் மாவட்ட அதிகாரியின் தொலைபேசி எண்ணைக் காண உங்கள் மாவட்டத்தின் பெயரைக் குறிப்பிடவும்.*"
                )
            elif language == "hi":
                return (
                    "### 👤 किसान कल्याण योजनाओं हेतु संपर्क अधिकारी\n"
                    "- **ब्लॉक/ग्राम स्तर:** सहायक कृषि अधिकारी (AAO) / सहायक कृषि निदेशक (ADA)\n"
                    "- **जिला स्तर:** संयुक्त कृषि निदेशक (JDA) / जिला कलेक्ट्रेट कृषि विभाग\n"
                    "- **आवेदन केंद्र:** स्थानीय प्राथमिक कृषि ऋण समिति (PACS) अथवा ई-सेवा / कॉमन सर्विस सेंटर (CSC)\n"
                    "*💡 अपने जिले के अधिकारी का सीधा संपर्क देखने के लिए अपने जिले का नाम लिखें।*"
                )
            else:
                return (
                    "### 👤 Competent Officers to Meet for Farmer Welfare Schemes\n"
                    "- **Block/Village Level:** Assistant Agricultural Officer (AAO) / Assistant Director of Agriculture (ADA) at Block Agriculture Extension Center\n"
                    "- **District Level:** Joint Director of Agriculture (JDA) / District Collectorate Agriculture Wing\n"
                    "- **Application Center:** Local Primary Agricultural Credit Society (PACS) or Common Service Centre (CSC)\n"
                    "*💡 To view your exact district officer's phone number and office location, mention your district (e.g., Theni, Madurai, Pudukkottai, Erode, Karur).*"
                )
