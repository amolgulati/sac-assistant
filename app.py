import base64
import json
import logging
import os
import re
import time
from urllib.parse import urlsplit

import requests
import streamlit as st
from annotator import annotate
from dotenv import load_dotenv
from openai import OpenAI

logger = logging.getLogger(__name__)

load_dotenv()

_TOKEN_CACHE = {"access_token": None, "expires_at": 0}


def _normalize_workspace_host(base_url):
    parts = urlsplit(base_url.strip())
    if not parts.scheme or not parts.netloc:
        raise RuntimeError("BASE_URL must be a valid absolute URL.")
    return f"{parts.scheme}://{parts.netloc}"


def get_databricks_access_token(base_url):
    access_token = _TOKEN_CACHE.get("access_token")
    expires_at = int(_TOKEN_CACHE.get("expires_at", 0))
    if access_token and expires_at > int(time.time()) + 30:
        return access_token

    client_id = os.getenv("DATABRICKS_CLIENT_ID")
    client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError(
            "Databricks app credentials are unavailable. Set API_KEY for local use or run inside a Databricks App."
        )

    token_url = f"{_normalize_workspace_host(base_url)}/oidc/v1/token"
    response = requests.post(
        token_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "client_credentials", "scope": "all-apis"},
        auth=(client_id, client_secret),
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    access_token = payload.get("access_token")
    if not access_token:
        raise RuntimeError("Databricks OAuth response did not include an access token.")

    _TOKEN_CACHE["access_token"] = access_token
    _TOKEN_CACHE["expires_at"] = int(time.time()) + int(payload.get("expires_in", 300))
    return access_token


def build_client(base_url, api_key):
    resolved_api_key = api_key or get_databricks_access_token(base_url)
    return OpenAI(api_key=resolved_api_key, base_url=base_url)


_ANNOTATION_BLOCK_RE = re.compile(r'\n?```annotations\s*([\s\S]*?)```', re.MULTILINE)


def parse_response(text: str) -> tuple:
    """Split model response into (text_content, annotations_list or None).

    Extracts the trailing ```annotations ... ``` block if present.
    Returns the clean text (block removed) and a parsed list of dicts.
    Falls back to (original_text, None) on any parse error.
    """
    match = _ANNOTATION_BLOCK_RE.search(text)
    if not match:
        return text, None
    try:
        annotations = json.loads(match.group(1).strip())
        if not isinstance(annotations, list) or not annotations:
            return text, None
        text_content = (text[: match.start()] + text[match.end():]).strip()
        return text_content, annotations
    except json.JSONDecodeError:
        logger.warning("Failed to parse annotations JSON from model response")
        return text, None

# ── Startup validation ──────────────────────────────────────────────
REQUIRED_VARS = {"API_KEY": os.getenv("API_KEY"),
                 "BASE_URL": os.getenv("BASE_URL"),
                 "MODEL_NAME": os.getenv("MODEL_NAME")}

has_databricks_app_auth = bool(os.getenv("DATABRICKS_CLIENT_ID") and os.getenv("DATABRICKS_CLIENT_SECRET"))
missing = [k for k, v in REQUIRED_VARS.items() if not v and k != "API_KEY"]
if not REQUIRED_VARS["API_KEY"] and not has_databricks_app_auth:
    missing.append("API_KEY or Databricks app auth")

if missing:
    st.set_page_config(page_title="SAC Assistant — Setup", page_icon=":material/assistant:")
    st.error("**Missing environment variables**")
    st.markdown(
        "Create a `.env` file in the project root with the following:\n\n"
        "```\n"
        + "\n".join(
            "API_KEY=your-value-here"
            if k == "API_KEY or Databricks app auth"
            else f"{k}=your-value-here"
            for k in missing
        )
        + "\n```\n\n"
        "For Databricks Apps, you can omit API_KEY and rely on the injected app credentials instead."
    )
    st.stop()

# ── Config ───────────────────────────────────────────────────────────
st.set_page_config(page_title="SAC Assistant", page_icon=":material/assistant:", layout="centered")

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")
PROJECTS_DIR = os.path.join(os.path.dirname(__file__), "projects")

with open(os.path.join(PROMPTS_DIR, "system.md")) as f:
    SYSTEM_PROMPT = f.read()

MODEL = REQUIRED_VARS["MODEL_NAME"]


# ── Project helpers ─────────────────────────────────────────────────
def discover_projects():
    """Return sorted list of project folder names that contain a _project.md."""
    if not os.path.isdir(PROJECTS_DIR):
        return []
    projects = []
    for entry in sorted(os.listdir(PROJECTS_DIR)):
        if entry.startswith("_"):
            continue
        project_dir = os.path.join(PROJECTS_DIR, entry)
        if os.path.isdir(project_dir) and os.path.isfile(os.path.join(project_dir, "_project.md")):
            projects.append(entry)
    return projects


