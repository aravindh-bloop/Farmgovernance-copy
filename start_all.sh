#!/usr/bin/env bash
# Multilingual Cooperative AI Portal - Launcher for Linux / macOS
set -e

echo "====================================================================="
echo " Multilingual Cooperative Governance & Legal Assistance Portal"
echo " Team BRAVITS - SIH26088"
echo "====================================================================="

# 1. Start Backend in background
echo "[1/3] Starting FastAPI Backend on http://localhost:8000 ..."
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

sleep 3

# 2. Start Kiosk Frontend in background
echo "[2/3] Starting Hardware Kiosk Frontend on http://localhost:5173 ..."
(cd frontend && npm run dev -- --host 0.0.0.0 --port 5173) &
KIOSK_PID=$!

sleep 2

# 3. Start Web Portal in background
echo "[3/3] Starting Web Portal Frontend on http://localhost:5174 ..."
(cd frontend-web && npm run dev -- --host 0.0.0.0 --port 5174) &
WEB_PID=$!

echo "====================================================================="
echo " All services running in background!"
echo " - API Docs:   http://localhost:8000/docs"
echo " - Kiosk UI:   http://localhost:5173"
echo " - Web Portal: http://localhost:5174"
echo " Press CTRL+C to terminate all servers."
echo "====================================================================="

# Trap exit signal to kill all children
trap "kill $BACKEND_PID $KIOSK_PID $WEB_PID 2>/dev/null" EXIT
wait
