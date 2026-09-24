#!/usr/bin/env bash
# Build & deploy the KIOSK frontend + backend to a kiosk machine (Linux).
# Run this ON the kiosk machine (or adapt paths for remote deploy).
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WEB_ROOT=/var/www/kiosk

echo "==> [1/5] Building kiosk frontend (production)..."
cd "$APP_DIR/frontend"
[ -d node_modules ] || npm install
# Point the frontend at the same-origin API (nginx proxies /api/v1 -> :8000)
export VITE_API_BASE_URL=/api/v1
npm run build

echo "==> [2/5] Installing static files to $WEB_ROOT..."
sudo mkdir -p "$WEB_ROOT"
sudo rm -rf "$WEB_ROOT"/*
sudo cp -r dist/* "$WEB_ROOT"/
sudo chown -R www-data:www-data "$WEB_ROOT"

echo "==> [3/5] Syncing backend to /opt/coop-assistant..."
sudo mkdir -p /opt/coop-assistant
sudo rsync -a --delete \
  --exclude '.venv' --exclude 'node_modules' --exclude '.git' --exclude 'frontend-web' --exclude '.venv' \
  "$APP_DIR"/ /opt/coop-assistant/
cd /opt/coop-assistant
[ -d .venv ] || sudo python3 -m venv .venv
sudo .venv/bin/pip install -r requirements.txt

echo "==> [4/5] Installing systemd services..."
sudo cp "$APP_DIR/deploy/backend.service" "$APP_DIR/deploy/kiosk-browser.service" /etc/systemd/system/
sudo cp "$APP_DIR/deploy/nginx-kiosk.conf" /etc/nginx/sites-available/kiosk
sudo ln -sf /etc/nginx/sites-available/kiosk /etc/nginx/sites-enabled/kiosk
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl daemon-reload
sudo systemctl enable --now backend
sudo systemctl enable --now nginx
sudo systemctl enable --now kiosk-browser

echo "==> [5/5] Done. Kiosk should boot to fullscreen UI at http://localhost"
echo "    Backend health: curl http://localhost:8000/docs"
