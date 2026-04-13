import base64
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """You are an Expert SAP Analytics Cloud (SAC) and SAP Datasphere Developer.

You help corporate finance users build planning models, write advanced formulas,
design Datasphere SQL views, troubleshoot errors, and follow SAP best practices.

When shown a screenshot, analyze it carefully and provide specific, actionable guidance.
Format code blocks with appropriate syntax highlighting (e.g. ```sql, ```python).
Be concise but thorough."""

st.set_page_config(page_title="SAC Assistant", page_icon=":material/assistant:", layout="centered")

st.title("SAC Assistant")
st.caption("AI-powered help for SAP Analytics Cloud & Datasphere")

uploaded_file = st.file_uploader(
    "Paste or upload a screenshot",
    type=["png", "jpg", "jpeg", "gif", "webp"],
)

if uploaded_file:
    st.image(uploaded_file, use_container_width=True)

question = st.text_area("What do you need help with?", placeholder="e.g. Why is my allocation formula not distributing correctly?")

if st.button("Submit", type="primary", disabled=not question):
    # Build messages
    user_content = [{"type": "text", "text": question}]

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        mime = uploaded_file.type or "image/png"
        user_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"},
        })

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

    with st.spinner("Thinking..."):
        try:
            client = OpenAI(
                api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"),
            )
            response = client.chat.completions.create(
                model=os.getenv("MODEL_NAME"),
                messages=messages,
            )
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"API Error: {e}")
