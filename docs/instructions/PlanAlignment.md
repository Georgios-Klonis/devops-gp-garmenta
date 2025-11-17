# PlanAlignment: TicketWise

## Completed Work
- Base.md captures the canonical problem statement, requirements, and constraints.
- DesignPlan.md, CodingStandards.md, CurrentStage.md, PlanAlignment.md, and Concerns.md are initialized to guide implementation.

## Planned vs. Remaining Scope
- **Search & Aggregation:** Natural-language parsing, provider fan-out, normalization, deduplication, and best-price calculation are not started.
- **User & Favorites:** Authentication, profile CRUD, and favorites personalization logic remain unimplemented.
- **Observability & Ops:** Health/admin endpoints, Application Insights telemetry, and provider monitoring are pending.
- **Performance & Reliability:** Rate limiting, caching, circuit breakers, and graceful degradation logic are TBD.
- **CI/CD & Tooling:** FastAPI project scaffolding, Docker image, lint/test tooling, and Azure DevOps pipelines have not been created.

## Upcoming Technical Tasks
1. Scaffold FastAPI project structure, dependency injection wiring, and shared config management.
2. Stand up CI/CD (linting, formatting, mypy, unit tests, container build/push) and Dockerfile for Azure App Service.
3. Implement NL query parsing workflow with PydanticAI and deterministic validation.
4. Build first provider connector (official API) plus normalization/deduplication pipeline backed by MongoDB.
5. Deliver `/search` endpoint with caching, best-price computation, and health checks.
6. Add authentication integration, user profile storage, and favorites CRUD endpoints.
7. Instrument Application Insights, expose admin/health endpoints, and define provider monitoring dashboard.
8. Extend provider coverage, add personalization hooks, and prepare for alerts/recommendations roadmap.

## Future Refactors / Technical Debt to Monitor
- Potential need to split provider ingestion into separate worker processes if throughput grows.
- Evaluate storing historical price snapshots for analytics—could require additional collections or cold storage.
- Revisit MongoDB schema design before traffic scales to ensure partitioning strategy aligns with Azure Cosmos limits.
- Determine whether personalization weighting belongs in search ranking or a separate recommendation module once MVP stabilizes.
