"""
Financial Literacy & KCC API Routes.
"""
import os
import json
from fastapi import APIRouter
from config.settings import settings

router = APIRouter()

@router.get("/")
async def get_financial_data():
    p = os.path.join(settings.DATABASE_PATH, "financial", "financial_literacy.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return {"status": "success", "data": json.load(f)}
    return {"status": "error", "message": "Financial literacy data not found"}
