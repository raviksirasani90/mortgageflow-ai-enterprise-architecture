# ADR 0001: Start with a Modular Monolith

- **Status:** Accepted
- **Date:** 2026-10-17

## Context

Mortgage origination includes application intake, document processing, validation, workflow orchestration, and audit logging. Deploying every capability as a separate microservice at the beginning would add operational complexity before service boundaries and scaling requirements are understood.

## Decision

Start with a modular monolith using FastAPI. Keep application, document, underwriting, workflow, and integration responsibilities logically separated in the codebase.

## Consequences

### Benefits

- Faster initial development and testing
- Simpler local setup and deployment
- Clear logical boundaries for future service extraction
- Lower initial operational overhead

### Trade-offs

- Modules initially share a deployment lifecycle
- Strong module boundaries and interface discipline are required
- Independent scaling is unavailable until components are extracted

## Future Evolution

Extract modules into separate services when justified by scaling, security isolation, deployment independence, or team ownership. Use API contracts and events to reduce coupling during migration.
