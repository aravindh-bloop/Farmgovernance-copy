@echo off
TITLE Multilingual Cooperative AI Portal - Launcher
echo =====================================================================
echo  Multilingual Cooperative Governance & Legal Assistance Portal
echo  Team BRAVITS - SIH26088
echo =====================================================================
echo.

echo [1/3] Starting FastAPI Backend on http://localhost:8000 ...
start "Backend API (Port 8000)" cmd /k "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [2/3] Starting Hardware Kiosk Frontend on http://localhost:5173 ...
start "Kiosk Frontend (Port 5173)" cmd /k "cd frontend && npm run dev -- --host 0.0.0.0 --port 5173"

timeout /t 2 /nobreak >nul

echo [3/3] Starting Web Portal Frontend on http://localhost:5174 ...
start "Web Portal (Port 5174)" cmd /k "cd frontend-web && npm run dev -- --host 0.0.0.0 --port 5174"

echo.
echo =====================================================================
echo  All services have been successfully launched!
echo  - API Docs:      http://localhost:8000/docs
echo  - Kiosk UI:      http://localhost:5173
echo  - Web Portal:    http://localhost:5174
echo =====================================================================
pause
