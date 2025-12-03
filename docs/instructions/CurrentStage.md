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
- `/v1/getTicketGames` proxies structured inputs into an OpenAI prompt (with optional vendor list) to fetch ticket options; uses DI-provided TicketFinderService with web-search when available, falling back to chat completions otherwise.
- `/v1/providers/status` exposes stub provider health response.
- `/v1/profile/me` uses a demo bearer token to return/create a stubbed profile.
- JWT validation available when configured via environment (HS256 path).
- APIError handler returns structured JSON errors for future domain exceptions.

## Architecture Status
- Layering introduced (API router → service → repository). `/getTicketGames` now flows through a TicketFinderService; OpenAI key is injected via settings/env; prompt builder lives in a dedicated helper.
- No infrastructure automation or deployment manifests exist; Dockerfile and requirements are stub-level. OpenAI SDK pinned to `>=1.52.0`; chat fallback remains for older clients.

## Testing & Quality
- No automated tests or CI pipelines yet; linting/type-check steps are still to be configured. Route/service tests added for search, profile, ticket finder, and Mongo DI selection.

## Current Limitations
- `/search` data is static and in-memory; `/getTicketGames` relies on an OpenAI prompt rather than provider integrations.
- Ticket finder lacks provider-backed enrichment and guardrails (rate limiting/retries/observability) around the LLM call.
- Auth is stub/JWT-only; no external IdP wiring yet.
- Observability, rate limiting, error budgets, and production-grade CORS/security settings are not configured.
- Risk mitigation strategies (rate limiting, LLM guardrails) remain unimplemented.
- Layering refinement planned: consolidate LLM logic into one layer (services or endpoints) and move fully to Mongo-backed repositories as the primary store.
