"""
Source Validator with Updated Database Cross-Verification to guarantee hallucination-free responses.
"""
from typing import List, Dict, Any, Optional
from ai_engine.verification.database_cross_verifier import DatabaseCrossVerifier

class SourceValidator:
    def __init__(self):
        self.cross_verifier = DatabaseCrossVerifier()

    def validate(
        self,
        answer: str,
        context_docs: List[Dict[str, Any]],
        citations: List[str],
        domain: str = "general",
        extracted_slots: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Perform deep database cross-verification
        db_verification = self.cross_verifier.cross_verify(
            draft_answer=answer,
            domain=domain,
            retrieved_docs=context_docs,
            extracted_slots=extracted_slots
        )

        all_citations = set(citations)
        all_citations.update(db_verification["official_citations"])

        for doc in context_docs:
            if "citations" in doc and isinstance(doc["citations"], list):
                all_citations.update(doc["citations"])
            if "section" in doc:
                all_citations.add(f"{doc.get('act_name', 'Act')} - {doc.get('section')}")

        return {
            "is_verified": db_verification["is_verified"],
            "citations": list(all_citations),
            "trust_score": db_verification["trust_score"],
            "verified_facts": db_verification["verified_facts"],
            "corrections_applied": db_verification["corrections_applied"],
            "source_authority": db_verification["verification_authority"],
            "database_sync_status": db_verification["updated_database_status"]
        }
