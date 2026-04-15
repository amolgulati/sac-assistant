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

Local development expects a `.env` file. Databricks Apps deployment can rely on injected app credentials instead of a local `API_KEY`.

## Configuration

All config lives in `.env`:

| Variable | Required | Description | Example |
| -------- | -------- | ----------- | ------- |
| `API_KEY` | Local only unless Databricks App auth is available | API key or access token for an OpenAI-compatible endpoint | `sk-...` |
| `BASE_URL` | Yes | OpenAI-compatible API base URL | `https://api.openai.com/v1` |
| `MODEL_NAME` | Yes | Model to use | `gpt-4o` |

The app uses the standard OpenAI SDK, so any OpenAI-compatible endpoint works (OpenAI, Azure, Databricks AI Gateway, etc.).

If `API_KEY` is not set, the app can still start inside a Databricks App when `DATABRICKS_CLIENT_ID` and `DATABRICKS_CLIENT_SECRET` are injected by the platform. In that mode the app exchanges those credentials for a short-lived Databricks OAuth token automatically.

If any variables are missing on startup, the app shows a friendly setup page with instructions instead of a cryptic error.

## Usage

1. **Start the app** — `streamlit run app.py`
2. **Chat** — type questions in the chat input at the bottom of the page
3. **Attach screenshots** — paste, drag-drop, or pick an image directly in the chat input via the paperclip icon; the image sends with your next message
4. **Multi-turn conversation** — the assistant remembers your full conversation, so you can ask follow-ups
5. **New conversation** — click "New Conversation" in the sidebar to start fresh
6. **Project-aware mode** — pick a project in the sidebar to load `_project.md` plus all `.md` and `.txt` files from that project folder into context

Responses stream in real-time, token by token.

## Features

- **Conversational chat** — full multi-turn conversation with context retained across messages
- **Streaming responses** — tokens appear as they're generated, no waiting for the full response
- **Screenshot support with visual annotations** — attach images inline in the chat input (paste, drag-drop, or paperclip picker); the assistant analyzes SAC models, Datasphere views, and error messages, and returns annotated screenshots with numbered markers (circles, arrows, highlights) pointing at exactly where to click and what to change
- **Enriched system prompt** — deep knowledge of SAC formulas (MEMBERSET, FOREACH, RESULTLOOKUP, LINK), Datasphere/HANA SQL dialect, planning model structure, and common gotchas; editable in `prompts/system.md`
- **Project context loading** — select a project folder and inject its markdown/text docs into the model context automatically
- **Token budget visibility** — sidebar shows approximate project-context size so you can trim oversized context sets
- **Sidebar controls** — new conversation, project context selector with token-budget display
- **Startup validation** — clear error messages if environment variables or auth inputs are missing
- **Databricks App auth fallback** — local `API_KEY` for desktop use, OAuth token exchange for Databricks Apps

## Example Use Cases

- Generate YTD calculations for revenue measures
- Debug allocation formulas from error screenshots
- Convert Excel logic to Datasphere calculated columns
- Optimize SQL views for performance
- Troubleshoot SAC/Datasphere error messages
- Understand aggregation types and exception aggregation
- Get guidance on planning model design (versions, dimensions, measures)

## Project Structure

```text
sac-assistant/
  app.py                 # Streamlit chat application
  annotator.py           # Draws annotation markers on screenshot images (planned)
  response_parser.py     # Extracts annotation JSON from model responses (planned)
  app.yaml               # Databricks App entrypoint/config
  docs/                  # Design specs and implementation plans
  projects/              # Optional project context folders
  prompts/
    system.md            # SAC/Datasphere system prompt (editable)
  tests/                 # pytest tests for annotator and parser (planned)
  requirements.txt       # Python dependencies
  .env.example           # Configuration template
  .env                   # Your configuration (not committed)
```

## Corporate Deployment

Designed for locked-down environments:

- **No OS-level automation** — no PyAutoGUI, keyboard hooks, or screen capture
- **No external calls required** — point `BASE_URL` to an internal endpoint (e.g. Databricks AI Gateway)
- **No admin privileges needed** — pure Python, runs in user space
- **Minimal dependencies** — four well-known packages (Streamlit, OpenAI SDK, python-dotenv, Pillow)

## Databricks Apps Deployment

This repo can be deployed as a Databricks App using the included `app.yaml`.

The checked-in `app.yaml` provides default values for:

- `BASE_URL`
- `MODEL_NAME`

That means a Databricks deployment typically only needs auth configured unless you want to override those defaults.

1. Create the app once:

  ```bash
  databricks apps create sac-assistant -p AmolG
  ```

1. Import the repo to your workspace files:

  ```bash
  databricks workspace mkdirs /Workspace/Users/amol_gulati@oxy.com/sac-assistant -p AmolG
  databricks workspace import-dir . /Workspace/Users/amol_gulati@oxy.com/sac-assistant --overwrite -p AmolG
  ```

1. Deploy the imported source:

  ```bash
  databricks apps deploy sac-assistant \
    --source-code-path /Workspace/Users/amol_gulati@oxy.com/sac-assistant \
    -p AmolG
  ```

1. In the Databricks App configuration, provide one of these auth patterns:

- Preferred: Databricks App credentials via injected `DATABRICKS_CLIENT_ID` and `DATABRICKS_CLIENT_SECRET`
- Alternative: explicit `API_KEY`

1. Override `BASE_URL` and `MODEL_NAME` only if the `app.yaml` defaults are not correct for your workspace.

If auth or required environment variables are not configured yet, the app still starts and shows the built-in setup screen instead of failing.
