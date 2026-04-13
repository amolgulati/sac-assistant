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
    st.session_state.messages.append({"role": "user", "display": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
            st.session_state.messages.append({"role": "assistant", "display": response})
        except Exception as e:
            st.error(f"**API Error:** {e}")
