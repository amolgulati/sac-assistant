# SAC Assistant — Development Plan

This file is kept for historical reference. The active design spec is:

**[SAC Assistant v2 Design Spec](docs/superpowers/specs/2026-04-12-sac-assistant-v2-design.md)**

Current implementation also includes Databricks App deployment support via `app.yaml` and runtime auth fallback to Databricks App OAuth when `API_KEY` is not provided.

## Status

| Phase | Description | Status |
| ----- | ----------- | ------ |
| Phase 1 | Core UX — chat history, streaming, enriched system prompt, sidebar controls, startup validation | Done |
| Phase 2 | Project Context — project folders, selector, context loader, token budget display | Done |
| Deployment | Databricks App runtime config and OAuth token exchange fallback | Done |
| Phase 3 | Polish — PDF/DOCX support, per-file toggle, export conversation, code block copy | Not started |
