# Phase 1: Core UX — Implementation Plan

> Archive note: this implementation plan has already been executed. The current app includes chat history, streaming, sidebar image handling, startup validation, and an externalized system prompt. Keep this file as implementation history, not as the current source of truth.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the SAC Assistant from a single-turn Q&A form into a streaming conversational chat with enriched SAC/Datasphere system prompt and sidebar controls.

**Architecture:** Single-file Streamlit app (`app.py`) with the system prompt extracted to `prompts/system.md`. Chat history lives in `st.session_state.messages`. Image upload moves to sidebar. Streaming via OpenAI SDK `stream=True` + `st.write_stream`.

**Tech Stack:** Streamlit (chat UI, sidebar), OpenAI Python SDK (streaming completions), python-dotenv, Pillow, streamlit-paste-button

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `prompts/system.md` | Create | Enriched SAC/Datasphere system prompt |
| `app.py` | Rewrite | Chat UI, streaming, sidebar controls, startup validation |

---

### Task 1: Create enriched system prompt

**Files:**
- Create: `prompts/system.md`

- [ ] **Step 1: Create the `prompts/` directory and write `system.md`**

Create `prompts/system.md` with the following content. This replaces the 3-line hardcoded prompt with comprehensive SAC/Datasphere domain knowledge:

```markdown
You are an Expert SAP Analytics Cloud (SAC) and SAP Datasphere Developer.

You help corporate finance users build planning models, write advanced formulas,
design Datasphere SQL views, troubleshoot errors, and follow SAP best practices.

## SAC Formula Syntax

Key functions and patterns:

- **MEMBERSET**: Filter or enumerate dimension members.
  `MEMBERSET([d/Dimension], "[MEMBER_ID]", "[MEMBER_ID2]")`
- **FOREACH**: Iterate over dimension members to apply logic per member.
  `FOREACH([d/CostCenter], MEMBERSET([d/CostCenter], "CC100", "CC200"), ...)`
- **RESULTLOOKUP**: Reference the result of the current calculation for a different member.
  `RESULTLOOKUP([d/Time] = "2026.01")`
- **LINK**: Pull data from a secondary model into a formula context.
  `LINK([Model2:Measure], [d/Dimension1] = [d/Dimension1])`
- **IF / THEN / ELSE**: Conditional logic in advanced formulas.
  `IF([d/Version] = "Actual", [Measures].[Revenue], [Measures].[Plan_Revenue])`

Aggregation types: SUM, AVERAGE, LAST, COUNT, MAX, MIN, NONE, FORMULA.
Exception aggregation overrides the default for specific dimensions.

## Datasphere & HANA SQL

- Datasphere uses SAP HANA SQL dialect, not standard ANSI SQL.
- Key differences from standard SQL:
  - String concatenation: `||` operator (not `CONCAT` for multi-arg)
  - Date functions: `ADD_DAYS()`, `ADD_MONTHS()`, `CURRENT_DATE` (no parentheses)
  - `CASE` expressions work like standard SQL
  - `IFNULL(expr, replacement)` instead of `COALESCE` (though `COALESCE` also works)
  - `TO_DATE('2026-01-01', 'YYYY-MM-DD')` for date parsing
  - `LEFT OUTER JOIN` is common; HANA supports `INNER`, `LEFT/RIGHT/FULL OUTER`, `CROSS`
- Datasphere view types: Graphical Views (no-code) vs. SQL Views (code)
- Analytic Model = consumption layer on top of views; exposes measures + dimensions
- Fact sources need at least one measure; dimension sources need a key column

## Common SAC Gotchas

- **Aggregation type mismatch**: A measure set to SUM that should be LAST (e.g., headcount) produces wrong results in time aggregation.
- **Exception aggregation**: Used when a measure needs different aggregation for different dimensions (e.g., SUM across cost centers but LAST across time).
- **Currency conversion**: Requires a currency conversion table, rate type, and target currency configured in the model. Often fails silently if the rate table is missing entries.
- **Version management**: Versions control data isolation. Public versions are shared; private versions are user-scoped. Planning actions write to a specific version.
- **Data locking**: Locks prevent concurrent edits to the same data slice. Can cause confusing "read-only" behavior if another user holds a lock.
- **Null vs. zero**: SAC treats null (no data) differently from zero. Formulas referencing null cells may return unexpected results.

## Planning Model Structure

- **Versions**: Actual, Budget, Forecast (e.g., v_ACTUAL, v_BUDGET, v_FC01). Each version holds a separate copy of the data.
- **Categories**: Deprecated predecessor to versions in older models. Avoid mixing categories and versions.
- **Measures**: Quantitative values (Revenue, Cost, Headcount). Can be stored as amount, quantity, or price.
- **Dimensions**: Axes of analysis (Time, Entity, Account, CostCenter, Product, etc.).
- **Properties**: Attributes of dimension members (e.g., Region as a property of Entity).
- **Hierarchies**: Parent-child structures within dimensions for drill-down.

## Best Practices

- Use UPPER_SNAKE_CASE for measure and dimension IDs (e.g., `GROSS_REVENUE`, `COST_CENTER`).
- Keep descriptions human-readable; IDs machine-readable.
- Test formulas on a small data slice before applying to full model.
- Use data actions for bulk operations; advanced formulas for cell-level logic.
- In Datasphere, push filtering into SQL views rather than loading excess data into models.
- Prefer graphical views for simple joins/filters; use SQL views for complex logic.

## Response Guidelines

- When shown a screenshot, analyze it carefully and provide specific, actionable guidance.
- Format code blocks with appropriate syntax highlighting (e.g., ```sql, ```python, ```sac).
- Be concise but thorough.
- When writing SAC formulas, always specify which formula type (advanced formula, calculated measure, data action step).
- When writing SQL for Datasphere, specify whether it's for a SQL View, a transformation, or a task chain script.
```

- [ ] **Step 2: Commit the system prompt**

```bash
git add prompts/system.md
git commit -m "feat: add enriched SAC/Datasphere system prompt"
```

---

### Task 2: Rewrite app.py — chat UI, streaming, sidebar, validation

**Files:**
- Rewrite: `app.py`

This is a full rewrite of the 80-line file. The new version implements:
1. Startup validation (check env vars before proceeding)
2. Sidebar with image upload, paste, and "New Conversation" button
3. Chat history in `st.session_state.messages`
4. Streaming responses via `st.write_stream`
5. System prompt loaded from `prompts/system.md`

- [ ] **Step 1: Write the new `app.py`**

Replace the entire contents of `app.py` with:

```python
import base64
import io
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit_paste_button import paste_image_button

