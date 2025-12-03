TicketWise – Modular Monolith for sports ticket search.

## Sprint Plan
- Sprint 0 (completed): Framed the concept, defined high-level architecture, and assigned initial roles.
- Sprint 1 (in progress): Backend foundation. Goals: stand up FastAPI service skeleton, define schemas for events/listings/search, wire a search endpoint (stubbed provider + cache), and prepare documentation for implementation standards.

## Current Progress
- FastAPI API service scaffolded with health/root endpoints, structured error handler, and versioned router.
- `/v1/search` endpoint returns normalized sample events from an in-memory provider with a simple TTL cache.
- Domain schemas defined for prices, seats, listings, events, and search requests/responses.
- `/v1/providers/status` exposes stubbed provider health information.
- Auth stub added with `/v1/profile/me` protected by a demo bearer token (`demo-token`).
- Config, dependency wiring, provider aggregation (in-memory + optional HTTP stub), and basic logging added via pydantic settings and shared helpers.
- Mongo-ready repositories for search cache and profiles (toggle via settings) plus HS256 JWT validation path when configured.
- Instructions updated to reflect the new baseline and remaining scope.

## Run the API locally
- Ensure Python 3.11+ (use `python`, not `python3` on Windows) and install deps: `pip install -r requirements.txt`
- Start the service: `uvicorn app.main:app --reload --app-dir src/backend/services/api-service`
- Health check: `GET http://127.0.0.1:8000/health`
- Search sample: `POST http://127.0.0.1:8000/v1/search` with body `{"query": "Barcelona"}`
- Provider status: `GET http://127.0.0.1:8000/v1/providers/status`
- Profile (auth stub): `GET http://127.0.0.1:8000/v1/profile/me` with header `Authorization: Bearer demo-token`
- JWT validation (optional): set `TW_JWT_SECRET`, `TW_JWT_ISSUER`, and `TW_JWT_AUDIENCE` to enable HS256 JWT auth.
- Mongo (optional): set `TW_MONGODB_URI` and toggle `TW_USE_MONGO_CACHE=true` / `TW_USE_MONGO_PROFILES=true` to persist cache/profiles.

## Tests
- Run tests from repo root: `python -m pytest tests`

## Upcoming backend focus
- Replace stub provider with first real connector + normalization mapping.
- Enable Mongo-backed cache/profiles in environments with `TW_USE_MONGO_*` toggles; validate collections/indexes.
- Swap demo token for real JWT/IdP config and tighten CORS/auth defaults.

## Team (initial roles)
- Backend: Georgios, Nikoloz
- Frontend: Kareem, Faisal
- DevOps: Jose Maria, Greg
- LLM Integration: Nikoloz, Georgios

Roles can adjust in future sprints, but these are the current owners for Sprint 1 delivery.
