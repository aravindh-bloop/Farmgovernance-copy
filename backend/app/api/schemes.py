"""
Schemes & PMFBY API Endpoints.
"""
import os
import json
from fastapi import APIRouter
from config.settings import settings

router = APIRouter()

@router.get("/")
async def list_all_schemes():
    schemes_path = os.path.join(settings.DATABASE_PATH, "schemes", "farmer_schemes.json")
    pmfby_path = os.path.join(settings.DATABASE_PATH, "pmfby", "pmfby_guidelines.json")
    
    data = []
    if os.path.exists(schemes_path):
        with open(schemes_path, "r", encoding="utf-8") as f:
            data.extend(json.load(f))
    if os.path.exists(pmfby_path):
        with open(pmfby_path, "r", encoding="utf-8") as f:
            data.extend(json.load(f))
            
    return {"status": "success", "count": len(data), "data": data}

@router.get("/pmfby")
async def get_pmfby_guidelines():
    pmfby_path = os.path.join(settings.DATABASE_PATH, "pmfby", "pmfby_guidelines.json")
    if os.path.exists(pmfby_path):
        with open(pmfby_path, "r", encoding="utf-8") as f:
            return {"status": "success", "data": json.load(f)}
    return {"status": "error", "message": "PMFBY guidelines not found"}
