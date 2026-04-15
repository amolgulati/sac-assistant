# Inline Image Attach in Chat Input — Design Spec

## Overview

Replace the sidebar image-attachment flow with Streamlit's native file-accepting chat input. Users paste, drag-drop, or pick images directly in the chat input rather than routing through a sidebar paste button and thumbnail.

This is a localized UX change to `app.py` plus a `requirements.txt` bump. It is independent of Phase 3 of the v2 spec and can ship on its own.

## Motivation

Today, attaching a screenshot takes four interactions: click the sidebar paste button, confirm the thumbnail, return focus to the chat input, type and send. The sidebar context switch breaks chat flow. `st.chat_input(accept_file=True)` (Streamlit 1.43+) puts the paperclip, drag-drop target, and paste affordance inline with the text input — one pane, one flow.

## Behavior

- User attaches an image via paperclip icon, drag-drop onto the chat input, or (browser-permitting) Cmd+V paste into the input
- Image is attached to the user turn it was submitted with, matching the current single-image-per-turn model
- Streamlit clears the attached file automatically after submit
- Sidebar "Image Attachment" section is removed — no paste button, no file uploader, no thumbnail
- When the user submits only an image with no text, the user-visible message is auto-filled with `(image attached)` so the chat transcript reads sensibly

## Scope

### In scope

- Swap `st.chat_input` to `accept_file=True, file_type=["png", "jpg", "jpeg", "gif", "webp"]`
- Handle the new `ChatInputValue` return shape (`.text` + `.files`)
- Support empty-text + image submissions with `(image attached)` as the display text
- Delete the sidebar Image Attachment block and `st.session_state.image` state
- Remove `streamlit-paste-button` dependency and related imports (`streamlit_paste_button`, `io`)
- Bump `streamlit>=1.43.0` in `requirements.txt`

### Out of scope

- Multiple images per turn (single-image behavior preserved)
- Rendering past images inline in `st.chat_message` transcripts (unchanged from today)
- Any Phase 3 polish items (PDF/DOCX parsing, per-file toggles, export, code-block copy)
- Non-image file attachments

## Implementation Notes

### `app.py` changes

1. **Imports**
   - Remove `import io`
   - Remove `from streamlit_paste_button import paste_image_button`

2. **Session state** ([app.py:137–143](app.py:137))
   - Remove the `st.session_state.image` initialization
   - Remove the `st.session_state.image = None` reset inside the "New Conversation" button handler

3. **Sidebar** ([app.py:185–206](app.py:185))
   - Delete the entire "Image Attachment" block, including the `st.divider()` that precedes it

4. **Chat input + submit handler** ([app.py:218–245](app.py:218))
   - Replace the walrus-operator gate:
     ```python
     user_input = st.chat_input(
         "What do you need help with?",
         accept_file=True,
         file_type=["png", "jpg", "jpeg", "gif", "webp"],
     )
     if user_input:
         text = (user_input.text or "").strip()
         files = user_input.files or []
         image_file = files[0] if files else None
         display_text = text if text else "(image attached)"
         # ... build api_messages using display_text and image_file ...
     ```
   - The image-attach block (currently gated on `st.session_state.image`) now gates on `image_file is not None` and reads bytes via `image_file.getvalue()` and MIME via `image_file.type`
   - The `api_content` stored back onto `st.session_state.messages[-1]` is unchanged in shape — only the source of the image bytes changes
   - Submission is valid when `text` is non-empty OR `image_file` is not None. Add an explicit guard: if both are missing, skip submission (defensive — Streamlit's exact behavior here isn't documented)

### `requirements.txt` changes

- `streamlit>=1.31.0` → `streamlit>=1.43.0`
- Remove `streamlit-paste-button>=0.1.2`

## Edge Cases

| Case | Behavior |
|------|----------|
| Text + image | Multimodal content block with both; same as today |
| Text only | Text-only content; same as today |
| Image only, no text | `display_text` = `(image attached)`; multimodal content sent with `(image attached)` as the text block |
| Non-image file type | Blocked by `file_type` at the widget layer; no runtime path |
| Paste fails in browser | User falls back to paperclip picker or drag-drop; no worse than today |
| Large image | Unchanged from today; no new size handling introduced |

## Testing

Manual verification steps after implementation:

1. Drag-drop a PNG onto the chat input, send with no text → transcript shows `(image attached)`, assistant receives the image
2. Click paperclip, pick a JPG, type "what do you see?", send → transcript shows the text, assistant sees both
3. Cmd+V a screenshot into the chat input (Chrome / Safari / Firefox) — document which browsers work for future reference
4. Attach image on turn 1, ask follow-up text-only question on turn 2 → assistant retains image context from turn 1 (via stored `api_content`)
5. Click "New Conversation" → chat history clears; no residual image state

No automated tests — the app has no test suite today and this change is entirely UX-facing.

## Files Changed

| File | Action |
|------|--------|
| `app.py` | Modify — chat input signature, submit handler, remove sidebar image block, remove image session state |
| `requirements.txt` | Modify — bump `streamlit`, remove `streamlit-paste-button` |

## Rollback

Single-commit change touching two files. Revert the commit to restore the sidebar flow.

## Success Criteria

- User can paste a screenshot and send in one keystroke sequence (Cmd+V, type, Enter) without touching the sidebar, in at least one mainstream browser
- Drag-drop into the chat input attaches an image
- The sidebar no longer contains an image attachment section
- `streamlit-paste-button` is removed from dependencies
- Existing multi-turn behavior is preserved: image attached on turn N remains visible to the model on turn N+1
