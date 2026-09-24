"""
PACS, Cooperative Law, and Financial Literacy API Endpoints.
"""
import os
import json
from fastapi import APIRouter
from config.settings import settings

pacs_router = APIRouter()
law_router = APIRouter()
financial_router = APIRouter()

@pacs_router.get("/")
async def get_pacs_data():
    p = os.path.join(settings.DATABASE_PATH, "pacs", "pacs_bylaws.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return {"status": "success", "data": json.load(f)}
    return {"status": "error", "message": "PACS data not found"}

@law_router.get("/")
async def get_laws_data():
    p = os.path.join(settings.DATABASE_PATH, "laws", "cooperative_laws.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return {"status": "success", "data": json.load(f)}
    return {"status": "error", "message": "Cooperative laws not found"}

@financial_router.get("/")
async def get_financial_data():
    p = os.path.join(settings.DATABASE_PATH, "financial", "financial_literacy.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return {"status": "success", "data": json.load(f)}
    return {"status": "error", "message": "Financial literacy data not found"}
