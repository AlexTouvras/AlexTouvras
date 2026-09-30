# Smart Mirror — Backend

Smart, small, and resilient backend for the Magic Mirror project (Raspberry Pi).
This repo contains the headless, containerized backend services (time and weather)
designed to run on constrained hardware with an emphasis on reliability and DevOps.

[![CI](https://github.com/AlexTouvras/MagicMirror/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexTouvras/MagicMirror/actions/workflows/ci.yml)

## Overview

Services:
- \`time-service\` — simple time/context API.
- \`weather-service\` — Open-Meteo integration, normalized forecast and summary endpoints.

Architecture principles:
- Containerized services (Docker Compose).
- Config via \`.env\`, secrets via Compose secrets (mounted from \`secrets/\`).
- Persistent cache (host-mounted \`./data\`).
- Startup validation: fail-fast on invalid config.
- Systemd timer on host warms cache periodically.

## Quick start (on the Pi)

bash
## clone (if not already)
git clone git@github.com:AlexTouvras/MagicMirror.git
cd <repo>

## start stack (uses docker compose v2)
docker compose up -d --build

## check services
curl http://localhost:8010/health    # time-service
curl http://localhost:8020/health    # weather-service
curl http://localhost:8020/forecast  # minimal forecast
curl http://localhost:8020/forecast/summary

or 

python3 - <<'PY'
import urllib.request, json
print(urllib.request.urlopen("http://localhost:8010/health", timeout=5).read().decode())
print("-----")
print(urllib.request.urlopen("http://localhost:8020/health", timeout=5).read().decode())
print("-----")
print(urllib.request.urlopen("http://localhost:8020/forecast", timeout=20).read().decode()[:800])
print("-----")
print(urllib.request.urlopen("http://localhost:8020/forecast/summary", timeout=20).read().decode()[:800])
PY

## Project layout

\`\`\`
smart-mirror-backend/
 ├─ docker-compose.yml
 ├─ .env.example
 ├─ services/
 │  ├─ time-service/
 │  └─ weather-service/
 ├─ data/ (host-mounted cache)
 └─ docs/
    └─ runbook.md
\`\`\`

## Ops notes

- Config vs Secrets:
  - Non-secret config in \`.env\` (see \`.env.example\`)
  - Secrets in \`secrets/\` and mounted as Docker secrets.
- Persistent weather cache: \`./data/weather_cache.json\`.
- To force refresh cache (host): \`sudo systemctl start weather-cache-refresh.service\`
- To view logs: \`docker compose logs -f weather-service\`

## Development

- CI (GitHub Actions) validates Python syntax and Dockerfile builds.
- Tagging: use \`git tag now/1.3\` for this milestone.

---

## Contributing
Open a PR against \`main\`. CI must pass before merge.
