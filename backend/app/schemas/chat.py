"""
Pydantic API Schemas for Chat, Intent Classification, and Grievance workflows.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str
    language: Optional[str] = "en"
    domain: Optional[str] = None
    district: Optional[str] = None

class CitationModel(BaseModel):
    citation_text: str
    badge: Optional[str] = "Official"

class ProcedureStep(BaseModel):
    step_no: int
    title: str
    instruction: str
    timeline: str

class ChatResponse(BaseModel):
    query: str
    domain: str
    language: str
    confidence: float
    answer: str
    citations: List[str]
    verification_status: bool
    active_domains: Optional[List[str]] = None
    is_multi_domain: Optional[bool] = False
    trust_score: Optional[float] = 0.95
    verified_facts: Optional[List[str]] = None
    corrections_applied: Optional[List[str]] = None
    source_authority: Optional[str] = None
    extracted_slots: Optional[Dict[str, Any]] = None
    transcription: Optional[str] = None
    officer_recommendation: Optional[Dict[str, Any]] = None
    recommended_officer: Optional[Dict[str, Any]] = None
    procedure: Optional[Dict[str, Any]] = None
    authorities: Optional[List[Dict[str, Any]]] = None

class GrievanceSubmission(BaseModel):
    applicant_name: str
    mobile: str
    aadhaar_last4: Optional[str] = None
    district: str
    society_name: Optional[str] = None
    category: str
    complaint_details: str
    language: Optional[str] = "en"
