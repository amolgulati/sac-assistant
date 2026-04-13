# SAC Assistant — Development Plan

Active design spec: **[SAC Assistant v2 Design Spec](docs/superpowers/specs/2026-04-12-sac-assistant-v2-design.md)**

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Core UX — chat history, streaming, enriched system prompt, sidebar controls, startup validation | Done |
| Phase 2 | Project Context — project folders, selector, context loader, token budget display | Done |
| Phase 3 | Polish — PDF/DOCX support, per-file toggle, export conversation, code block copy | Not started |

## What's Implemented

- Multi-turn conversational chat with full context retention
- Real-time streaming responses (token by token)
- Screenshot support (paste from clipboard or file upload)
- Enriched system prompt with SAC/Datasphere domain knowledge (`prompts/system.md`)
- Project context system — load project-specific `.md`/`.txt` files from `projects/`
- Sidebar project selector with automatic discovery
- Token budget display with warnings at 60k+ and errors at 80k+ tokens
- Startup validation with clear setup instructions
- Sidebar controls for conversation, project, and image management

## What's Next (Phase 3)

- PDF/DOCX support for project context files
- Per-file toggles to selectively include/exclude context
- Export conversation to markdown
- Code block copy buttons in responses

See the [design spec](docs/superpowers/specs/2026-04-12-sac-assistant-v2-design.md) for full details on Phase 3.
