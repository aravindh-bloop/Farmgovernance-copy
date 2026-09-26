"""
End-to-End Multilingual RAG Pipeline coordinating Domain Routing, Multi-Domain Sub-Model Execution,
Post-LLM Database Cross-Verification for every sub-model, and Unified Fusion Synthesis.
"""
from typing import Dict, Any, List
from ai_engine.orchestration.domain_router import DomainRouter
from ai_engine.orchestration.fusion_synthesizer import FusionSynthesizer
from ai_engine.submodels.farmer_scheme_engine import FarmerSchemeEngine
from ai_engine.submodels.grievance_engine import GrievanceEngine
from ai_engine.submodels.pacs_pmfby_engine import PacsPmfbyEngine
from ai_engine.submodels.cooperative_law_engine import CooperativeLawEngine
from ai_engine.submodels.financial_literacy_engine import FinancialLiteracyEngine
from ai_engine.rag.prompt_builder import PromptBuilder
from ai_engine.llm.reasoner import LLMReasoner
from ai_engine.resolution_navigator.procedure_generator import ProcedureGenerator
from ai_engine.language.language_detector import LanguageDetector
from ai_engine.language.translation import TranslationEngine

class RAGPipeline:
    def __init__(self):
        self.router = DomainRouter()
        self.reasoner = LLMReasoner()
        self.farmer_scheme_submodel = FarmerSchemeEngine()
        self.grievance_submodel = GrievanceEngine()
        self.pacs_pmfby_submodel = PacsPmfbyEngine()
        self.cooperative_law_submodel = CooperativeLawEngine()
        self.financial_literacy_submodel = FinancialLiteracyEngine()
        self.fusion_synthesizer = FusionSynthesizer()
        self.procedure_gen = ProcedureGenerator()
        self.lang_detector = LanguageDetector()
        self.translator = TranslationEngine()

    def _answer_general(self, query: str, language: str) -> str:
        """Greeting / small-talk answered by the LLM directly in the user's language."""
        prompt = PromptBuilder.build_greeting_prompt(query, language)
        ans = self.reasoner.generate_response(prompt, [], "general", language)
        if (not ans or ans.strip().startswith("I could not find") or ans.strip().startswith("No matching official")):
            ans = self.reasoner.greeting_answer()
            if language and language != "en":
                translated = self.translator.translate(ans, "en", language)
                if translated:
                    ans = translated
        return ans.strip()

    def _no_record_message(self, language: str) -> str:
        msg = (
            "I could not find a verified official record matching your question in the database. "
            "Please rephrase your question or contact your local Assistant Registrar of Cooperative "
            "Societies (ARCS) or PACS Secretary with your full details."
        )
        if language and language != "en":
            translated = self.translator.translate(msg, "en", language)
            if translated:
                return translated
        return msg

    def process_query(self, query: str, language: str = "en") -> Dict[str, Any]:
        # Auto-detect language from query text if Indic script characters are present
        if query and query.strip():
            det = self.lang_detector.detect(query)
            if det and det.get("language") and det.get("language") != "en":
                language = det.get("language")

        # 1. Routing & Retrieval across all activated sub-domains
        routing_result = self.router.route_and_retrieve(query=query, language=language)
        primary_domain = routing_result["domain"]
        active_domains = routing_result.get("active_domains", [primary_domain])
        all_docs = routing_result["retrieved_context"]
        citations = routing_result["citations"]
        extracted_slots = routing_result.get("extracted_slots", {})
        authorities = routing_result.get("authorities", [])

        domain_contexts: Dict[str, List[Dict[str, Any]]] = {}
        domain_answers: Dict[str, str] = {}

        # 2. Execute each sub-model with specialized engines or domain RAG.
        #    A sub-model can now return an EMPTY guidance (no verified match) —
        #    the pipeline never fills that gap with top catalog entries.
        for dom in active_domains:
            guidance_text = ""
            primary_doc: Dict[str, Any] = {}
            dom_citations: List[str] = []

            if dom == "farmer_scheme":
                scheme_res = self.farmer_scheme_submodel.generate_scheme_guidance(query, language)
                guidance_text = scheme_res["guidance_text"]
                primary_doc = scheme_res["primary_scheme"]
                dom_citations = scheme_res["citations"]
            elif dom == "grievance":
                grv_res = self.grievance_submodel.generate_grievance_guidance(query, language)
                guidance_text = grv_res["guidance_text"]
                primary_doc = grv_res["primary_grievance"]
                dom_citations = grv_res["primary_grievance"].get("legal_sections", [])
            elif dom == "pacs_pmfby":
                pacs_res = self.pacs_pmfby_submodel.generate_guidance(query, language)
                guidance_text = pacs_res["guidance_text"]
                primary_doc = pacs_res["primary_topic"]
                dom_citations = pacs_res["citations"]
            elif dom == "cooperative_law":
                law_res = self.cooperative_law_submodel.generate_guidance(query, language)
                guidance_text = law_res["guidance_text"]
                primary_doc = law_res["primary_law"]
                dom_citations = law_res["citations"]
            elif dom == "financial_literacy":
                fin_res = self.financial_literacy_submodel.generate_guidance(query, language)
                guidance_text = fin_res["guidance_text"]
                primary_doc = fin_res["primary_topic"]
                dom_citations = fin_res["citations"]

            if guidance_text:
                domain_answers[dom] = guidance_text
                if primary_doc:
                    domain_contexts[dom] = [primary_doc]
                citations.extend(dom_citations)

        # 3. Greetings & general chat — answered directly by the LLM (never by a sub-model default)
        is_greeting = self.reasoner.is_greeting(query)
        if is_greeting:
            if "general" not in active_domains:
                active_domains = active_domains + ["general"]
            domain_answers["general"] = self._answer_general(query, language)
            domain_contexts["general"] = []
        elif "general" in active_domains and "general" not in domain_answers:
            # Unmatched content query — honest pointer, in the user's language.
            domain_answers["general"] = self._no_record_message(language)
            domain_contexts["general"] = []

        # 4. No verified record matched anywhere → graceful, honest response (no canned defaults)
        if not domain_answers:
            fallback_ans = self.reasoner.generate_response(
                PromptBuilder.build_rag_prompt(query, all_docs[:3], language),
                all_docs[:3], primary_domain, language
            )
            if not fallback_ans or fallback_ans.startswith("I could not find") or fallback_ans.startswith("No matching official"):
                fallback_ans = self._no_record_message(language)
            domain_answers[primary_domain] = fallback_ans
            domain_contexts[primary_domain] = all_docs[:2]

        # 5. Post-LLM Multi-Domain Database Cross-Verification & Fusion
        fused_result = self.fusion_synthesizer.synthesize(
            query=query,
            active_domains=active_domains,
            domain_contexts=domain_contexts,
            domain_answers=domain_answers,
            citations=citations,
            extracted_slots=extracted_slots,
            language=language
        )

        # 6. Procedure / Resolution recommendation if Grievance or Calamity
        procedure = None
        if "grievance" in active_domains or primary_domain == "grievance" or any(w in query.lower() for w in ["delay", "reject", "refuse", "bribe", "complaint"]):
            procedure = self.procedure_gen.generate_for_query(query, all_docs)

        return {
            "query": query,
            "language": language,
            "domain": primary_domain,
            "active_domains": active_domains,
            "is_multi_domain": fused_result["is_multi_domain"],
            "confidence": routing_result["intent"]["confidence"],
            "answer": fused_result["fused_answer"],
            "recommended_officer": fused_result.get("recommended_officer"),
            "citations": fused_result["citations"],
            "verification_status": fused_result["verification_status"],
            "trust_score": fused_result["trust_score"],
            "verified_facts": fused_result["verified_facts"],
            "corrections_applied": fused_result.get("corrections_applied", []),
            "source_authority": fused_result["source_authority"],
            "procedure": procedure,
            "extracted_slots": extracted_slots,
            "authorities": authorities
        }
