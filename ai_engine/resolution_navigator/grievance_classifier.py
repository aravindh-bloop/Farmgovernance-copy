"""
Resolution Navigator: Grievance Classifier & Severity Estimator.
"""
from typing import Dict, Any

class GrievanceClassifier:
    def classify_grievance(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        if "crop" in text_lower or "pmfby" in text_lower or "insurance" in text_lower or "बीमा" in text_lower:
            return {
                "category": "PMFBY Crop Insurance Claim Dispute",
                "severity": "High",
                "primary_authority": "District Level Grievance Redressal Committee (DGRC)",
                "escalation_sla_days": 15
            }
        elif "membership" in text_lower or "member" in text_lower or "सदस्यता" in text_lower:
            return {
                "category": "Denial or Delay in PACS Membership",
                "severity": "Medium",
                "primary_authority": "Assistant Registrar of Cooperative Societies (ARCS)",
                "escalation_sla_days": 21
            }
        elif "fertilizer" in text_lower or "seed" in text_lower or "खाद" in text_lower or "यूरिया" in text_lower:
            return {
                "category": "PACS Fertilizer/Seed Shortage or Overcharging",
                "severity": "High",
                "primary_authority": "District Agriculture Officer & PACS Secretary",
                "escalation_sla_days": 7
            }
        else:
            return {
                "category": "PACS Loan & Operational Delay",
                "severity": "Medium",
                "primary_authority": "PACS Secretary / DCCB Branch Manager",
                "escalation_sla_days": 15
            }
