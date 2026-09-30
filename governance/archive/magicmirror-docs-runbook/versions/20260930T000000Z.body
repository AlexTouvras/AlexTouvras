# Smart Mirror Backed - Runbook

## What this is 
Containerized backed services running on a Raspberry Pi using Docker Compose.
Autostart is handled by systemd.

Repo location on Pi:
- /home/pi/smart-mirror-backend

## Services & Ports
- time-service:http://localhost:8010
-weather-service: http://localhost:8020

Health endpoints:
- GET /health

Time-service endpoints:
- GET /time
- GET /context

## Start/Stop (systemd)
Start:
- sudo systemctl start smart-mirror.backend.service

Stop:
- sudo systemctl stop smart-mirror-backend.service

Status:
- sudo systemctl status smart-mirror-backend.service --no-pager
- sudo journalctl -u smart-mirror-backend.service -b --no-pager -n 200

## Start/Stop )manual via Compose)
From /home/pi/smart-mirror-backend:
- docker compose up -d
- docker compose down 
- docker compose ps
- docker compose logs -f time-service

## Config (.env)
- .env is local-only (ignored by git)
- .env.example is the template

After changing .env:
Run on PI: 
- python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8010/health').read().decode())"
- python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8020/health').read().decode())"

## Deployment (safe + deterministic)
Boot should NOT build images

Recommended deploy flow:
1) git pull
2) docker compose build 
3) docker compose up -d --remove-orphans 
4) verify /health endpoints 

## Persistent cache for Weather Service

- Cache file: ./data/weather_cache.json
- Refresher: systemd timer `weather-cache-refresh.timer` (every 15 minutes)
- To force refresh: sudo systemctl start weather-cache-refresh.service
- Cache file is read on service startup into in-memory cache

## 1.4 — Service autostart & recovery (CLOSED)

- systemd timer `weather-cache-refresh.timer` installed on host to warm cache.
- Cache file mounted into container at `./data/weather_cache.json`.
- Docker Compose set up with service restart policy (restart: unless-stopped).
- Weather service validated to fail-fast on invalid config.
- Recovery test: container restart verified manually (killed & auto restarted).

To force a cache refresh on the host:
  sudo systemctl start weather-cache-refresh.service

To force a service restart (container):
  docker compose restart weather-service

To view logs:
  docker compose logs -f weather-service

