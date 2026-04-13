# SAC Assistant

AI-powered conversational assistant for SAP Analytics Cloud (SAC) and SAP Datasphere development. Chat with an expert co-pilot that understands SAC formulas, Datasphere SQL, planning models, and common gotchas — with streaming responses and screenshot support.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then edit .env with your values
streamlit run app.py
```

## Configuration

All config lives in `.env`:

| Variable     | Description                              | Example                        |
|-------------|------------------------------------------|--------------------------------|
| `API_KEY`   | API key or access token                  | `sk-...`                       |
| `BASE_URL`  | OpenAI-compatible API base URL           | `https://api.openai.com/v1`    |
| `MODEL_NAME`| Model to use (must support vision)       | `gpt-4o`                       |

The app uses the standard OpenAI SDK, so any OpenAI-compatible endpoint works (OpenAI, Azure, Databricks AI Gateway, etc.).

If any variables are missing on startup, the app shows a friendly setup page with instructions instead of a cryptic error.

## Usage

1. **Start the app** — `streamlit run app.py`
2. **Chat** — type questions in the chat input at the bottom of the page
3. **Attach screenshots** — paste from clipboard or upload in the sidebar; the image stays attached until you remove it
4. **Multi-turn conversation** — the assistant remembers your full conversation, so you can ask follow-ups
5. **Load project context** — select a project from the sidebar dropdown to give the assistant knowledge of your specific dimensions, conventions, and status
6. **New conversation** — click "New Conversation" in the sidebar to start fresh (also resets automatically when you switch projects)

Responses stream in real-time, token by token.

## Features

- **Conversational chat** — full multi-turn conversation with context retained across messages
- **Streaming responses** — tokens appear as they're generated, no waiting for the full response
- **Screenshot support** — paste from clipboard or upload an image; the assistant can analyze SAC models, Datasphere views, and error messages
- **Project context** — load project-specific files (dimensions, conventions, status) so the assistant gives guidance tailored to what you're building
- **Token budget display** — sidebar shows approximate token count of loaded context with warnings when approaching limits
- **Enriched system prompt** — deep knowledge of SAC formulas (MEMBERSET, FOREACH, RESULTLOOKUP, LINK), Datasphere/HANA SQL dialect, planning model structure, and common gotchas; editable in `prompts/system.md`
- **Sidebar controls** — new conversation, project selector, image attachment with preview and removal
- **Startup validation** — clear error messages if environment variables are missing

## Example Use Cases

- Generate YTD calculations for revenue measures
- Debug allocation formulas from error screenshots
- Convert Excel logic to Datasphere calculated columns
- Optimize SQL views for performance
- Troubleshoot SAC/Datasphere error messages
- Understand aggregation types and exception aggregation
- Get guidance on planning model design (versions, dimensions, measures)

## Project Context

The assistant can load project-specific context to give tailored guidance. Create a folder under `projects/` with a `_project.md` file:

```
projects/
  _template/             # Copy this to start a new project
    _project.md
  fy26-forecast/         # Example: your project folder
    _project.md          # Required — project overview, dimensions, conventions
    prd.md               # Optional — additional context files (.md, .txt)
    meeting-notes.txt    # Optional — any supporting documentation
```

1. Copy `projects/_template/` to a new folder (e.g., `projects/fy26-forecast/`)
2. Edit `_project.md` with your project's dimensions, measures, conventions, and status
3. Add any additional `.md` or `.txt` files for extra context (PRDs, meeting notes, etc.)
4. Select the project from the sidebar dropdown — the assistant will reference your specific setup

The `_project.md` file is always loaded first, followed by remaining files alphabetically. Switching projects clears the conversation since the context changes.

## Project Structure

```
sac-assistant/
  app.py                 # Streamlit chat application
  prompts/
    system.md            # SAC/Datasphere system prompt (editable)
  projects/
    _template/
      _project.md        # Starter template for new projects
  requirements.txt       # Python dependencies
  .env.example           # Configuration template
  .env                   # Your configuration (not committed)
```

## Corporate Deployment

Designed for locked-down environments:

- **No OS-level automation** — no PyAutoGUI, keyboard hooks, or screen capture
- **No external calls required** — point `BASE_URL` to an internal endpoint (e.g. Databricks AI Gateway)
- **No admin privileges needed** — pure Python, runs in user space
- **Minimal dependencies** — five well-known packages
