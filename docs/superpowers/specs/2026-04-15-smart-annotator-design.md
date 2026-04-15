# Smart Annotator — Annotated Screenshot Responses

**Date:** 2026-04-15
**Status:** Approved

## Problem

The SAC Assistant today is a text-in/text-out chat. When a user sends a screenshot of their SAP Analytics Cloud model, the AI describes what to do in prose, but never shows *where* to click or *which* element to change. This forces the user to mentally map text instructions back to a complex UI — slow, error-prone, and cumbersome.

The inspiration is [Clicky](https://github.com/farzaa/clicky), a native macOS assistant that can see your screen and point at UI elements. We want a similar "tutor pointing at your screen" experience, but constrained to a Databricks-hosted Streamlit web app with a locked-down corporate browser (no extensions, no OS automation).

## Solution

When the user sends a screenshot, the AI returns an **annotated copy of the image** with numbered markers (circles, arrows, highlights) drawn on it, alongside corresponding numbered step-by-step text instructions.

### Example Interaction

> **User:** *[pastes screenshot of SAC planning model]* "How do I add a YTD calculation here?"
>
> **AI response:**
> - **Annotated image** inline: original screenshot with a red circle (1) on the "Add Column" button, an arrow (2) pointing to the formula bar, a green highlight (3) on the target cell range
> - **Numbered steps:**
>   1. Click **Add Column** (circled in red) to insert a new calculated column
>   2. In the formula bar, enter: `RESULTLOOKUP([d/SAP_FIN_YTD], ...)`
>   3. The formula will populate the highlighted range

## Architecture

### Current Flow

```
User → paste screenshot → Streamlit chat → API (vision model) → text response → display
```

### New Flow

```
User → paste screenshot → Streamlit chat → API (vision model) → structured response
  → parse annotations JSON + text → Pillow draws on image → display annotated image + steps
```

### Components

Three additions to the existing codebase:

1. **System prompt update** (`prompts/system.md`) — Instructs the model to return spatial annotations in a structured JSON block when it has a screenshot to reference and spatial guidance to give. Normal text questions get normal text answers.

2. **Response parser** (in `app.py`, ~30-40 new lines) — Extracts the annotation JSON block from the model's response. Everything outside the block flows through as normal markdown.

3. **Image annotator** (`annotator.py`, ~80-100 lines) — Pure function: `annotate(image_bytes, annotations_json) -> image_bytes`. Uses Pillow to draw markers on the original image.

### File Changes

| File | Change |
|------|--------|
| `prompts/system.md` | Append annotation instructions |
| `app.py` | Add response parsing + annotated image rendering (~30-40 lines) |
| `annotator.py` | New file — annotation drawing logic (~80-100 lines) |
| `requirements.txt` | Re-add `Pillow` |
| `README.md` | Document the feature |

### What Stays the Same

- Screenshot input flow (paste/drag/pick via `st.chat_input`)
- Streaming text display
- Project context system
- Databricks OAuth / deployment
- Conversation history

## Annotation Format

The model wraps annotation data in a fenced block at the end of its response:

````
Here's how to add the YTD calculation:

1. Click the **Add Column** button in the toolbar
2. Enter the formula in the formula bar
3. The result populates across the highlighted range

```annotations
[
  {"type": "circle", "x": 342, "y": 118, "radius": 25, "label": "1", "color": "red"},
  {"type": "arrow", "start": [342, 140], "end": [500, 60], "label": "2", "color": "red"},
  {"type": "highlight", "x": 200, "y": 300, "w": 400, "h": 50, "label": "3", "color": "green"}
]
```
````

### Why This Format

- Simple to parse — find the fenced block, extract JSON
- Doesn't interfere with normal markdown rendering
- Model can omit the block entirely for non-screenshot questions
- Works with streaming — buffer the annotations block, render the image after the full response arrives

### Annotation Types

| Type | Fields | Use Case |
|------|--------|----------|
| `circle` | x, y, radius, label, color | "Click this button" |
| `arrow` | start, end, label, color | "Drag here" or "Look at this" |
| `highlight` | x, y, w, h, label, color | "This region / cell range / error" |

Three types is enough. These cover "click here", "look here", and "this area".

### Prompt Instructions

The system prompt addition instructs the model to:

- Only emit annotations when the user attached a screenshot AND the guidance involves specific UI locations
- Use coordinates relative to image pixel dimensions
- Number annotations to match numbered steps in the text
- Keep annotations sparse: 2-5 markers per response
- Default colors: red for actions (click/type), green for reference areas, blue for informational

### Accuracy Expectations

Vision models are approximate at coordinate estimation (20-30px off). This is acceptable — the goal is "look in this area" not "click at this exact pixel." Numbered labels + text descriptions provide precision; visual markers provide spatial orientation.

## Rendering & Display

### Flow After Streaming Completes

During streaming, the full response is accumulated into a buffer (text still streams to the UI token-by-token as today). Once streaming finishes:

1. Parser splits the complete response into `text_content` (markdown) and `annotations_json` (optional)
2. If annotations exist and the current message had an image attached:
   - `annotate(original_image_bytes, annotations_json)` produces a new PNG
   - The streamed text is replaced with: annotated image first, then numbered steps as markdown below
3. If no annotations: the streamed text stays as-is (today's behavior)

### Drawing Details (`annotator.py`)

- **Circles:** 3px outlined stroke, numbered label centered inside on a colored badge
- **Arrows:** Line with arrowhead, label at midpoint
- **Highlights:** Semi-transparent fill (20% opacity) with solid border, label top-left
- **Font:** Pillow's built-in default or DejaVu Sans (ships with most Linux/container environments including Databricks)
- **Scaling:** Annotations drawn at native image resolution, no resizing

### Streamlit Rendering

```python
if annotations and user_image_bytes:
    annotated = annotate(user_image_bytes, annotations)
    st.image(annotated, caption="Annotated screenshot", use_container_width=True)

st.markdown(text_content)
```

### Chat History

- Annotated image bytes stored in `st.session_state.messages` for conversation persistence
- The **original** (unannotated) image is sent to the API on future turns — prevents the model from seeing its own annotations and getting confused

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Malformed annotation JSON | Log warning, display text-only response |
| Coordinates outside image bounds | Clamp to image edges |
| Annotations returned but no user image | Ignore annotations, text-only |
| Pillow drawing failure | Catch exception, text-only, log error |
| Empty annotations array `[]` | Text-only response |

**Principle:** Annotations are always additive, never blocking. If anything goes wrong with the visual layer, the user gets the same text response they'd get today. The tool never degrades below its current baseline.

## Scope

### In Scope

- Annotated image responses (circle, arrow, highlight)
- Updated system prompt with annotation instructions
- `annotator.py` module
- Response parser in `app.py`
- Pillow dependency
- Updated README

### Out of Scope

- Voice / TTS
- Auto-screenshot / clipboard watching
- Browser extensions or overlays
- Interactive overlays (clickable hotspots, step-through walkthrough)
- Annotation editing by the user
- Caching or persisting annotated images to disk

## Dependencies

`requirements.txt` goes from 3 packages to 4:

```
streamlit>=1.43.0
openai>=1.12.0
python-dotenv>=1.0.0
Pillow>=10.0.0
```

No new system-level dependencies.
