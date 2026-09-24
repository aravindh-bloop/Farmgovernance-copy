"""
Main FastAPI Application Entrypoint.
Team BRAVITS - Smart India Hackathon (SIH 2026)
Multilingual Cooperative Governance & Legal Assistance Portal (SIH26088)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings

from backend.app.api.chat import router as chat_router
from backend.app.api.schemes import router as schemes_router
from backend.app.api.grievance import router as grievance_router
from backend.app.api.pacs import pacs_router
from backend.app.api.law import router as law_router
from backend.app.api.financial import router as financial_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multilingual AI Assistant for Cooperative Societies, PACS, Farmers, PMFBY, and Grievance Resolution"
)

# Enable CORS for frontend and kiosk clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(chat_router, prefix=f"{settings.API_V1_STR}/chat", tags=["AI Chat & Legal RAG"])
app.include_router(schemes_router, prefix=f"{settings.API_V1_STR}/schemes", tags=["Schemes & PMFBY"])
app.include_router(grievance_router, prefix=f"{settings.API_V1_STR}/grievance", tags=["Resolution Navigator"])
app.include_router(pacs_router, prefix=f"{settings.API_V1_STR}/pacs", tags=["PACS Services & Bylaws"])
app.include_router(law_router, prefix=f"{settings.API_V1_STR}/law", tags=["Cooperative Laws & MSCS"])
app.include_router(financial_router, prefix=f"{settings.API_V1_STR}/financial", tags=["Financial Literacy & KCC"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "offline_edge_mode": settings.OFFLINE_MODE,
        "version": settings.APP_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