def load_project_context(project_name):
    """Load all .md and .txt files from a project folder. Returns concatenated text."""
    project_dir = os.path.join(PROJECTS_DIR, project_name)
    files = [f for f in os.listdir(project_dir)
             if os.path.isfile(os.path.join(project_dir, f))
             and f.lower().endswith((".md", ".txt"))]

    # _project.md first, then the rest alphabetically
    files.sort()
    if "_project.md" in files:
        files.remove("_project.md")
        files.insert(0, "_project.md")

    sections = []
    for fname in files:
        with open(os.path.join(project_dir, fname)) as f:
            content = f.read()
        sections.append(f"### {fname}\n\n{content}")

    return "\n\n".join(sections)

# ── Session state ────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_project" not in st.session_state:
    st.session_state.active_project = None  # project folder name or None

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("SAC Assistant")

    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # ── Project selector ────────────────────────────────────────────
    st.divider()
    st.subheader("Project Context")

    projects = discover_projects()
    options = ["No project"] + projects
    current_idx = 0
    if st.session_state.active_project in projects:
        current_idx = options.index(str(st.session_state.active_project))

    selected = st.selectbox("Active project", options, index=current_idx, key="project_select")
    new_project = None if selected == "No project" else selected

    if new_project != st.session_state.active_project:
        st.session_state.active_project = new_project
        st.session_state.messages = []  # context changed — clear conversation
        st.rerun()

    # Token budget display
    if st.session_state.active_project:
        project_context = load_project_context(st.session_state.active_project)
        approx_tokens = len(project_context) // 4
        if approx_tokens > 80_000:
            st.error(f"~{approx_tokens:,} tokens loaded — may exceed context window")
        elif approx_tokens > 60_000:
            st.warning(f"~{approx_tokens:,} tokens loaded — approaching limit")
        else:
            st.info(f"~{approx_tokens:,} tokens loaded")
    else:
        project_context = None

    # ── Image attachment toggle ─────────────────────────────────────
    st.divider()
    attach_images = st.toggle(
        "Enable image attach",
        value=False,
        help="Turn on to attach images via paperclip or drag-drop. "
             "Leave off for normal Ctrl+V text paste.",
    )

# ── Chat area ────────────────────────────────────────────────────────
st.title("SAC Assistant")
st.caption("AI-powered help for SAP Analytics Cloud & Datasphere")

# Render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("annotated_image"):
            st.image(msg["annotated_image"],
                     caption="Annotated screenshot",
                     use_container_width=True)
        st.markdown(msg["display"])

# Handle new user input
if attach_images:
    user_input = st.chat_input(
        "What do you need help with?",
        accept_file=True,
        file_type=["png", "jpg", "jpeg", "gif", "webp"],
    )
else:
    user_input = st.chat_input("What do you need help with?")

if user_input:
    if attach_images:
        text = (user_input.text or "").strip()
        files = user_input.files or []
        image_file = files[0] if files else None
    else:
        text = user_input.strip() if isinstance(user_input, str) else (user_input.text or "").strip()
        image_file = None

    # Defensive: Streamlit's exact accept_file semantics for empty submissions aren't
    # documented, so guard here in case ChatInputValue arrives with neither text nor files.
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
        current_image_bytes = None
        if image_file is not None:
            img_bytes = image_file.getvalue()
            current_image_bytes = img_bytes  # keep original for annotator
            mime = image_file.type or "image/png"
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            api_messages[-1]["content"] = [  # type: ignore[assignment]
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
                # Stream into a placeholder so we can replace it with the annotated version
                placeholder = st.empty()
                with placeholder.container():
                    response = st.write_stream(stream)

                text_content, annotations = parse_response(response)

                annotated_bytes = None
                if annotations and current_image_bytes:
                    try:
                        annotated_bytes = annotate(current_image_bytes, annotations)
                        with placeholder.container():
                            st.image(annotated_bytes,
                                     caption="Annotated screenshot",
                                     use_container_width=True)
                            st.markdown(text_content)
                    except Exception:
                        logger.warning("Annotation rendering failed", exc_info=True)
                        text_content = response  # fall back to full original response
                        annotated_bytes = None

                msg_entry = {"role": "assistant", "display": text_content}
                if annotated_bytes:
                    msg_entry["annotated_image"] = annotated_bytes
                st.session_state.messages.append(msg_entry)
            except Exception as e:
                st.error(f"**API Error:** {e}")
