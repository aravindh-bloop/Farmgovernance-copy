"""
Metadata filtering for cooperative domain knowledge queries.
"""
from typing import List, Dict, Any

class MetadataFilter:
    @staticmethod
    def filter_by_domain(documents: List[Dict[str, Any]], domain: str) -> List[Dict[str, Any]]:
        if not domain or domain == "general_coop":
            return documents
        filtered = [doc for doc in documents if doc.get("domain") == domain]
        return filtered if filtered else documents

    @staticmethod
    def filter_by_state(documents: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
        if not state:
            return documents
        return [doc for doc in documents if state.lower() in str(doc.get("applicable_to", "")).lower() or not doc.get("applicable_to")]
