# Implementation Contract

## Mission

Ship a durable, inspectable agentic OS baseline that closes the loop on local computer work.

## First Milestone

Closed-loop local execution with verification and learning on a deterministic task graph.

## Safety Posture

- No destructive shell commands by default
- No network side effects
- Verification gate before completion
- Evidence written at every phase

## Proof-of-Progress Metrics

- goals created
- tasks created
- tasks verified complete
- median runtime per task
- retry count
- intervention count
- eval pass rate
- memory updates written

## Verification Strategy

- unit/integration test via `unittest`
- demo run via CLI
- artifact existence/content verification
- status mirror written to markdown
