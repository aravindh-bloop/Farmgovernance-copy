"""
Grievance Registration & Resolution Navigator API.
"""
from fastapi import APIRouter
from backend.app.schemas.chat import GrievanceSubmission
from backend.app.services.grievance_service import grievance_service
import os
import json
from config.settings import settings

router = APIRouter()

@router.post("/register")
async def register_grievance(payload: GrievanceSubmission):
    result = grievance_service.file_grievance(payload.dict())
    return result

@router.get("/tickets")
async def get_tickets():
    return {"status": "success", "tickets": grievance_service.get_all_tickets()}

@router.get("/authorities")
async def get_authorities_directory():
    auth_path = settings.AUTHORITIES_PATH
    if os.path.exists(auth_path):
        with open(auth_path, "r", encoding="utf-8") as f:
            return {"status": "success", "authorities": json.load(f)}
    return {"status": "success", "authorities": []}