load_dotenv()

# ── Startup validation ──────────────────────────────────────────────
REQUIRED_VARS = {"API_KEY": os.getenv("API_KEY"),
                 "BASE_URL": os.getenv("BASE_URL"),
                 "MODEL_NAME": os.getenv("MODEL_NAME")}

missing = [k for k, v in REQUIRED_VARS.items() if not v]
if missing:
    st.set_page_config(page_title="SAC Assistant — Setup", page_icon=":material/assistant:")
    st.error("**Missing environment variables**")
    st.markdown(
        "Create a `.env` file in the project root with the following:\n\n"
        "```\n"
        + "\n".join(f"{k}=your-value-here" for k in missing)
        + "\n```\n\n"
        "Then restart the app."
    )
    st.stop()

# ── Config ───────────────────────────────────────────────────────────
st.set_page_config(page_title="SAC Assistant", page_icon=":material/assistant:", layout="centered")

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
with open(os.path.join(PROMPTS_DIR, "system.md")) as f:
    SYSTEM_PROMPT = f.read()

client = OpenAI(api_key=REQUIRED_VARS["API_KEY"], base_url=REQUIRED_VARS["BASE_URL"])
MODEL = REQUIRED_VARS["MODEL_NAME"]

# ── Session state ────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "image" not in st.session_state:
    st.session_state.image = None  # (bytes, mime_type) or None

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("SAC Assistant")

    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.image = None
        st.rerun()

    st.divider()
    st.subheader("Image Attachment")

    paste_result = paste_image_button("Paste from clipboard", key="paste_btn")
    if paste_result and paste_result.image_data:
        buf = io.BytesIO()
        paste_result.image_data.save(buf, format="PNG")
        st.session_state.image = (buf.getvalue(), "image/png")

    uploaded_file = st.file_uploader(
        "Or upload an image",
        type=["png", "jpg", "jpeg", "gif", "webp"],
        key="file_upload",
    )
    if uploaded_file:
        st.session_state.image = (uploaded_file.getvalue(), uploaded_file.type or "image/png")

    if st.session_state.image:
        st.image(st.session_state.image[0], use_container_width=True)
        if st.button("Remove image", use_container_width=True):
            st.session_state.image = None
            st.rerun()

