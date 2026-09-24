"""
Notification Service & Smart Scheme Alert Matcher for rural cooperative members.
"""
from typing import List, Dict, Any
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.notifications: List[Dict[str, Any]] = [
            {
                "id": "NOTIF-01",
                "title": "PMFBY 72-Hour Claim Window Alert",
                "category": "Crop Insurance",
                "message": "Heavy unseasonal rain reported in district. Affected farmers must register claim within 72 hours via Crop Insurance App or PACS.",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "priority": "High",
                "badge": "Urgent"
            },
            {
                "id": "NOTIF-02",
                "title": "PACS Computerization & ERP Enrollment",
                "category": "PACS Modernization",
                "message": "All PACS members are requested to link Aadhaar with society passbooks for DBT crop loan interest subvention.",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "priority": "Medium",
                "badge": "Advisory"
            },
            {
                "id": "NOTIF-03",
                "title": "PM-KISAN 17th Installment Release",
                "category": "Direct Benefit Transfer",
                "message": "Verify your e-KYC status at pmkisan.gov.in or nearest CSC to prevent installment holding.",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "priority": "Normal",
                "badge": "Update"
            }
        ]

    def get_active_notifications(self) -> List[Dict[str, Any]]:
        return self.notifications

    def match_user_schemes(self, land_size_acres: float, has_kcc: bool) -> List[Dict[str, Any]]:
        matched = []
        if land_size_acres > 0:
            matched.append({
                "scheme": "PM-KISAN",
                "status": "Eligible",
                "estimated_benefit": "₹6,000 / year"
            })
            matched.append({
                "scheme": "PMFBY Crop Insurance",
                "status": "Recommended for Kharif/Rabi",
                "premium_subsidy": "Up to 90% premium paid by Central & State Govt"
            })
        if not has_kcc:
            matched.append({
                "scheme": "KCC Loan Subvention Scheme",
                "status": "Action Required: Apply at local PACS",
                "effective_interest": "4.0% with prompt repayment"
            })
        return matched
