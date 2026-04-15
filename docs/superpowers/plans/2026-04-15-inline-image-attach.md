# Inline Image Attach — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the sidebar image attachment flow with Streamlit's native file-accepting chat input so screenshots can be pasted, drag-dropped, or picked inline with the message.

**Architecture:** Single-file change to `app.py` plus a `requirements.txt` bump. The chat input gains `accept_file=True` and returns a `ChatInputValue` with `.text` and `.files`. Image bytes are pulled from `user_input.files[0].getvalue()` instead of `st.session_state.image`. Sidebar image section and `streamlit-paste-button` dependency are deleted.

**Tech Stack:** Streamlit 1.43+ (`st.chat_input(accept_file=True)`), OpenAI Python SDK (multimodal content blocks, unchanged).

**Spec:** [2026-04-15-inline-image-attach-design.md](../specs/2026-04-15-inline-image-attach-design.md)

**Note on testing:** The repo has no test suite and the spec defers automated tests — every task below uses manual browser verification instead of pytest. Follow the manual steps exactly; don't skip them just because there's no red/green signal.

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `requirements.txt` | Modify | Bump `streamlit>=1.43.0`; remove `streamlit-paste-button` |
| `app.py` | Modify | Swap sidebar image attach for inline `st.chat_input(accept_file=True)` |

---

### Task 1: Bump Streamlit to 1.43+

This task lands the dependency bump in isolation so we can confirm the existing sidebar flow still works on the newer Streamlit before we rip it out. Leave `streamlit-paste-button` for now — Task 2 removes it together with its last usage.

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Update `requirements.txt`**

Open `requirements.txt` and change the `streamlit` line. The file's other pins stay as-is.

Before:
```
streamlit>=1.31.0
```

After:
```
streamlit>=1.43.0
```

- [ ] **Step 2: Reinstall dependencies**

Run:
```bash
pip install -r requirements.txt
```

Expected: pip upgrades Streamlit (or reports already satisfied if ≥1.43 is installed). `streamlit-paste-button` remains installed.

- [ ] **Step 3: Verify Streamlit version**

Run:
```bash
python -c "import streamlit; print(streamlit.__version__)"
```

Expected: version string ≥ `1.43.0`.

- [ ] **Step 4: Smoke-test the existing app**

Run:
```bash
streamlit run app.py
```

In the browser:
- Open the app (default `http://localhost:8501`)
- Confirm the sidebar still shows "Paste from clipboard" and "Or upload an image"
- Paste a screenshot from clipboard (or upload any image) — the thumbnail should appear in the sidebar
- Type a prompt like "what's in this image?" and send
- Confirm the assistant responds referencing the image

Expected: the old flow works unchanged on Streamlit 1.43+. Stop the server (`Ctrl+C`).

If anything is broken, that's a regression in Streamlit itself — investigate before proceeding.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt
git commit -m "chore: bump streamlit to 1.43+ for chat_input accept_file"
```

---

### Task 2: Switch to inline image attach

This is one coherent atomic change: the chat input, the submit handler, the sidebar block, the session state entry, the imports, and the remaining dependency all move together. An intermediate commit that changed only some of these would leave the app in a half-broken state (sidebar writes to state that's never read, etc.), so everything ships in a single commit.

**Files:**
- Modify: `app.py`
- Modify: `requirements.txt`

- [ ] **Step 1: Remove unused imports**

In [app.py:1–11](app.py:1), delete these two lines:

```python
import io
```
```python
from streamlit_paste_button import paste_image_button
```

After this step, the import block at the top of `app.py` should read:
```python
import base64
import os
import time
from urllib.parse import urlsplit

import requests
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
```

- [ ] **Step 2: Remove `image` from session state init**

In [app.py:137–143](app.py:137), delete the two lines that set up `st.session_state.image`:

Before:
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
if "image" not in st.session_state:
    st.session_state.image = None  # (bytes, mime_type) or None
if "active_project" not in st.session_state:
    st.session_state.active_project = None  # project folder name or None
```

After:
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_project" not in st.session_state:
    st.session_state.active_project = None  # project folder name or None