# ── Chat area ────────────────────────────────────────────────────────
st.title("SAC Assistant")
st.caption("AI-powered help for SAP Analytics Cloud & Datasphere")

# Render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["display"])

# Handle new user input
if prompt := st.chat_input("What do you need help with?"):
    # Build display content (what the user sees in the chat)
    display = prompt
    if st.session_state.image:
        display = prompt  # image shown in sidebar, not inline in chat

    st.session_state.messages.append({"role": "user", "display": display})
    with st.chat_message("user"):
        st.markdown(display)

    # Build API messages
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            api_messages.append({"role": "user", "content": msg.get("api_content", msg["display"])})
        else:
            api_messages.append({"role": "assistant", "content": msg["display"]})

    # Attach image to the current user message (API only — already in sidebar visually)
    if st.session_state.image:
        img_bytes, mime = st.session_state.image
        b64 = base64.b64encode(img_bytes).decode("utf-8")
        api_messages[-1]["content"] = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
        ]
        # Store the multimodal content so future turns include it
        st.session_state.messages[-1]["api_content"] = api_messages[-1]["content"]

    # Stream the response
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=api_messages,
                stream=True,
            )
            response = st.write_stream(stream)
        except Exception as e:
            response = f"**API Error:** {e}"
            st.error(response)

    st.session_state.messages.append({"role": "assistant", "display": response})
```

- [ ] **Step 2: Verify the app runs**

```bash
cd /Users/amol_gulati/Documents/Coding_Projects/SAC-assistant
source .venv/bin/activate
streamlit run app.py
```

Open the browser and verify:
- If `.env` is missing vars, see the setup error page
- Sidebar shows "New Conversation", paste button, file uploader
- Chat input at the bottom works, messages appear in chat bubbles
- Responses stream in token-by-token
- Uploading an image shows it in the sidebar with a "Remove" button
- "New Conversation" clears the chat and image
- Multi-turn conversation works (Claude references earlier messages)

- [ ] **Step 3: Commit the rewrite**

```bash
git add app.py
git commit -m "feat: rewrite app with chat UI, streaming, sidebar controls, and startup validation"
```

---

### Task 3: Manual smoke test

No files changed — this is a verification pass.

- [ ] **Step 1: Test conversation continuity**

Send 2-3 messages in a row and verify the assistant references earlier context. Example:
1. "What's the difference between SUM and LAST aggregation in SAC?"
2. "When would I use exception aggregation for that?"
3. Verify message 2's response references the SUM/LAST context from message 1.

- [ ] **Step 2: Test image attachment**

1. Upload or paste a screenshot in the sidebar
2. Ask "What do you see in this screenshot?"
3. Verify the response describes the image content
4. Click "Remove image", send another message, verify no image is sent

- [ ] **Step 3: Test New Conversation**

1. Have a few messages in the chat
2. Click "New Conversation" in the sidebar
3. Verify the chat is cleared and the input is ready

- [ ] **Step 4: Test startup validation**

1. Temporarily rename `.env` to `.env.bak`
2. Restart the app
3. Verify the setup error page appears with clear instructions
4. Rename `.env.bak` back to `.env`
