# PlanAlignment: TicketWise

## Completed Work
- Base.md captures the canonical problem statement, requirements, and constraints.
- DesignPlan.md, CodingStandards.md, CurrentStage.md, PlanAlignment.md, and Concerns.md are initialized to guide implementation.
- FastAPI API-service scaffolded with health/root endpoints, structured error handling, versioned router, and stubbed `/v1/search` backed by in-memory provider + cache.
- Added provider health endpoint `/v1/providers/status`, central configuration (pydantic settings), dependency wiring, provider aggregation (in-memory + optional HTTP stub), and baseline logging setup.
- Auth stub with `/v1/profile/me`, user/favorites schemas, and in-memory profile repository.
- Pricing helper marks best-price listings per event.
- Root-level `requirements.txt` points to service dependencies for simpler installs; API service requirements now pin `openai>=1.52.0`.
- Mongo-ready repositories for search cache and profiles/favorites (feature-flagged), plus optional HS256 JWT validation path.
- LLM-backed `/v1/getTicketGames` endpoint added (via TicketFinderService with vendor list support and settings-driven OpenAI key/model).
- Scrum Master (Sprint 1): Georgios.
- Added route/service tests for ticket finder and Mongo DI selection; search/profile tests retained.
- GitHub Actions workflow builds the FastAPI backend image from `src/backend/services/api-service`, pushes `latest` and `${GITHUB_SHA}` tags to `tickaiacr.azurecr.io`, and deploys the container to the `tickai-app` Azure Web App.
- Deployment job now configures the Web App to pull commit-tagged images from ACR, injects Cosmos DB (`tickai-db`) connection settings (`TW_MONGODB_URI/DB_NAME`), toggles Mongo-backed repositories, and disables stub data in the hosted environment.

## Planned vs. Remaining Scope
- **Search & Aggregation:** `/v1/search` remains in-memory; real provider connectors, normalization/deduplication/pricing, and guarded LLM parsing are still pending. `/v1/getTicketGames` now uses a service layer and env-configured OpenAI key but still relies on LLM prompting instead of provider integrations.
- **User & Favorites:** Authentication provider (JWT/IdP) and personalization logic remain unimplemented; demo token only, though Cosmos-backed repositories are now wired via env vars.
- **Observability & Ops:** Structured telemetry, Application Insights wiring, and provider monitoring are pending beyond the basic health endpoint.
- **Performance & Reliability:** Real caching, circuit breakers, rate limiting, and graceful degradation are TBD; Cosmos indexes/backups and Key Vault-backed secrets are still pending.
- **CI/CD & Tooling:** Backend pipeline now builds/pushes to ACR and deploys to App Service, but still lacks lint/test gates, artifact reuse for other services, and environment promotion controls.
- **LLM workflow:** Ticket finder still LLM+web-search only; lacks provider-backed enrichment and guardrails (rate limiting/retries/observability).
- **Layering/Repos:** Plan to consolidate LLM prompt/orchestration into a single layer (services or endpoints, not both) and fully standardize on Mongo-backed repositories as the primary store.

## Upcoming Technical Tasks
1. Harden FastAPI project structure with config management, dependency injection, and logging/telemetry hooks.
2. Extend CI/CD to run lint/format/type checks, publish test results, and gate deployments before promoting containers built/pushed to ACR.
3. Move Cosmos/App Service secrets to Key Vault + managed identity instead of GitHub secrets; add collection/index provisioning scripts.
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
