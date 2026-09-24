"""
Resolution Navigator: Office & Officer Recommender with jurisdiction matching.
"""
from typing import List, Dict, Any

class OfficeOfficerRecommender:
    def recommend(self, category: str, district: str = "Default District") -> List[Dict[str, Any]]:
        if "Insurance" in category or "PMFBY" in category:
            return [
                {
                    "tier": "Level 1: Local / Block",
                    "office_title": "District Agriculture Office & Insurance Helpdesk",
                    "officer_designation": "District Agriculture Officer (DAO)",
                    "action_required": "Submit 72-hr Intimation Docket & Surveyor Joint Survey Report",
                    "sla": "7 Days"
                },
                {
                    "tier": "Level 2: District Apex",
                    "office_title": "District Magistrate / Collector Office",
                    "officer_designation": "Head, District Grievance Redressal Committee (DGRC)",
                    "action_required": "File formal arbitration petition against insurance company rejection",
                    "sla": "15 Days"
                }
            ]
        elif "Membership" in category:
            return [
                {
                    "tier": "Level 1: Primary Society",
                    "office_title": "Local Primary Agricultural Credit Society (PACS)",
                    "officer_designation": "Secretary / Managing Committee",
                    "action_required": "Obtain written acknowledgment of share capital submission",
                    "sla": "30 Days"
                },
                {
                    "tier": "Level 2: Sub-Division",
                    "office_title": "Office of Assistant Registrar of Cooperative Societies",
                    "officer_designation": "Assistant Registrar (ARCS)",
                    "action_required": "Appeal under Section 19 of Cooperative Societies Act for Deemed Membership",
                    "sla": "21 Days"
                }
            ]
        else:
            return [
                {
                    "tier": "Level 1: Branch",
                    "office_title": "District Central Cooperative Bank (DCCB)",
                    "officer_designation": "DCCB Branch Manager / PACS Chief Executive",
                    "action_required": "Demand KCC ledger verification and sanction status letter",
                    "sla": "15 Days"
                },
                {
                    "tier": "Level 2: District Registrar",
                    "office_title": "Office of Deputy Registrar of Cooperative Societies",
                    "officer_designation": "DRCS / Cooperative Ombudsman",
                    "action_required": "Formal petition for administrative inquiry",
                    "sla": "30 Days"
                }
            ]
