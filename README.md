# SAC Assistant

AI-powered assistant for SAP Analytics Cloud (SAC) and SAP Datasphere development. Paste a screenshot, ask a question, and get expert guidance — formulas, SQL, troubleshooting steps, and best practices.

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

## Usage

1. **Take a screenshot** of your SAC model, Datasphere view, or error message
2. **Paste it** using the clipboard button, or upload a file
3. **Type your question** (e.g. "Why is my allocation formula not distributing correctly?")
4. **Submit** and get a formatted response with code blocks and actionable steps

## Example Use Cases

- Generate YTD calculations for revenue measures
- Debug allocation formulas from error screenshots
- Convert Excel logic to Datasphere calculated columns
- Optimize SQL views for performance
- Troubleshoot SAC/Datasphere error messages

## Corporate Deployment

Designed for locked-down environments:

- **No OS-level automation** — no PyAutoGUI, keyboard hooks, or screen capture
- **No external calls required** — point `BASE_URL` to an internal endpoint (e.g. Databricks AI Gateway)
- **No admin privileges needed** — pure Python, runs in user space
- **Minimal dependencies** — five well-known packages
