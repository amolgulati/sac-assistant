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
5. **New conversation** — click "New Conversation" in the sidebar to start fresh

Responses stream in real-time, token by token.

## Features

- **Conversational chat** — full multi-turn conversation with context retained across messages
- **Streaming responses** — tokens appear as they're generated, no waiting for the full response
- **Screenshot support** — paste from clipboard or upload an image; the assistant can analyze SAC models, Datasphere views, and error messages
- **Enriched system prompt** — deep knowledge of SAC formulas (MEMBERSET, FOREACH, RESULTLOOKUP, LINK), Datasphere/HANA SQL dialect, planning model structure, and common gotchas; editable in `prompts/system.md`
- **Sidebar controls** — new conversation, image attachment with preview and removal
- **Startup validation** — clear error messages if environment variables are missing

## Example Use Cases

- Generate YTD calculations for revenue measures
- Debug allocation formulas from error screenshots
- Convert Excel logic to Datasphere calculated columns
- Optimize SQL views for performance
- Troubleshoot SAC/Datasphere error messages
- Understand aggregation types and exception aggregation
- Get guidance on planning model design (versions, dimensions, measures)

## Project Structure

```
sac-assistant/
  app.py                 # Streamlit chat application
  prompts/
    system.md            # SAC/Datasphere system prompt (editable)
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

## Databricks Apps Deployment

This repo can be deployed as a Databricks App using the included `app.yaml`.

1. Create the app once:
  ```bash
  databricks apps create sac-assistant -p AmolG
  ```
2. Import the repo to your workspace files:
  ```bash
  databricks workspace mkdirs /Workspace/Users/amol_gulati@oxy.com/sac-assistant -p AmolG
  databricks workspace import-dir . /Workspace/Users/amol_gulati@oxy.com/sac-assistant --overwrite -p AmolG
  ```
3. Deploy the imported source:
  ```bash
  databricks apps deploy sac-assistant \
    --source-code-path /Workspace/Users/amol_gulati@oxy.com/sac-assistant \
    -p AmolG
  ```
4. In the Databricks App configuration, add secret resources for:
  - `API_KEY`
  - `BASE_URL`
  - `MODEL_NAME`

If those environment variables are not configured yet, the app still starts and shows the built-in setup screen instead of failing.
