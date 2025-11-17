# CodingStandards: TicketWise

## Guiding Principles
- Favor clean architecture boundaries (API ↔ application services ↔ domain ↔ infrastructure) with dependency flow inward.
- Prefer readability and explicitness over clever abstractions; small, composable functions with clear responsibilities.
- Apply SOLID principles and domain-driven naming; keep business logic framework-agnostic.
- Treat observability, security, and testing as first-class requirements rather than add-ons.

## Architecture & Patterns
- Use FastAPI routers per bounded context (search, favorites, admin) and dependency injection for services.
- Implement provider connectors with a shared abstract base, supporting strategy and adapter patterns for provider-specific quirks.
- Encapsulate LLM workflows (PydanticAI) behind service classes with typed inputs/outputs and validators.
- Keep MongoDB access behind repositories/gateways; never query directly from controllers.
- Feature flags (e.g., personalization) should rely on a configuration provider, enabling gradual rollout.

## Style & Language Conventions
- Python 3.11+, strict type hints everywhere; enable `from __future__ import annotations` when beneficial.
- Follow `black` formatting, `isort` ordering, and `ruff` linting defaults; enforce in CI.
- Pydantic models define external contracts; internal domain models can be dataclasses or pydantic models depending on validation needs.
- Avoid mutable default arguments and implicit truthiness for important decisions.

## Error Handling & Logging
- Convert provider and LLM failures into domain-specific exceptions with actionable messages.
- Never swallow exceptions—log context (provider, request id, ticket id) at WARN/ERROR level with structured logs.
- Return sanitized error responses; internal details belong in logs/Application Insights only.
- Include correlation IDs (trace/span ids) in log entries and propagate them through external calls.

## Testing Requirements
- Minimum 90% statement and branch coverage enforced via CI.
- Unit tests for domain services, pricing logic, provider adapters, and LLM normalization helpers using deterministic fixtures.
- Integration tests hitting FastAPI routers via TestClient with realistic Mongo/test doubles.
- Contract tests per provider connector validating schema mapping and error handling.
- Snapshot/golden tests for LLM prompts/responses to detect drift.
- Include negative tests (rate-limit, malformed input) for resilience.

## Security Practices
- Enforce HTTPS, HSTS, and JWT/session validation on every protected route.
- Secrets and API keys must come from Azure Key Vault/App Service configuration; never commit secrets.
- Input validation via Pydantic; escape/encode any data rendered in UI.
- Apply least privilege on Mongo collections and Azure resources; audit access regularly.
- Log security events (auth failures, admin actions) with severity tagging.

## Performance & Observability
- Use async IO for provider calls and database operations; avoid blocking operations in request handlers.
- Cache recent search results and provider metadata with TTL indexes to reduce repeated calls.
- Emit metrics for search latency, provider fan-out duration, LLM usage, and cache hit ratios.
- Use Application Insights OpenTelemetry integration for traces; include dependency IDs for provider calls.
- Profile critical code paths before optimizing; document findings.

## Documentation & Readability
- Add docstrings to public modules/classes/functions describing purpose and key parameters.
- Keep prompt templates, provider mappings, and configuration documented in `docs/` or inline Markdown tables.
- Update control documents (DesignPlan, CurrentStage, PlanAlignment, Concerns) whenever scope or implementation changes.
- Provide ADR-style notes for non-obvious architectural decisions.

## Review Checklist
- [ ] Does the change respect architecture boundaries and dependency directions?
- [ ] Are inputs validated and errors handled with structured logging?
- [ ] Do new features include adequate unit/integration tests and keep coverage ≥90%?
- [ ] Are LLM prompts/results validated and deterministic where possible?
- [ ] Are security/privacy implications addressed (auth, PII, secrets)?
- [ ] Are performance implications measured or justified (provider calls, DB queries)?
- [ ] Are docs/control files updated to match the implementation?
