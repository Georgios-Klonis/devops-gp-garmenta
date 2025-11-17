# Base: TicketWise

## One-Sentence Summary
A modular-monolith platform that uses LLM workflows to find, aggregate, and deliver the best-priced sports tickets to users, with support for personalization through favorites and natural-language queries.

## Problem & Context
- Sports ticket marketplaces are fragmented, forcing fans to check multiple sources manually.
- Pricing formats, seat-quality descriptions, and naming conventions vary per provider, making comparisons difficult.
- There is no unified system that normalizes events, venues, and prices across providers.
- Users want a single, reliable interface that surfaces the best deals despite provider inconsistencies.

## Goals & Vision
### Primary Goals
1. Deliver accurate, LLM-assisted ticket searches that highlight the current best price per event.
2. Provide a seamless browsing experience for sports events with normalized metadata.
3. Enable personalization through user favorites and saved preferences.
4. Maintain ≥90% automated test coverage to guard critical workflows.
5. Build a scalable modular monolith that can later be decomposed into services.

### Vision
- Offer intelligent alerts for price drops and personalized recommendations driven by user interests.
- Expand coverage beyond sports to concerts and other live events.
- Become the "Skyscanner for event tickets" while remaining compliant with provider policies.

## Target Users & Personas
1. **Casual Sports Fans** – want cheap seats occasionally; prefer natural-language search like "cheap Barca tickets Saturday".
2. **Devoted Team Followers** – track specific teams; rely on favorites and alerts.
3. **Deal Seekers** – aggressively compare prices across providers for best deals.
4. **Students & Budget-Conscious Users** – need affordable options quickly with filters for price ceilings, locations, and dates.

## Functional Requirements
1. Search for sports events by team, league, location, date, or natural-language prompts.
2. Aggregate ticket listings from multiple provider APIs or approved scraping targets.
3. Use LLM workflows to parse, normalize, and enrich user queries and provider data.
4. Allow users to authenticate, manage profiles, and save favorite teams/organizations.
5. Compute, normalize, and return best ticket prices with consistent metadata (teams, venues, dates, seating details).
6. Expose admin/health endpoints for operational insight.
7. Keep the architecture extensible for future alerting, recommendations, and new event categories.

## Non-Functional Requirements
### Performance
- Median ticket search latency under 2–4 seconds depending on provider response times, with streaming updates when possible.

### Reliability
- 99%+ uptime target with graceful degradation if one or more providers fail or rate-limit requests.

### Security
- HTTPS-only endpoints with JWT (or session token) authentication and secrets stored in Azure Key Vault / App Service config.

### Scalability
- Horizontal scaling via Azure App Service instances; modular monolith boundaries allow future extraction of services.

### User Experience
- Minimalist frontend with clear pricing, normalized event details, and human-friendly phrasing when presenting LLM output.

### Compliance
- Respect provider scraping/usage policies and enforce GDPR-aligned data handling.

### Other Quality Expectations
- Observe SOLID and clean architecture principles and enforce strict linting, type checking, and ≥90% automated test coverage.

## Technical Preferences & Stack
- **Language:** Python (primary language for APIs and workflows).
- **Frameworks:** FastAPI for the HTTP boundary; PydanticAI for LLM-powered orchestration and validation.
- **Storage / Database:** MongoDB (Azure Cosmos DB with Mongo API) for user data, preferences, normalized events, and provider cache.
- **Deployment:** Containerized FastAPI app deployed to Azure App Service with images stored in Azure Container Registry.
- **Integrations:** Mix of ticket provider APIs and compliant scraping; Azure OpenAI or OpenAI API for LLM calls; Application Insights for observability.
- **DevOps Preferences:** Observability-first instrumentation, automated CI/CD through Azure DevOps, strict linting, and type checking.

## Constraints & Assumptions
### Constraints
- Provider APIs may impose rate limits or block high-volume requests.
- Scraping is only permitted for providers whose terms of service allow it.
- LLM latency adds overhead to query workflows and must be accounted for in UX.

### Assumptions
- Provider APIs or HTML structures are available to gather ticket data legally.
- Users accept slightly slower AI-assisted searches in exchange for higher-quality normalization.
- MVP UI can remain basic while the backend establishes core capabilities.

## Risks & Open Questions
### Risks
- Provider availability or blocking may limit coverage.
- LLM hallucinations could hurt normalization accuracy and price selection.
- Complex events with inconsistent naming may break deduplication logic.
- LLM and provider API usage costs could escalate with traffic growth.

### Open Questions
- Should the system store historical ticket prices for analytics or trend-based recommendations?
- Should user favorites influence recommendations within the MVP scope or only later?
- Which providers deliver the initial integration set for launch?
- Are price-drop alerts part of the MVP or deferred to a future milestone?
