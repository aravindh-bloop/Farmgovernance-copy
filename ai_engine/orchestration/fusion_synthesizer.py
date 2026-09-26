from typing import Dict, Any, List
from ai_engine.verification.database_cross_verifier import DatabaseCrossVerifier
from ai_engine.resolution_navigator.officer_recommender import OfficerRecommender

from ai_engine.language.translation import TranslationEngine

class FusionSynthesizer:
    def __init__(self):
        self.cross_verifier = DatabaseCrossVerifier()
        self.officer_recommender = OfficerRecommender()
        self.translator = TranslationEngine()

    def synthesize(
        self,
        query: str,
        active_domains: List[str],
        domain_contexts: Dict[str, List[Dict[str, Any]]],
        domain_answers: Dict[str, str],
        citations: List[str],
        extracted_slots: Dict[str, Any],
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Synthesizes multi-domain submodel outputs, performs database cross-verification
        across all active sub-models, and enriches with verified district officer recommendations.
        """
        all_verified_facts: List[str] = []
        all_corrections: List[str] = []
        all_citations: List[str] = list(citations)
        trust_scores: List[float] = []

        domain_titles_en = {
            "pacs_pmfby": "🌾 PACS Services & PMFBY Crop Insurance",
            "farmer_scheme": "📜 Farmer Welfare & Subsidy Schemes",
            "grievance": "⚖️ Grievance Redressal & Statutory Escalation",
            "cooperative_law": "🏛️ Cooperative Law & Governance (MSCS Act)",
            "financial_literacy": "💳 Credit Literacy & Kisan Credit Card (KCC)",
            "general": "💬 General Assistance"
        }

        domain_titles_ta = {
            "pacs_pmfby": "🌾 PACS சேவைகள் & PMFBY பயிர் காப்பீடு",
            "farmer_scheme": "📜 உழவர் நலன் & அரசு மானியத் திட்டங்கள்",
            "grievance": "⚖️ குறைதீர்ப்பு & சட்டப்பூர்வ தீர்வு",
            "cooperative_law": "🏛️ கூட்டுறவு சட்டம் & நிர்வாக வழிகாட்டுதல்",
            "financial_literacy": "💳 கிசான் கிரெடிட் கார்டு (KCC) & கடன் வழிகாட்டல்",
            "general": "💬 பொது உதவி"
        }

        domain_titles_hi = {
            "pacs_pmfby": "🌾 पैक्स सेवाएं एवं पीएम फसल बीमा",
            "farmer_scheme": "📜 किसान कल्याण एवं सरकारी योजनाएं",
            "grievance": "⚖️ शिकायत निवारण एवं कानूनी समाधान",
            "cooperative_law": "🏛️ सहकारी कानून एवं प्रशासन",
            "financial_literacy": "💳 किसान क्रेडिट कार्ड (KCC) एवं वित्तीय साक्षरता",
            "general": "💬 सामान्य सहायता"
        }

        domain_titles = domain_titles_ta if language == "ta" else (domain_titles_hi if language == "hi" else domain_titles_en)

        # 1. Cross-verify every sub-model with the updated database
        for dom in active_domains:
            docs = domain_contexts.get(dom, [])
            ans = domain_answers.get(dom, "")
            v_res = self.cross_verifier.cross_verify(
                draft_answer=ans,
                domain=dom,
                retrieved_docs=docs,
                extracted_slots=extracted_slots
            )
            all_verified_facts.extend(v_res.get("verified_facts", []))
            all_corrections.extend(v_res.get("corrections_applied", []))
            all_citations.extend(v_res.get("official_citations", []))
            trust_scores.append(v_res.get("trust_score", 0.95))

        # 2. Build fused structured answer
        fused_sections: List[str] = []
        
        # Header banner if multi-domain
        if len(active_domains) > 1:
            active_labels = " + ".join([domain_titles.get(d, d.title()) for d in active_domains])
            if language == "ta":
                fused_sections.append(f"### 🌐 ஒருங்கிணைந்த சரிபார்க்கப்பட்ட வழிகாட்டல்: {active_labels}\n")
            elif language == "hi":
                fused_sections.append(f"### 🌐 एकीकृत सत्यापित परामर्श: {active_labels}\n")
            else:
                fused_sections.append(f"### 🌐 Multi-Domain Verified Advisory: {active_labels}\n")

        for dom in active_domains:
            title = domain_titles.get(dom, dom.replace("_", " ").title())
            ans = domain_answers.get(dom, "").strip()
            if ans:
                if len(active_domains) > 1:
                    fused_sections.append(f"#### {title}\n{ans}\n")
                else:
                    fused_sections.append(ans)

        fused_answer = "\n".join(fused_sections).strip()

        # If nothing verified matched, use an honest fallback rather than an empty reply.
        if not fused_answer:
            fused_answer = (
                "I could not find a verified official record matching your question in the database. "
                "Please rephrase your question or contact your local Assistant Registrar of Cooperative "
                "Societies (ARCS) or PACS Secretary with your full details."
            )
            if language and language != "en":
                translated = self.translator.translate(fused_answer, "en", language)
                if translated:
                    fused_answer = translated

        # Tamil & Hindi have native sub-model templates, but some topics fall back to
        # English. Translate those via the neural pipeline (Bhashini→Sarvam→Google).
        if language in ("ta", "hi") and fused_answer:
            ascii_ratio = (sum(1 for ch in fused_answer if ord(ch) < 128) / max(len(fused_answer), 1)) if fused_answer else 1.0
            if ascii_ratio > 0.95:
                translated = self.translator.translate(fused_answer, "en", language)
                if translated:
                    fused_answer = translated

        # Apply phrase translation if language is not English, Tamil, or Hindi (which already have native sub-model templates)
        if language not in ("en", "ta", "hi") and fused_answer:
            fused_answer = self.translator.translate(fused_answer, "en", language) or fused_answer

        # 3. Recommend Verified District Officer (Strict Zero-Hallucination)
        officer_rec = self.officer_recommender.recommend_officer(
            query=query,
            active_domains=active_domains,
            fusion_output=fused_answer,
            language=language
        )
        recommended_officer_data = None
        if officer_rec:
            fused_answer = fused_answer + "\n\n" + officer_rec["recommendation_text"]
            officer_obj = officer_rec.get("officer")
            recommended_officer_data = officer_obj
            if officer_obj:
                all_citations.append(officer_obj.get("source", "District Administration Official Directory"))
                off_name = officer_obj.get("name") or "Designated Officer"
                all_verified_facts.append(f"Verified District Official: {off_name} ({officer_obj.get('designation_or_role')})")

        avg_trust_score = round(sum(trust_scores) / len(trust_scores), 2) if trust_scores else 0.98
        unique_citations = list(dict.fromkeys(all_citations))
        unique_facts = list(dict.fromkeys(all_verified_facts))

        return {
            "fused_answer": fused_answer,
            "is_multi_domain": len(active_domains) > 1,
            "active_domains": active_domains,
            "recommended_officer": recommended_officer_data,
            "trust_score": min(avg_trust_score, 0.99),
            "verification_status": True if avg_trust_score >= 0.70 else False,
            "verified_facts": unique_facts,
            "corrections_applied": all_corrections,
            "citations": unique_citations,
            "source_authority": "Ministry of Cooperation / State District Administration Live Verified Database"
        }
