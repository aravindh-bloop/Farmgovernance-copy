"""
Cooperative Law API Routes.
"""
import os
import json
from fastapi import APIRouter
from config.settings import settings

router = APIRouter()

@router.get("/")
async def get_laws_data():
    p = os.path.join(settings.DATABASE_PATH, "laws", "cooperative_laws.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return {"status": "success", "data": json.load(f)}
    return {"status": "error", "message": "Cooperative laws not found"}
