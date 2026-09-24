"""
Grievance Service handling Resolution Navigator tickets, escalation tracking, and officer routing.
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List
from ai_engine.resolution_navigator.procedure_generator import ProcedureGenerator
from ai_engine.resolution_navigator.escalation_engine import EscalationEngine

class GrievanceService:
    def __init__(self):
        self.procedure_gen = ProcedureGenerator()
        self.tickets: List[Dict[str, Any]] = []

    def file_grievance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        ticket_id = f"COOP-GRV-{uuid.uuid4().hex[:6].upper()}"
        procedure = self.procedure_gen.generate_for_query(
            query=f"{data.get('category')} {data.get('complaint_details')}",
            context_docs=[]
        )

        ticket = {
            "ticket_id": ticket_id,
            "created_at": datetime.now().isoformat(),
            "status": "Registered & Assigned",
            "applicant_name": data.get("applicant_name"),
            "district": data.get("district"),
            "category": data.get("category"),
            "complaint_details": data.get("complaint_details"),
            "assigned_officer": procedure["recommended_officers"][0],
            "escalation_officer": procedure["recommended_officers"][1] if len(procedure["recommended_officers"]) > 1 else None,
            "sla_days": procedure["statutory_sla_days"],
            "days_elapsed": 0,
            "escalation_status": EscalationEngine.calculate_escalation_status(0, procedure["statutory_sla_days"])
        }

        self.tickets.append(ticket)
        return {
            "status": "success",
            "message": "Grievance registered and dispatched to designated jurisdictional authority.",
            "ticket": ticket,
            "procedure_steps": procedure["procedural_steps"]
        }

    def get_all_tickets(self) -> List[Dict[str, Any]]:
        return self.tickets

grievance_service = GrievanceService()
