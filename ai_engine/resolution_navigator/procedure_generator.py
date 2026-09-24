"""
Resolution Navigator: Step-by-Step Procedure Generator with document checklists.
"""
from typing import Dict, Any, List
from ai_engine.resolution_navigator.grievance_classifier import GrievanceClassifier
from ai_engine.resolution_navigator.office_officer_recommender import OfficeOfficerRecommender

class ProcedureGenerator:
    def __init__(self):
        self.classifier = GrievanceClassifier()
        self.recommender = OfficeOfficerRecommender()

    def generate_for_query(self, query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        classification = self.classifier.classify_grievance(query)
        category = classification["category"]
        officers = self.recommender.recommend(category)

        steps = [
            {
                "step_no": 1,
                "title": "Document Compilation",
                "instruction": "Assemble Aadhaar card, Society passbook, land records (7/12 / Khatauni) and receipt/docket numbers.",
                "timeline": "Day 1"
            },
            {
                "step_no": 2,
                "title": f"Initial Representation to {officers[0]['officer_designation']}",
                "instruction": f"Submit written grievance with dated acknowledgment slip at {officers[0]['office_title']}.",
                "timeline": f"Within {officers[0]['sla']}"
            },
            {
                "step_no": 3,
                "title": f"Escalation to {officers[1]['officer_designation']}",
                "instruction": f"If no resolution received in initial window, trigger statutory escalation to {officers[1]['office_title']}.",
                "timeline": f"SLA: {officers[1]['sla']}"
            }
        ]

        return {
            "grievance_category": category,
            "severity": classification["severity"],
            "recommended_officers": officers,
            "procedural_steps": steps,
            "statutory_sla_days": classification["escalation_sla_days"]
        }
