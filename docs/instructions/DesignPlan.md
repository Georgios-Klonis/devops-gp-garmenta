# DesignPlan: TicketWise

## Architecture Summary
TicketWise is a Python-based modular monolith built on FastAPI. The runtime is organized into clearly separated layers (API, Application Services, Domain, Infrastructure) that can later be split into independent services. LLM-powered workflows (via PydanticAI) normalize user queries and provider payloads, while asynchronous provider connectors aggregate and deduplicate ticket listings. MongoDB (Cosmos DB) stores normalized events, listings cache, user profiles, and favorites. Application Insights captures logs, metrics, and traces. The system is containerized and deployed to Azure App Service with images stored in Azure Container Registry.

## Functional Requirements
- Natural-language and structured search for sports events (team, league, date, location).
- Aggregation of ticket listings from configured provider APIs or approved scraping targets.
- LLM workflows that parse intent, normalize metadata, and map inconsistent provider fields.
- User authentication, profile management, and ability to save favorites.
- Computation of best ticket price per event, returning normalized results.
- Admin/health endpoints for readiness/liveness and provider ingest status.
- Extensible design that can add alerts, recommendations, and new event categories.

## Non-Functional Requirements
- **Performance:** median search latency <2–4 seconds end-to-end; async providers; caching of recent searches.
- **Reliability:** ≥99% uptime, circuit breakers/fallback behavior when providers fail, durable provider ingest retries.
- **Security:** HTTPS-only, JWT-based auth, secrets in Key Vault/App Service config, audit logging for critical actions.
- **Scalability:** Azure App Service horizontal scaling; stateless API tier; workloads packaged as containers.
- **User Experience:** minimalist UI fed by clear, human-friendly API responses; normalized pricing units.
- **Compliance:** respect provider ToS and GDPR (consent, deletion workflows, encrypted data at rest/in transit).
- **Quality Bar:** SOLID, clean architecture, strict linting/type-checking, ≥90% automated test coverage.

## Component-Level Design
### API Layer
- FastAPI routers expose `/search`, `/favorites`, `/profile`, `/auth`, `/admin/health`, and `/providers/status` endpoints.
- Pydantic models define request/response contracts with validation.
- Authentication middleware verifies JWT/session tokens.

### LLM Orchestration Service
- PydanticAI workflows parse NL search input into structured intents (team, league, price sensitivity, date, venue).
- Another workflow normalizes provider listing payloads (seat quality, section, currency) to the canonical model.
- Prompt templates stored in version-controlled configs with guardrails (tool calling limited to deterministic helpers).

### Provider Aggregation & Normalization
- Provider connectors implement a shared interface with async fetch, rate-limit handling, and retries.
- Connectors either call official APIs or scraping adapters that stay within allowed terms.
- Listings flow into a normalization pipeline (LLM-assisted + deterministic business rules) and are cached in MongoDB with TTL indexes.
- Deduplication service merges listings by provider_event_id + normalized seat hash.

### Pricing & Ranking Engine
- Applies currency conversion, fee normalization, and selects the best price per event.
- Supports future ranking heuristics (e.g., favorites boost, seat quality weighting) via pluggable strategy objects.

### User Profiles & Favorites
- Auth service integrates with JWT provider (custom or Azure AD B2C) and stores user documents in MongoDB.
- Favorites service links users to teams/leagues and influences personalized searches (phase-two feature flag).

### Background Jobs
- Scheduler (Azure Functions timer or FastAPI background tasks) periodically refreshes provider catalogs and invalidates stale caches.
- Application Insights telemetry is emitted for job success/failure and provider latency metrics.

### Observability & Admin
- Health endpoints expose API readiness and provider connectivity checks.
- Application Insights ingestion of structured logs, distributed traces, and custom metrics (search latency, LLM cost, provider availability).

## Data Model Highlights
- `User`: auth_id, profile info, preferences, favorites list, notification settings.
- `Favorite`: user_id, entity_type (team/league), entity_ref, metadata.
- `Event`: normalized_id, teams, league, venue, datetime, provider_refs.
- `TicketListing`: event_id, provider_id, seat_details, price.amount/currency, url, freshness metadata, best_price flag.
- `ProviderStatus`: provider_id, last_success_at, failure_counts, rate_limit_state.

## Tech Stack Reasoning
- **FastAPI** provides async HTTP handling, automatic OpenAPI docs, and works well with Pydantic.
- **PydanticAI** ensures structured contracts around LLM interactions, reducing hallucination risk with validators.
- **MongoDB** (Cosmos DB) supports schemaless storage for variable provider payloads and TTL caching; global distribution available.
- **Azure App Service + ACR** simplifies container deployment, scaling, and secret injection via Key Vault references.
- **Application Insights** supplies centralized logging/tracing, satisfying the observability-first requirement.
- **Azure DevOps Pipelines** enforce CI/CD with linting, type checks (mypy), unit/integration tests, and container builds.

## Testing & Quality Model
- **Unit tests:** domain models, provider adapters (with fakes), pricing engine, favorites logic.
- **Integration tests:** FastAPI endpoints via TestClient; provider connector contract tests using sandbox fixtures; Mongo interactions using ephemeral databases.
- **LLM workflow tests:** use deterministic test prompts/responses with golden files to detect prompt regressions.
- **Performance tests:** load tests for `/search` and provider fan-out to maintain <4s median latency.
- **Security tests:** JWT middleware, role enforcement, and dependency scans in CI.
- Coverage gates enforce ≥90% statements/branches; tests run in CI before container build/push.

## Milestones
1. **M1 – Foundation:** Repo scaffolding, FastAPI skeleton, CI/CD, CodingStandards, empty doc set.
2. **M2 – Search MVP:** Implement NL parsing workflow, 1–2 provider connectors, normalization pipeline, `/search` endpoint, caching, initial unit/integration tests.
3. **M3 – User & Favorites:** Auth integration, Mongo user store, favorites endpoints, personalization hooks (feature-flagged), profile UI/API alignment.
4. **M4 – Observability & Ops:** Health/admin endpoints, provider monitoring, Application Insights dashboards, automated alerts.
5. **M5 – Hardening:** Add additional providers, performance tuning, reliability failovers, rounding out ≥90% coverage, readiness for alerts/recommendations roadmap.

## Risks & Open Questions
- Provider blocking or ToS changes reduce data quality; mitigated via caching tiers and diversified providers.
- LLM hallucination may mislabel events—requires guardrails, validators, and human-readable fallbacks.
- Mongo as single store could become bottleneck; plan sharding/partitioning strategy early.
- Need clarity on storing historical prices and whether favorites influence MVP ranking.
- Determine explicit provider list for M2 and whether price-drop alerts are MVP scope or later.
