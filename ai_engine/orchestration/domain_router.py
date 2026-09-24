"""
Domain Router for dispatching queries to specialized RAG handlers and knowledge retrievers.
Supports multi-domain concurrent activation across farmer_scheme, grievance, pacs_pmfby,
cooperative_law, and financial_literacy.
"""
from typing import Dict, Any, List
from ai_engine.orchestration.intent_classifier import IntentClassifier
from ai_engine.retrieval.hybrid_retrieval import HybridRetriever

class DomainRouter:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.retriever = HybridRetriever()

    def route_and_retrieve(self, query: str, language: str = "en") -> Dict[str, Any]:
        classification = self.classifier.classify(query)
        primary_domain = classification["primary_domain"]
        active_domains = classification.get("active_domains", [primary_domain])

        aggregated_docs: List[Dict[str, Any]] = []
        aggregated_citations: List[str] = []
        authorities: List[Dict[str, Any]] = []

        # Retrieve context across all activated domains
        for dom in active_domains:
            res = self.retriever.retrieve(query=query, domain_filter=dom, top_k=3)
            for doc in res.get("documents", []):
                if doc not in aggregated_docs:
                    aggregated_docs.append(doc)
            aggregated_citations.extend(res.get("citations", []))
            if res.get("authorities"):
                for auth in res["authorities"]:
                    if auth not in authorities:
                        authorities.append(auth)

        # Fallback if specific domain search yielded nothing
        if not aggregated_docs:
            general_res = self.retriever.retrieve(query=query, domain_filter=None, top_k=3)
            aggregated_docs = general_res.get("documents", [])
            aggregated_citations.extend(general_res.get("citations", []))

        return {
            "intent": classification,
            "domain": primary_domain,
            "active_domains": active_domains,
            "is_multi_domain": len(active_domains) > 1,
            "language": language,
            "retrieved_context": aggregated_docs,
            "citations": list(dict.fromkeys(aggregated_citations)),
            "authorities": authorities,
            "extracted_slots": classification.get("extracted_slots", {})
        }
