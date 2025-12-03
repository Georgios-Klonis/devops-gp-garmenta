# CurrentStage: TicketWise

## Implementation Snapshot
- FastAPI service scaffolded with versioned router, global error handler, CORS policy, and health/root endpoints.
- Domain schemas cover events, listings, prices, search requests/responses, provider health snapshots, user profiles, and favorites.
- Application layer includes in-memory and HTTP provider stubs behind a composite repository, TTL cache stub, SearchService wiring, and dependency helpers with configuration via pydantic settings.
- Mongo-ready repositories exist for search cache and user profiles/favorites (feature-flagged); HS256 JWT validation path added alongside the demo token.
- Logging configured centrally; root `requirements.txt` now installs service dependencies from project root. Control documents remain the source of truth for scope and standards.

## Implemented Features
- `/health` and `/` endpoints confirm service availability.
- `/v1/search` endpoint returns normalized sample events from an in-memory provider with basic filtering and caching.
- `/v1/providers/status` exposes stub provider health response.
- `/v1/profile/me` uses a demo bearer token to return/create a stubbed profile.
- JWT validation available when configured via environment (HS256 path).
- APIError handler returns structured JSON errors for future domain exceptions.

## Architecture Status
- Layering introduced (API router → service → repository) but remains in-memory only; no persistence or provider integrations yet.
- No infrastructure automation or deployment manifests exist; Dockerfile and requirements are stub-level.

## Testing & Quality
- No automated tests or CI pipelines yet; linting/type-check steps are still to be configured.

## Current Limitations
- Search data is static and in-memory; no production provider connectors or LLM workflows.
- Auth is stub/JWT-only; no external IdP wiring yet.
- Observability, rate limiting, error budgets, and production-grade CORS/security settings are not configured.
- Risk mitigation strategies (rate limiting, LLM guardrails) remain unimplemented.
