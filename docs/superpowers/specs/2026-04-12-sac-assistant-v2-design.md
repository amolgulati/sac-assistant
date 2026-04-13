# SAC Assistant v2 — Design Spec

## Overview

Transform the SAC Assistant from a single-turn Q&A form into a project-aware conversational co-pilot for SAP Analytics Cloud and Datasphere development.

Three vertical slices, each independently shippable. Each phase is a single focused session (~60-90 min).

## Current State

Single-file Streamlit app (`app.py`, ~200 lines) with enriched system prompt in `prompts/system.md`. Phases 1 and 2 are complete: multi-turn conversational chat with streaming responses, screenshot support (paste + upload), project context system with folder discovery and token budget display, sidebar controls, and startup validation. Phase 3 (polish) is not yet started.

---

## Phase 1: Core UX ✓

**Goal:** Transform from one-shot Q&A form into a real chat experience.

**Estimated effort:** ~90 min

### 1.1 Conversation History

- Replace `st.text_area` + `st.button` with `st.chat_input` / `st.chat_message`
- Store messages in `st.session_state.messages` (list of `{"role": ..., "content": ...}`)
- Full history sent to the API each turn so Claude has conversation context
- Image attachments stored in message history and displayed inline

### 1.2 Streaming Responses

- Switch from `client.chat.completions.create()` to `stream=True`
- Render tokens as they arrive via `st.write_stream`
- Eliminates the `st.spinner("Thinking...")` blocking wait

### 1.3 Enriched System Prompt

- Extract system prompt from `app.py` to `prompts/system.md`
- Loaded at startup via `open().read()`
- Expand content to include:
  - SAC formula syntax: MEMBERSET, FOREACH, RESULTLOOKUP, LINK, etc.
  - Datasphere / HANA SQL specifics and dialect differences from standard SQL
  - Common SAC gotchas: aggregation types, exception aggregation, currency conversion, version management
  - Planning model structure: versions, categories, measures, dimensions
  - Best practices for model design and formula writing
- Editable without touching Python code

### 1.4 Sidebar Controls

- "New Conversation" button to clear `st.session_state.messages`
- Image upload (paste + file upload) moves to sidebar to keep the chat area clean
- Uploaded image shown as thumbnail in sidebar with option to remove

### 1.5 Startup Validation

- On launch, check that `API_KEY`, `BASE_URL`, `MODEL_NAME` env vars are set
- If any are missing, show a clear setup message with instructions instead of letting the app proceed to a cryptic API error

### Files Changed

| File | Action |
|------|--------|
| `app.py` | Rewrite — chat UI, streaming, sidebar, validation |
| `prompts/system.md` | Create — enriched system prompt |

---

## Phase 2: Project Context ✓

**Goal:** Make the assistant project-aware so it gives guidance specific to what you're building.

**Estimated effort:** ~90 min

**Depends on:** Phase 1 (conversation history must exist)

### 2.1 Project Folder Structure

```
projects/
  _template/
    _project.md          <- starter template to copy for new projects
  fy26-forecast/         <- example user project
    _project.md
    prd.md
    meeting-notes.md
```

- Each subdirectory of `projects/` with a `_project.md` file is a selectable project
- `_template/` provides a starting point for new projects

### 2.2 `_project.md` Template

Structured file with sections:

```markdown
# Project Name

## What We're Building
Brief description of the project scope and objectives.

## Key Dimensions
- Entity: ...
- Time: ...
- Version: ...
- Measures: ...

## Current Status
- Phase/step 1: DONE / IN PROGRESS / NOT STARTED
- Phase/step 2: ...

## Conventions
- Measure IDs: UPPER_SNAKE_CASE
- Version naming: v_ACTUAL, v_BUDGET, v_FC01
- ...
```

### 2.3 Sidebar Project Selector

- Dropdown populated by scanning `projects/` for valid subdirectories
- Options: "No project" (default) + each discovered project
- Selection stored in `st.session_state.active_project`
- Switching projects clears conversation history (context changes)

### 2.4 Context Loader

- When a project is active, load all `.md` and `.txt` files from that project folder
- `_project.md` is always loaded first
- Remaining files loaded in alphabetical order
- Flat loading only (no subdirectory recursion)
- No binary files
- Concatenated content injected as a system message between the system prompt and conversation history, delimited with `--- PROJECT CONTEXT ---` headers

### 2.5 Token Budget Display

- Show approximate token count of loaded context in the sidebar
- Estimation: `len(text) // 4` (rough but sufficient)
- Visual warning (orange/red) when context exceeds ~80k tokens
- Helps user decide whether to trim project files or disable some

### Files Changed

| File | Action |
|------|--------|
| `app.py` | Modify — add project scanning, selector, context injection |
| `projects/_template/_project.md` | Create — starter template |

---

## Phase 3: Polish

**Goal:** Round out the tool for daily-driver use and make it shareable.

**Estimated effort:** ~60 min

**Depends on:** Phase 2 (project context must exist)

### 3.1 PDF/DOCX Support

- Add `pypdf` and `python-docx` to `requirements.txt`
- Extend context loader to parse `.pdf` and `.docx` files alongside `.md`/`.txt`
- Meeting transcripts and PRDs can be dropped into project folders as-is
- Text extraction only (no images from PDFs)

### 3.2 Per-File Toggle

- Sidebar shows list of files in the active project with checkboxes
- All files enabled by default
- Unchecking a file excludes it from the context sent to the API
- Toggling a file clears conversation history (context changed)
- State stored in `st.session_state`

### 3.3 Export Conversation

- "Export to Markdown" button in sidebar
- Dumps the full conversation to a `.md` file:
  - Header with timestamp, active project name, model name
  - Each message with role label and content
  - Code blocks preserved
- Timestamped filename: `export-2026-04-12-143022.md`
- Downloaded via `st.download_button`

### 3.4 Code Block Copy

- Replace raw `st.markdown` response rendering with logic that detects fenced code blocks
- Render code blocks via `st.code(code, language=lang)` which provides built-in copy buttons
- Non-code portions of the response still rendered via `st.markdown`

### Files Changed

| File | Action |
|------|--------|
| `app.py` | Modify — file parsers, toggles, export, code rendering |
| `requirements.txt` | Modify — add `pypdf`, `python-docx` |

---

## Out of Scope

These are explicitly deferred and not part of this plan:

- **CLI interface** — Streamlit is the interface; no separate CLI tool
- **Persistent conversation storage** — `st.session_state` only; no database
- **Authentication / multi-user** — single-user tool for now
- **RAG / embeddings** — full file loading is sufficient at current scale
- **SAC/Datasphere API integration** — tool suggests, user executes
- **Context auto-summarization** — manual file management for now

## Dependencies

### Current (`requirements.txt`)
- `streamlit>=1.31.0`
- `openai>=1.12.0`
- `python-dotenv>=1.0.0`
- `Pillow>=10.0.0`
- `streamlit-paste-button>=0.1.2`

### Added in Phase 3
- `pypdf>=4.0.0`
- `python-docx>=1.0.0`

## Success Criteria

- **Phase 1:** ✓ Can have a multi-turn conversation about a SAC model with screenshots, responses stream in real-time, system prompt produces noticeably better SAC-specific answers
- **Phase 2:** ✓ Can load a project folder, paste a screenshot, and get guidance that references your specific dimension names, conventions, and project status
- **Phase 3:** Can drop a PDF meeting transcript into a project folder and have it inform responses; can export a useful conversation to share with a colleague
