# PlanAlignment: TicketWise

## Completed Work
- Base.md captures the canonical problem statement, requirements, and constraints.
- DesignPlan.md, CodingStandards.md, CurrentStage.md, PlanAlignment.md, and Concerns.md are initialized to guide implementation.
- FastAPI API-service scaffolded with health/root endpoints, structured error handling, versioned router, and stubbed `/v1/search` backed by in-memory provider + cache.
- Added provider health endpoint `/v1/providers/status`, central configuration (pydantic settings), dependency wiring, provider aggregation (in-memory + optional HTTP stub), and baseline logging setup.
- Auth stub with `/v1/profile/me`, user/favorites schemas, and in-memory profile repository.
- Pricing helper marks best-price listings per event.
- Root-level `requirements.txt` points to service dependencies for simpler installs.
- Mongo-ready repositories for search cache and profiles/favorites (feature-flagged), plus optional HS256 JWT validation path.

## Planned vs. Remaining Scope
- **Search & Aggregation:** `/v1/search` exists with in-memory data only; real provider connector + normalization/deduplication/pricing and LLM parsing remain to be delivered.
- **User & Favorites:** Authentication provider (JWT/IdP), persistent profile/favorites storage, and personalization logic remain unimplemented; demo token only.
- **Observability & Ops:** Structured telemetry, Application Insights wiring, and provider monitoring are pending beyond the basic health endpoint.
- **Performance & Reliability:** Real caching, circuit breakers, rate limiting, and graceful degradation are TBD.
- **CI/CD & Tooling:** Dockerfile/requirements exist but pipelines, lint/test tooling, and automation have not been created.

## Upcoming Technical Tasks
1. Harden FastAPI project structure with config management, dependency injection, and logging/telemetry hooks.
2. Stand up CI/CD (linting, formatting, mypy, unit tests, container build/push) and Dockerfile for Azure App Service.
3. Implement NL query parsing workflow with PydanticAI and deterministic validation.
4. Build first provider connector (official API) plus normalization/deduplication pipeline backed by MongoDB.
5. Extend `/search` with caching, best-price computation, and health/admin checks.
6. Add authentication integration, user profile storage, and favorites CRUD endpoints.
7. Instrument Application Insights, expose admin/health endpoints, and define provider monitoring dashboard.
8. Extend provider coverage, add personalization hooks, and prepare for alerts/recommendations roadmap.

## Future Refactors / Technical Debt to Monitor
- Potential need to split provider ingestion into separate worker processes if throughput grows.
- Evaluate storing historical price snapshots for analytics—could require additional collections or cold storage.
- Revisit MongoDB schema design before traffic scales to ensure partitioning strategy aligns with Azure Cosmos limits.
- Determine whether personalization weighting belongs in search ranking or a separate recommendation module once MVP stabilizes.
