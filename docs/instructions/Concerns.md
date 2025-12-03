# Concerns: TicketWise

## Requirement Ambiguities
- Clarity is needed on whether price-drop alerts and recommendation weighting of favorites are MVP scope or deferred features.
- Provider integration priorities (which APIs, what access levels) are unspecified, affecting milestones and contract testing.
- Decision pending on storing historical ticket prices for analytics and whether it is mandatory for launch.

## Architecture Concerns
- Relying on a single MongoDB/Cosmos account could become a bottleneck; need partitioning and failover planning early.
- Modular monolith must enforce strict boundaries; without tooling, it could devolve into a big-ball-of-mud and block future decomposition.

## Implementation Risks
- Provider APIs may throttle or block scraping, requiring caching, rate-limit backoff, and alternative sources.
- LLM workflows may hallucinate or mislabel events, causing incorrect normalization and pricing; requires validators and fallback heuristics.
- LLM and provider usage costs can escalate quickly without budget monitoring or request throttling.
- Early endpoints rely on permissive CORS and in-memory data; must be replaced with secured auth, persistence, and validated provider connectors before exposure.

## Performance & Security Issues to Watch
- LLM latency could push searches beyond 4 seconds if provider fan-out is serialized; concurrency and caching strategy must be proven.
- Aggregating user favorites and search history introduces GDPR obligations (right to delete, consent) not yet detailed.
- Secrets management must strictly rely on Key Vault/App Service; any deviation risks leaking provider credentials.

## Open Questions
- Are alerts part of the MVP feature set or should they be designed but disabled?
- Which authentication provider or identity store (e.g., Azure AD B2C, custom JWT) will be used initially?
- What SLA targets do provider partners guarantee, and how should we surface degradation to users?
- Should MVP personalization weight favorites in ranking automatically, or remain opt-in until more data exists?