```

- [ ] **Step 3: Remove image reset from "New Conversation" handler**

In the sidebar "New Conversation" button handler ([app.py:149–152](app.py:149)), delete the `st.session_state.image = None` line.

Before:
```python
    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.image = None
        st.rerun()
```

After:
```python
    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
```

- [ ] **Step 4: Delete the sidebar Image Attachment block**

In [app.py:185–206](app.py:185), delete the entire block starting at the second `st.divider()` inside the `with st.sidebar:` context and running through the end of the sidebar.

Delete these exact lines:
```python
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
        st.image(st.session_state.image[0], use_column_width=True)
        if st.button("Remove image", use_container_width=True):
            st.session_state.image = None
            st.rerun()
```

After this step the `with st.sidebar:` block should end immediately after the project-context token-budget display (the block that prints `~{approx_tokens:,} tokens loaded`).

- [ ] **Step 5: Replace the chat input and submit handler**

In [app.py:217–245](app.py:217), replace the walrus-operator gate and the image-attach block with the new `ChatInputValue`-aware handler.

Before (the entire "Handle new user input" block through the `st.session_state.messages[-1]["api_content"] = ...` line):
```python
# Handle new user input
if prompt := st.chat_input("What do you need help with?"):
    st.session_state.messages.append({"role": "user", "display": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build API messages
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if project_context:
        api_messages.append({
            "role": "system",
            "content": f"--- PROJECT CONTEXT ---\n\n{project_context}\n\n--- END PROJECT CONTEXT ---",
        })
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
```

After:
```python
# Handle new user input
user_input = st.chat_input(
    "What do you need help with?",
    accept_file=True,
    file_type=["png", "jpg", "jpeg", "gif", "webp"],
)

if user_input:
    text = (user_input.text or "").strip()
    files = user_input.files or []
    image_file = files[0] if files else None

    if text or image_file:
        display_text = text if text else "(image attached)"

        st.session_state.messages.append({"role": "user", "display": display_text})
        with st.chat_message("user"):
            st.markdown(display_text)

        # Build API messages
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if project_context:
            api_messages.append({
                "role": "system",
                "content": f"--- PROJECT CONTEXT ---\n\n{project_context}\n\n--- END PROJECT CONTEXT ---",
            })
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                api_messages.append({"role": "user", "content": msg.get("api_content", msg["display"])})
            else:
                api_messages.append({"role": "assistant", "content": msg["display"]})

        # Attach image to the current user message
        if image_file is not None:
            img_bytes = image_file.getvalue()
            mime = image_file.type or "image/png"
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            api_messages[-1]["content"] = [
                {"type": "text", "text": display_text},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ]
            # Store the multimodal content so future turns include it
            st.session_state.messages[-1]["api_content"] = api_messages[-1]["content"]
```

The "Stream the response" block must be indented one additional level to sit inside the `if text or image_file:` branch. Here is the complete final shape of the submit handler (starting at the replaced line and running through the end of the file):

```python
# Handle new user input
user_input = st.chat_input(
    "What do you need help with?",
    accept_file=True,
    file_type=["png", "jpg", "jpeg", "gif", "webp"],
)

if user_input:
    text = (user_input.text or "").strip()
    files = user_input.files or []
    image_file = files[0] if files else None

    if text or image_file:
        display_text = text if text else "(image attached)"

        st.session_state.messages.append({"role": "user", "display": display_text})
        with st.chat_message("user"):
            st.markdown(display_text)

        # Build API messages
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if project_context:
            api_messages.append({
                "role": "system",
                "content": f"--- PROJECT CONTEXT ---\n\n{project_context}\n\n--- END PROJECT CONTEXT ---",
            })
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                api_messages.append({"role": "user", "content": msg.get("api_content", msg["display"])})
            else:
                api_messages.append({"role": "assistant", "content": msg["display"]})

        # Attach image to the current user message
        if image_file is not None:
            img_bytes = image_file.getvalue()
            mime = image_file.type or "image/png"
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            api_messages[-1]["content"] = [
                {"type": "text", "text": display_text},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ]
            # Store the multimodal content so future turns include it
            st.session_state.messages[-1]["api_content"] = api_messages[-1]["content"]

        # Stream the response
        with st.chat_message("assistant"):
            try:
                client = build_client(REQUIRED_VARS["BASE_URL"], REQUIRED_VARS["API_KEY"])
                stream = client.chat.completions.create(
                    model=MODEL,
                    messages=api_messages,
                    stream=True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "display": response})
            except Exception as e:
                st.error(f"**API Error:** {e}")
```

- [ ] **Step 6: Remove `streamlit-paste-button` from `requirements.txt`**

Delete this line from `requirements.txt`:
```
streamlit-paste-button>=0.1.2
```

- [ ] **Step 7: Uninstall the unused package**

Run:
```bash
pip uninstall -y streamlit-paste-button
```

Expected: pip reports it uninstalled the package. If it reports "not installed", that's fine — move on.

- [ ] **Step 8: Start the app and verify imports resolve**

Run:
```bash
streamlit run app.py
```

Expected: the app starts without `ImportError`. Watch the terminal — any `ModuleNotFoundError: No module named 'streamlit_paste_button'` means Step 1 missed a reference.

- [ ] **Step 9: Manual verification — image only (no text)**

In the browser:
1. Copy an image to your clipboard (screenshot or any PNG)
2. Click into the chat input at the bottom of the page
3. Press Cmd+V (macOS) or Ctrl+V (Windows/Linux)

Expected outcomes, in order of preference:
- **Best case:** an image chip appears inside the chat input showing the pasted file
- **Fallback:** paste doesn't register. Instead, click the paperclip icon inside the chat input and pick a PNG from disk, or drag a file from Finder/Explorer onto the chat area

With the image attached and the text field empty, hit Enter.

Expected:
- A user message appears in the transcript reading `(image attached)`
- The assistant streams a response describing/referencing the image
- The chat input's attached file chip clears automatically

If the assistant's response doesn't reference the image, check the network request — the OpenAI payload should contain an `image_url` content block with a `data:image/*;base64,...` URL.

- [ ] **Step 10: Manual verification — text + image**

In the same session:
1. Attach another image (paste, paperclip, or drag)
2. Type `what do you see in this one?`
3. Send

Expected:
- User message shows the typed text (not `(image attached)`)
- Assistant references the new image

- [ ] **Step 11: Manual verification — multi-turn image context**

Without attaching a new image, ask a follow-up like `what color was the background?`. Send.

Expected: assistant answers referencing the previously attached image, proving that the stored `api_content` carried the image forward.

- [ ] **Step 12: Manual verification — text only**

Send a plain text message with no attachment (e.g., `thanks, that's all`).

Expected: normal text exchange, no errors.

- [ ] **Step 13: Manual verification — sidebar has no image section**

Visually confirm the sidebar now contains only:
- "SAC Assistant" header
- "New Conversation" button
- "Project Context" section with project selector and token count

No "Image Attachment" subheader. No paste button. No file uploader. No thumbnail.

- [ ] **Step 14: Manual verification — New Conversation still works**

Click "New Conversation".

Expected: chat history clears. No errors in terminal. App is ready to start a fresh conversation.

- [ ] **Step 15: Stop the app**

`Ctrl+C` in the terminal running `streamlit run`.

- [ ] **Step 16: Commit**

```bash
git add app.py requirements.txt
git commit -m "feat: inline image attach via st.chat_input(accept_file=True)

Replace sidebar paste-button + file-uploader flow with Streamlit's native
file-accepting chat input. Users now paste, drag-drop, or pick images
inline with the message. Removes streamlit-paste-button dependency."
```

---

## Post-Implementation

After Task 2 commits, the change is complete. No further work required for this spec.

If Cmd+V paste doesn't work in the user's primary browser, log which browsers were tested and which methods worked (paperclip, drag-drop, paste) — that's useful context for future UX decisions but doesn't block this slice.

No changelog/README updates needed; the v2 design spec ([2026-04-12-sac-assistant-v2-design.md](../specs/2026-04-12-sac-assistant-v2-design.md)) describes the sidebar flow as-was but is not a user-facing document.
