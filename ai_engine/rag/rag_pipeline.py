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

        # 2. Execute each sub-model with specialized engines or domain RAG
        for dom in active_domains:
            if dom == "farmer_scheme":
                # Specialized Farmer Scheme Sub-Model Execution
                scheme_res = self.farmer_scheme_submodel.generate_scheme_guidance(query, language)
                domain_answers[dom] = scheme_res["guidance_text"]
                domain_contexts[dom] = [scheme_res["primary_scheme"]]
                citations.extend(scheme_res["citations"])
            elif dom == "grievance":
                # Specialized Grievance Redressal Sub-Model Execution
                grv_res = self.grievance_submodel.generate_grievance_guidance(query, language)
                domain_answers[dom] = grv_res["guidance_text"]
                domain_contexts[dom] = [grv_res["primary_grievance"]]
                citations.extend(grv_res["primary_grievance"].get("legal_sections", []))
            elif dom == "pacs_pmfby":
                # Specialized PACS + PMFBY Sub-Model Execution
                pacs_res = self.pacs_pmfby_submodel.generate_guidance(query, language)
                domain_answers[dom] = pacs_res["guidance_text"]
                domain_contexts[dom] = [pacs_res["primary_topic"]]
                citations.extend(pacs_res["citations"])
            elif dom == "cooperative_law":
                # Specialized Cooperative Law Sub-Model Execution
                law_res = self.cooperative_law_submodel.generate_guidance(query, language)
                domain_answers[dom] = law_res["guidance_text"]
                domain_contexts[dom] = [law_res["primary_law"]]
                citations.extend(law_res["citations"])
            elif dom == "financial_literacy":
                # Specialized Financial Literacy Sub-Model Execution
                fin_res = self.financial_literacy_submodel.generate_guidance(query, language)
                domain_answers[dom] = fin_res["guidance_text"]
                domain_contexts[dom] = [fin_res["primary_topic"]]
                citations.extend(fin_res["citations"])
            else:
                # General / Domain RAG Reasoner
                dom_docs = [d for d in all_docs if d.get("domain") == dom or d.get("domain") in dom]
                if not dom_docs:
                    dom_docs = all_docs[:2]
                domain_contexts[dom] = dom_docs

                prompt = PromptBuilder.build_rag_prompt(query, dom_docs, language)
                ans = self.reasoner.generate_response(prompt, dom_docs, dom, language)
                domain_answers[dom] = ans

        # 3. Post-LLM Multi-Domain Database Cross-Verification & Fusion
        fused_result = self.fusion_synthesizer.synthesize(
            query=query,
            active_domains=active_domains,
            domain_contexts=domain_contexts,
            domain_answers=domain_answers,
            citations=citations,
            extracted_slots=extracted_slots,
            language=language
        )

        # 4. Procedure / Resolution recommendation if Grievance or Calamity
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
