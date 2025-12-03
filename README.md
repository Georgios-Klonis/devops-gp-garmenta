TicketWise – Modular Monolith for sports ticket search.

## Sprint Plan
- Sprint 0 (completed): Framed the concept, defined high-level architecture, and assigned initial roles.
- Sprint 1 (in progress, Scrum Master: Georgios): Backend foundation. Goals: stand up FastAPI service skeleton, define schemas for events/listings/search, wire a search endpoint (stubbed provider + cache), add an LLM-backed ticket finder endpoint, and prepare documentation for implementation standards.

## Current Progress (Sprint 1)
- FastAPI API service scaffolded with health/root endpoints, structured error handler, versioned router, and DI wiring.
- `/v1/search` endpoint returns normalized sample events from an in-memory provider with a TTL cache (stub data only; no live provider connectors or pricing normalization yet).
- `/v1/getTicketGames` proxies structured inputs into an LLM+web-search prompt (OpenAI) to locate ticket offers; supports vendor preference list; uses `TicketFinderService` and DI, returns JSON. Still LLM-only with no provider-backed enrichment or guardrails (rate limiting/retries/observability).
- Domain schemas defined for prices, seats, listings, events, search requests/responses, and `GetTicketGamesSchema` aligning to the LLM endpoint inputs.
- `/v1/providers/status` exposes stubbed provider health information.
- Auth stub added with `/v1/profile/me` protected by a demo bearer token (`demo-token`); optional HS256 JWT validation path.
- Config, dependency wiring, provider aggregation (in-memory + optional HTTP stub), and basic logging added via pydantic settings and shared helpers.
- Mongo-ready repositories for search cache and profiles (feature-flagged via settings).
- OpenAI SDK pinned to `>=1.52.0`; OpenAI key/model/web-search toggle configurable via settings/env.
- Tests added/updated: API tests for search/profile/ticket finder; service tests for ticket finder (responses vs chat), search service, and Mongo DI selection.
- Instructions updated to reflect the new baseline, LLM endpoint, and remaining scope; Sprint 1 Scrum Master: Georgios.

## Run the API locally
- Ensure Python 3.11+ (use `python`, not `python3` on Windows) and install deps: `pip install -r requirements.txt`
- Start the service: `uvicorn app.main:app --reload --app-dir src/backend/services/api-service`
- Health check: `GET http://127.0.0.1:8000/health`
- Search sample: `POST http://127.0.0.1:8000/v1/search` with body `{"query": "Barcelona"}`
- Ticket finder (LLM): `POST http://127.0.0.1:8000/v1/getTicketGames` with body:
  ```json
  {
    "team_1": "Real Madrid",
    "team_2": "Barcelona",
    "date_from": "2025-01-15",
    "date_to": "2025-03-15",
    "price_from": "50",
    "price_to": "200",
    "preferred_vendors": ["Ticketmaster", "StubHub", "Viagogo"]
  }
  ```
- Provider status: `GET http://127.0.0.1:8000/v1/providers/status`
- Profile (auth stub): `GET http://127.0.0.1:8000/v1/profile/me` with header `Authorization: Bearer demo-token`
- JWT validation (optional): set `TW_JWT_SECRET`, `TW_JWT_ISSUER`, and `TW_JWT_AUDIENCE` to enable HS256 JWT auth.
- Mongo (optional): set `TW_MONGODB_URI` and toggle `TW_USE_MONGO_CACHE=true` / `TW_USE_MONGO_PROFILES=true` to persist cache/profiles.
- OpenAI: install `openai>=1.52.0` (now in requirements). Set `TW_OPENAI_API_KEY` (or `OPENAI_API_KEY`) for the ticket finder endpoint.

## Tests
- Run tests from repo root: `python -m pytest tests`

## Deployment (Azure)
- Container images are built from `src/backend/services/api-service` and pushed to `tickaiacr.azurecr.io/devops-gp-garmenta/backend` on every push to `main` via `.github/workflows/backend-push-build-deploy.yml`.
- The workflow deploys the freshly built image to the `tickai-app` Azure Web App in resource group `BCSAI2025-DEVOPS-STUDENT-3A`, setting the container image tag to the current commit and restarting the app.
- Cosmos DB for MongoDB (`tickai-db`) is wired through App Service settings: the workflow updates `TW_MONGODB_URI` (from the `COSMOS_CONNECTION_STRING` GitHub secret), sets `TW_MONGODB_DB_NAME`, and toggles `TW_USE_MONGO_CACHE/TW_USE_MONGO_PROFILES` plus `TW_ENABLE_STUB_DATA=false`.
- Required GitHub secrets: `AZURE_CREDENTIALS` (service principal JSON), `ACR_USERNAME`, `ACR_PASSWORD`, and `COSMOS_CONNECTION_STRING`. Add environment vars/secrets for other dependencies (e.g., `TW_OPENAI_API_KEY`) as needed.
- To troubleshoot locally, you can run `az webapp log tail --name tickai-app --resource-group BCSAI2025-DEVOPS-STUDENT-3A` after authenticating with `az login`.

## Upcoming backend focus
- Replace stub provider with first real connector + normalization mapping.
- Enable Mongo-backed cache/profiles in environments with `TW_USE_MONGO_*` toggles; validate collections/indexes.
- Swap demo token for real JWT/IdP config and tighten CORS/auth defaults.
- Align LLM prompt helpers and orchestration into a single layer (services or endpoints, not both) and move fully to Mongo-backed repositories as the primary store.

## Team (initial roles)
- Backend: Georgios, Nikoloz
- Frontend: Kareem, Faisal
- DevOps: Jose Maria, Greg
- LLM Integration: Nikoloz, Georgios

Roles can adjust in future sprints, but these are the current owners for Sprint 1 delivery.
