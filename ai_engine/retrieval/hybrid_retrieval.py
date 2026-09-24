"""
Hybrid Retrieval engine: real ChromaDB semantic search + domain metadata filtering,
plus officer/authority contact resolution per retrieved scheme.
"""
import os
import json
from typing import List, Dict, Any, Optional
from config.settings import settings
from ai_engine.retrieval.vector_search import VectorSearchEngine
from ai_engine.retrieval.authority_lookup import AuthorityLookup


class HybridRetriever:
    def __init__(self):
        self.vector_engine = VectorSearchEngine()
        self.authority_lookup = AuthorityLookup()
        self.authorities: List[Dict[str, Any]] = []
        self._load_authorities()

    def _load_authorities(self):
        auth_path = settings.AUTHORITIES_PATH
        if os.path.exists(auth_path):
            try:
                with open(auth_path, "r", encoding="utf-8") as f:
                    self.authorities = json.load(f)
            except Exception as e:
                print(f"Error loading authorities: {e}")

    def retrieve(self, query: str, domain_filter: Optional[str] = None, top_k: int = 3) -> Dict[str, Any]:
        # NOTE: domain_filter is intentionally NOT passed to vector_engine.search()
        # below. At this corpus size, a misclassified domain can wrongly exclude
        # the correct document (e.g. "KCC" queries classify as financial_literacy,
        # but KCC's data lives under farmer_scheme) — semantic search alone across
        # the whole corpus is more reliable than trusting domain classification
        # to gate the candidate pool. domain_filter is still accepted here for
        # compatibility with callers, just unused for filtering.
        results = self.vector_engine.search(query=query, domain_filter=None, top_k=top_k)

        citations = []
        for doc in results:
            citations.extend(doc.get("citations", []))

        # Only resolve an officer contact for the single best-matching document
        # (rank 1) — not every document in the top_k, which pulls in unrelated
        # officer types from loosely-related secondary matches.
        resolved_authorities = []
        if results:
            top_designation = results[0].get("designation")
            if top_designation:
                officer_result = self.authority_lookup.lookup(top_designation, query)
                if officer_result:
                    resolved_authorities.append(officer_result)

        return {
            "documents": results,
            "citations": list(set(citations)),
            "authorities": resolved_authorities,
        }
