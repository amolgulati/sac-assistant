# Smart Annotator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** When a user sends a screenshot, the AI returns an annotated copy of the image with numbered markers (circles, arrows, highlights) alongside step-by-step text instructions.

**Architecture:** The model's system prompt teaches it to emit a fenced `annotations` JSON block at the end of its response when it has spatial guidance to give. A response parser extracts this block from the streamed text. An annotator module (Pillow) draws the markers on the original image. The chat area renders the annotated image inline above the cleaned-up text.

**Tech Stack:** Python, Streamlit 1.43+, Pillow 10+, OpenAI SDK, pytest

**Spec:** `docs/superpowers/specs/2026-04-15-smart-annotator-design.md`

---

## File Structure

| File | Role |
|------|------|
| `annotator.py` | **Create.** Pure function `annotate(image_bytes, annotations) -> bytes`. Draws circles, arrows, highlights on an image using Pillow. ~80-100 lines. |
| `response_parser.py` | **Create.** Pure function `parse_response(text) -> (clean_text, annotations_list_or_none)`. Extracts the fenced `annotations` block from a model response. ~30 lines. |
| `app.py` | **Modify.** Replace `st.write_stream` with a manual streaming loop that hides the annotations block during streaming. After stream completes, render annotated image + clean text. ~40 lines changed. |
| `prompts/system.md` | **Modify.** Append annotation instructions (~30 lines). |
| `requirements.txt` | **Modify.** Add `Pillow>=10.0.0`. |
| `tests/test_response_parser.py` | **Create.** Tests for annotation extraction, edge cases. |
| `tests/test_annotator.py` | **Create.** Tests for image annotation drawing. |
| `README.md` | **Modify.** Document the annotated screenshot feature. |

---

### Task 1: Add Pillow Dependency and Test Infrastructure

**Files:**
- Modify: `requirements.txt`
- Create: `tests/__init__.py`

- [ ] **Step 1: Add Pillow to requirements.txt**

In `requirements.txt`, add the Pillow line at the end:

```
streamlit>=1.43.0
openai>=1.12.0
python-dotenv>=1.0.0
Pillow>=10.0.0
```

- [ ] **Step 2: Create tests directory**

Create `tests/__init__.py` as an empty file (makes `tests/` a Python package for pytest discovery).

- [ ] **Step 3: Install updated dependencies**

Run:
```bash
pip install -r requirements.txt
pip install pytest
```

Expected: All packages install successfully. Pillow version 10+ is installed.

- [ ] **Step 4: Verify pytest runs with no tests**

Run:
```bash
python -m pytest tests/ -v
```

Expected: `no tests ran` with exit code 5 (no tests collected). No import errors.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt tests/__init__.py
git commit -m "chore: add Pillow dependency and test infrastructure"
```

---

### Task 2: Response Parser — Tests

**Files:**
- Create: `tests/test_response_parser.py`

- [ ] **Step 1: Write tests for the response parser**

Create `tests/test_response_parser.py`:

```python
import json
import pytest
from response_parser import parse_response


class TestParseResponse:
    """Tests for extracting annotation blocks from model responses."""

    def test_response_with_annotations(self):
        """A response with a valid annotations block returns clean text + parsed annotations."""
        raw = (
            "Here are the steps:\n\n"
            "1. Click the button\n"
            "2. Enter the formula\n\n"
            '```annotations\n'
            '[{"type": "circle", "x": 100, "y": 200, "radius": 25, "label": "1", "color": "red"}]\n'
            '```'
        )
        text, annotations = parse_response(raw)
        assert text.strip() == "Here are the steps:\n\n1. Click the button\n2. Enter the formula"
        assert len(annotations) == 1
        assert annotations[0]["type"] == "circle"
        assert annotations[0]["x"] == 100

    def test_response_without_annotations(self):
        """A plain text response returns the text as-is and None for annotations."""
        raw = "Just a normal response with no annotations."
        text, annotations = parse_response(raw)
        assert text == raw
        assert annotations is None

    def test_empty_annotations_array(self):
        """An empty annotations array is treated as no annotations."""
        raw = "Some text\n\n```annotations\n[]\n```"
        text, annotations = parse_response(raw)
        assert "Some text" in text
        assert annotations is None

    def test_malformed_json_returns_none(self):
        """Malformed JSON in the annotations block is treated as no annotations."""
        raw = "Some text\n\n```annotations\n{not valid json\n```"
        text, annotations = parse_response(raw)
        assert "Some text" in text
        assert annotations is None

    def test_multiple_annotation_types(self):
        """A response with circle, arrow, and highlight annotations parses all three."""
        raw = (
            "Steps:\n\n"
            '```annotations\n'
            '[\n'
            '  {"type": "circle", "x": 50, "y": 60, "radius": 20, "label": "1", "color": "red"},\n'
            '  {"type": "arrow", "start": [50, 60], "end": [200, 100], "label": "2", "color": "red"},\n'
            '  {"type": "highlight", "x": 10, "y": 300, "w": 400, "h": 50, "label": "3", "color": "green"}\n'
            ']\n'
            '```'
        )
        text, annotations = parse_response(raw)
        assert text.strip() == "Steps:"
        assert len(annotations) == 3
        assert annotations[0]["type"] == "circle"
        assert annotations[1]["type"] == "arrow"
        assert annotations[2]["type"] == "highlight"

    def test_annotations_not_a_list_returns_none(self):
        """If the annotations block parses to a non-list JSON value, treat as no annotations."""
        raw = 'Some text\n\n```annotations\n{"type": "circle"}\n```'
        text, annotations = parse_response(raw)
        assert "Some text" in text
        assert annotations is None

    def test_text_after_annotations_is_preserved(self):
        """Any text after the annotations block is included in the clean text."""
        raw = (
            "Before\n\n"
            '```annotations\n'
            '[{"type": "circle", "x": 1, "y": 2, "radius": 10, "label": "1", "color": "red"}]\n'
            '```\n\n'
            "After"
        )
        text, annotations = parse_response(raw)
        assert "Before" in text
        assert "After" in text
        assert annotations is not None
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:
```bash
python -m pytest tests/test_response_parser.py -v
```

Expected: `ModuleNotFoundError: No module named 'response_parser'` — all tests fail because the module doesn't exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/test_response_parser.py
git commit -m "test: add response parser tests (red)"
```

---

### Task 3: Response Parser — Implementation

**Files:**
- Create: `response_parser.py`

- [ ] **Step 1: Implement the response parser**

Create `response_parser.py`:

```python
"""Extract an optional annotations JSON block from a model response."""

import json
import logging
import re

logger = logging.getLogger(__name__)

_ANNOTATIONS_PATTERN = re.compile(
    r"```annotations\s*\n(.*?)\n\s*```",
    re.DOTALL,
)


def parse_response(text: str) -> tuple[str, list[dict] | None]:
    """Split a model response into clean text and an optional annotations list.

    Returns
    -------
    (clean_text, annotations)
        *clean_text* has the fenced annotations block removed and surrounding
        whitespace tidied.  *annotations* is a list of annotation dicts, or
        ``None`` when no valid block is present.
    """
    match = _ANNOTATIONS_PATTERN.search(text)
    if not match:
        return text, None

    try:
        parsed = json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError):
        logger.warning("Malformed annotations JSON — ignoring block")
        return _strip_block(text, match), None

    if not isinstance(parsed, list) or len(parsed) == 0:
        return _strip_block(text, match), None

    return _strip_block(text, match), parsed


def _strip_block(text: str, match: re.Match) -> str:
    """Remove the matched annotations block and collapse extra blank lines."""
    cleaned = text[: match.start()] + text[match.end() :]
    # Collapse runs of 3+ newlines down to 2
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()
```

- [ ] **Step 2: Run the tests to verify they pass**

Run:
```bash
python -m pytest tests/test_response_parser.py -v
```

Expected: All 7 tests pass.

- [ ] **Step 3: Commit**

```bash
git add response_parser.py
git commit -m "feat: add response parser for annotation extraction"
```

---

### Task 4: Image Annotator — Tests

**Files:**
- Create: `tests/test_annotator.py`

- [ ] **Step 1: Write tests for the image annotator**

Create `tests/test_annotator.py`:

```python
import io
import pytest
from PIL import Image
from annotator import annotate


def _make_test_image(width=800, height=600) -> bytes:
    """Create a blank white PNG image as bytes."""
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class TestAnnotate:
    """Tests for drawing annotations on an image."""

    def test_returns_valid_png(self):
        """annotate() returns bytes that decode to a valid PNG image."""
        img_bytes = _make_test_image()
        annotations = [
            {"type": "circle", "x": 100, "y": 100, "radius": 25, "label": "1", "color": "red"},
        ]
        result = annotate(img_bytes, annotations)
        img = Image.open(io.BytesIO(result))
        assert img.format == "PNG"
        assert img.size == (800, 600)

    def test_preserves_image_dimensions(self):
        """Output image has the same dimensions as the input."""
        img_bytes = _make_test_image(1920, 1080)
        annotations = [
            {"type": "highlight", "x": 10, "y": 10, "w": 200, "h": 50, "label": "1", "color": "green"},
        ]
        result = annotate(img_bytes, annotations)
        img = Image.open(io.BytesIO(result))
        assert img.size == (1920, 1080)

    def test_circle_annotation(self):
        """A circle annotation produces output that differs from the original."""
        img_bytes = _make_test_image()
        annotations = [
            {"type": "circle", "x": 400, "y": 300, "radius": 30, "label": "1", "color": "red"},
        ]
        result = annotate(img_bytes, annotations)
        assert result != img_bytes  # image was modified

    def test_arrow_annotation(self):
        """An arrow annotation produces output that differs from the original."""
        img_bytes = _make_test_image()
        annotations = [
            {"type": "arrow", "start": [100, 100], "end": [400, 300], "label": "1", "color": "red"},
        ]
        result = annotate(img_bytes, annotations)
        assert result != img_bytes

    def test_highlight_annotation(self):
        """A highlight annotation produces output that differs from the original."""
        img_bytes = _make_test_image()
        annotations = [
            {"type": "highlight", "x": 50, "y": 50, "w": 300, "h": 100, "label": "1", "color": "green"},
        ]
        result = annotate(img_bytes, annotations)
        assert result != img_bytes

    def test_multiple_annotations(self):
        """Multiple annotations of different types all get drawn."""
        img_bytes = _make_test_image()
        annotations = [
            {"type": "circle", "x": 100, "y": 100, "radius": 20, "label": "1", "color": "red"},
            {"type": "arrow", "start": [100, 120], "end": [300, 50], "label": "2", "color": "red"},
            {"type": "highlight", "x": 50, "y": 200, "w": 400, "h": 80, "label": "3", "color": "green"},
        ]
        result = annotate(img_bytes, annotations)
        assert result != img_bytes

    def test_coordinates_clamped_to_image_bounds(self):
        """Coordinates outside image bounds don't crash — they get clamped."""
        img_bytes = _make_test_image(200, 200)
        annotations = [
            {"type": "circle", "x": 5000, "y": 5000, "radius": 25, "label": "1", "color": "red"},
        ]
        # Should not raise
        result = annotate(img_bytes, annotations)
        img = Image.open(io.BytesIO(result))
        assert img.size == (200, 200)

    def test_unknown_annotation_type_is_skipped(self):
        """An unrecognized annotation type is silently skipped."""
        img_bytes = _make_test_image()
        annotations = [
            {"type": "polygon", "points": [[0, 0], [100, 100]], "label": "1", "color": "red"},
        ]
        # Should not raise
        result = annotate(img_bytes, annotations)
        img = Image.open(io.BytesIO(result))
        assert img.size == (800, 600)

    def test_empty_annotations_returns_unchanged(self):
        """An empty annotations list returns the original image bytes."""
        img_bytes = _make_test_image()
        result = annotate(img_bytes, [])
        assert result == img_bytes
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:
```bash
python -m pytest tests/test_annotator.py -v
```

Expected: `ModuleNotFoundError: No module named 'annotator'` — all tests fail.

- [ ] **Step 3: Commit**

```bash
git add tests/test_annotator.py
git commit -m "test: add image annotator tests (red)"
```

---

### Task 5: Image Annotator — Implementation

**Files:**
- Create: `annotator.py`

- [ ] **Step 1: Implement the image annotator**

Create `annotator.py`:

```python
"""Draw annotation markers on a screenshot image."""

from __future__ import annotations

import io
import logging
import math

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

# ── Colour palette ──────────────────────────────────────────────────
_COLORS = {
    "red": (220, 50, 50),
    "green": (40, 180, 70),
    "blue": (50, 100, 220),
}
_DEFAULT_COLOR = (220, 50, 50)  # red

_STROKE_WIDTH = 3
_LABEL_FONT_SIZE = 16
_HIGHLIGHT_OPACITY = 50  # 0-255


def annotate(image_bytes: bytes, annotations: list[dict]) -> bytes:
    """Return a new PNG with *annotations* drawn on top of *image_bytes*.

    If *annotations* is empty the original bytes are returned unchanged.
    Unknown annotation types are silently skipped.  Coordinates that exceed
    image bounds are clamped to the edges.
    """
    if not annotations:
        return image_bytes

    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    label_draw = ImageDraw.Draw(overlay)

    font = _get_font()

    for ann in annotations:
        ann_type = ann.get("type")
        color = _COLORS.get(ann.get("color", ""), _DEFAULT_COLOR)
        label = str(ann.get("label", ""))

        if ann_type == "circle":
            _draw_circle(draw, label_draw, img.size, ann, color, label, font)
        elif ann_type == "arrow":
            _draw_arrow(draw, label_draw, img.size, ann, color, label, font)
        elif ann_type == "highlight":
            _draw_highlight(draw, label_draw, img.size, ann, color, label, font)
        else:
            logger.debug("Skipping unknown annotation type: %s", ann_type)

    composite = Image.alpha_composite(img, overlay)
    # Convert back to RGB for PNG output (no alpha channel needed)
    composite = composite.convert("RGB")

    buf = io.BytesIO()
    composite.save(buf, format="PNG")
    return buf.getvalue()


# ── Drawing helpers ─────────────────────────────────────────────────


def _clamp(val: int | float, lo: int, hi: int) -> int:
    return max(lo, min(int(val), hi))


def _resolve_color_alpha(rgb: tuple[int, int, int], alpha: int = 255):
    return (*rgb, alpha)


def _get_font() -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Try to load a readable font; fall back to Pillow's built-in default."""
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", _LABEL_FONT_SIZE)
    except OSError:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", _LABEL_FONT_SIZE)
        except OSError:
            return ImageFont.load_default()


def _draw_label_badge(
    draw: ImageDraw.Draw,
    cx: int,
    cy: int,
    label: str,
    color: tuple[int, int, int],
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
):
    """Draw a small coloured circle with a white text label centred at (cx, cy)."""
    if not label:
        return
    badge_r = 12
    draw.ellipse(
        [cx - badge_r, cy - badge_r, cx + badge_r, cy + badge_r],
        fill=_resolve_color_alpha(color),
    )
    bbox = font.getbbox(label)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 1), label, fill=(255, 255, 255, 255), font=font)


def _draw_circle(
    draw: ImageDraw.Draw,
    label_draw: ImageDraw.Draw,
    img_size: tuple[int, int],
    ann: dict,
    color: tuple[int, int, int],
    label: str,
    font,
):
    w, h = img_size
    cx = _clamp(ann.get("x", 0), 0, w - 1)
    cy = _clamp(ann.get("y", 0), 0, h - 1)
    r = max(int(ann.get("radius", 25)), 5)

    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        outline=_resolve_color_alpha(color),
        width=_STROKE_WIDTH,
    )
    _draw_label_badge(label_draw, cx, cy - r - 16, label, color, font)


def _draw_arrow(
    draw: ImageDraw.Draw,
    label_draw: ImageDraw.Draw,
    img_size: tuple[int, int],
    ann: dict,
    color: tuple[int, int, int],
    label: str,
    font,
):
    w, h = img_size
    start = ann.get("start", [0, 0])
    end = ann.get("end", [0, 0])
    x1 = _clamp(start[0], 0, w - 1)
    y1 = _clamp(start[1], 0, h - 1)
    x2 = _clamp(end[0], 0, w - 1)
    y2 = _clamp(end[1], 0, h - 1)

    rgba = _resolve_color_alpha(color)
    draw.line([(x1, y1), (x2, y2)], fill=rgba, width=_STROKE_WIDTH)

    # Arrowhead
    angle = math.atan2(y2 - y1, x2 - x1)
    head_len = 14
    for offset in [2.5, -2.5]:  # two sides of the arrowhead
        ax = x2 - head_len * math.cos(angle + offset)
        ay = y2 - head_len * math.sin(angle + offset)
        draw.line([(x2, y2), (int(ax), int(ay))], fill=rgba, width=_STROKE_WIDTH)

    # Label at midpoint
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    _draw_label_badge(label_draw, mx, my - 16, label, color, font)


def _draw_highlight(
    draw: ImageDraw.Draw,
    label_draw: ImageDraw.Draw,
    img_size: tuple[int, int],
    ann: dict,
    color: tuple[int, int, int],
    label: str,
    font,
):
    iw, ih = img_size
    x = _clamp(ann.get("x", 0), 0, iw - 1)
    y = _clamp(ann.get("y", 0), 0, ih - 1)
    w = max(int(ann.get("w", 100)), 1)
    h = max(int(ann.get("h", 30)), 1)
    x2 = min(x + w, iw - 1)
    y2 = min(y + h, ih - 1)

    # Semi-transparent fill
    draw.rectangle([x, y, x2, y2], fill=_resolve_color_alpha(color, _HIGHLIGHT_OPACITY))
    # Solid border
    draw.rectangle([x, y, x2, y2], outline=_resolve_color_alpha(color), width=_STROKE_WIDTH)

    _draw_label_badge(label_draw, x + 14, y - 16, label, color, font)
```

- [ ] **Step 2: Run the tests to verify they pass**

Run:
```bash
python -m pytest tests/test_annotator.py -v
```

Expected: All 9 tests pass.

- [ ] **Step 3: Commit**

```bash
git add annotator.py
git commit -m "feat: add image annotator with circle, arrow, and highlight support"
```

---

### Task 6: System Prompt Update

**Files:**
- Modify: `prompts/system.md` (append after line 72)

- [ ] **Step 1: Append annotation instructions to the system prompt**

Add the following to the end of `prompts/system.md`, after the existing "Response Guidelines" section:

```markdown

## Screenshot Annotations

When the user attaches a screenshot AND your guidance involves specific UI locations (buttons, fields, cells, menus, errors), include a fenced `annotations` block at the end of your response.

### Format

Write your text response with numbered steps as usual. Then append an annotations block:

    ```annotations
    [
      {"type": "circle", "x": 342, "y": 118, "radius": 25, "label": "1", "color": "red"},
      {"type": "arrow", "start": [342, 140], "end": [500, 60], "label": "2", "color": "red"},
      {"type": "highlight", "x": 200, "y": 300, "w": 400, "h": 50, "label": "3", "color": "green"}
    ]
    ```

### Annotation types

- **circle**: x, y, radius, label, color — for "click this button" or "look at this icon"
- **arrow**: start [x,y], end [x,y], label, color — for "drag from here to there" or "this leads to that"
- **highlight**: x, y, w, h, label, color — for "this cell range" or "this error message area"

### Rules

- Only emit annotations when the user attached a screenshot AND you are pointing at specific UI elements.
- Coordinates are in pixels relative to the image dimensions. Estimate positions based on what you see.
- Number annotations to match the numbered steps in your text (label "1" goes with step 1).
- Keep annotations sparse: 2-5 markers per response. Do not clutter.
- Colors: red for actions (click, type), green for reference areas, blue for informational.
- If you cannot identify specific UI locations confidently, skip the annotations block entirely and respond with text only.
- Do NOT emit annotations for questions that don't include a screenshot.
```

- [ ] **Step 2: Verify the prompt file is well-formed**

Run:
```bash
wc -l prompts/system.md
```

Expected: ~102 lines (72 original + ~30 new). No syntax errors in the markdown.

- [ ] **Step 3: Commit**

```bash
git add prompts/system.md
git commit -m "feat: add screenshot annotation instructions to system prompt"
```

---

### Task 7: Integrate into app.py

**Files:**
- Modify: `app.py:1-248`

This is the core integration. We modify the streaming loop to hide the annotations block during display, then render the annotated image after streaming completes.

- [ ] **Step 1: Add imports at the top of app.py**

At line 1 of `app.py`, add the new imports. The import section becomes:

```python
import base64
import io
import os
import time
from urllib.parse import urlsplit

import requests
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from annotator import annotate
from response_parser import parse_response
```

- [ ] **Step 2: Replace the streaming and display block**

Replace the current streaming block at lines 235-248 of `app.py`:

```python
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

With:

```python
        # Stream the response
        with st.chat_message("assistant"):
            try:
                client = build_client(REQUIRED_VARS["BASE_URL"], REQUIRED_VARS["API_KEY"])
                stream = client.chat.completions.create(
                    model=MODEL,
                    messages=api_messages,
                    stream=True,
                )

                # Manual streaming: buffer full response, display text portion live
                text_placeholder = st.empty()
                full_response = ""
                for chunk in stream:
                    delta = getattr(chunk.choices[0].delta, "content", None) or ""
                    full_response += delta
                    # Hide the annotations block from the live stream display
                    live_display = full_response.split("```annotations")[0].rstrip()
                    text_placeholder.markdown(live_display + "▍")
                text_placeholder.empty()

                # Parse annotations and render final output
                clean_text, annotations = parse_response(full_response)

                annotated_img_bytes = None
                if annotations and image_file is not None:
                    try:
                        annotated_img_bytes = annotate(img_bytes, annotations)
                        st.image(annotated_img_bytes, caption="Annotated screenshot", use_container_width=True)
                    except Exception:
                        pass  # Fall through to text-only display

                st.markdown(clean_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "display": clean_text,
                    "annotated_image": annotated_img_bytes,
                })
            except Exception as e:
                st.error(f"**API Error:** {e}")
```

- [ ] **Step 3: Update chat history rendering to show annotated images**

Replace the history rendering block at lines 184-187:

```python
# Render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["display"])
```

With:

```python
# Render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("annotated_image"):
            st.image(msg["annotated_image"], caption="Annotated screenshot", use_container_width=True)
        st.markdown(msg["display"])
```

- [ ] **Step 4: Verify the streaming block is correct**

Review the code from Step 2. The annotation/rendering section should use a pre-initialized variable to handle the case where `annotate()` raises. Confirm the block looks exactly like this (this is the canonical version — if Step 2 differs, use this):

```python
                # Parse annotations and render final output
                clean_text, annotations = parse_response(full_response)

                annotated_img_bytes = None
                if annotations and image_file is not None:
                    try:
                        annotated_img_bytes = annotate(img_bytes, annotations)
                        st.image(annotated_img_bytes, caption="Annotated screenshot", use_container_width=True)
                    except Exception:
                        pass  # Fall through to text-only display

                st.markdown(clean_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "display": clean_text,
                    "annotated_image": annotated_img_bytes,
                })
```

- [ ] **Step 5: Run the app locally to sanity-check it starts**

Run:
```bash
streamlit run app.py &
sleep 3
kill %1
```

Expected: App starts without import errors or crashes. (Don't try to send a message — just verify it boots.)

- [ ] **Step 6: Run all tests**

Run:
```bash
python -m pytest tests/ -v
```

Expected: All 16 tests pass (7 parser + 9 annotator).

- [ ] **Step 7: Commit**

```bash
git add app.py
git commit -m "feat: integrate annotation parser and annotated image rendering into chat"
```

---

### Task 8: Update README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update the Features section**

In `README.md`, update the screenshot support bullet in the Features list. Replace:

```markdown
- **Screenshot support** — attach images inline in the chat input (paste, drag-drop, or paperclip picker); the assistant can analyze SAC models, Datasphere views, and error messages
```

With:

```markdown
- **Screenshot support with visual annotations** — attach images inline in the chat input (paste, drag-drop, or paperclip picker); the assistant analyzes SAC models, Datasphere views, and error messages, and returns annotated screenshots with numbered markers (circles, arrows, highlights) pointing at exactly where to click and what to change
```

- [ ] **Step 2: Update the Project Structure section**

In the project structure diagram, add the new files. Replace:

```text
sac-assistant/
  app.py                 # Streamlit chat application
  app.yaml               # Databricks App entrypoint/config
  docs/                  # Design specs and implementation notes
  projects/              # Optional project context folders
  prompts/
    system.md            # SAC/Datasphere system prompt (editable)
  requirements.txt       # Python dependencies
  .env.example           # Configuration template
  .env                   # Your configuration (not committed)
```

With:

```text
sac-assistant/
  app.py                 # Streamlit chat application
  annotator.py           # Draws annotation markers on screenshot images
  response_parser.py     # Extracts annotation JSON from model responses
  app.yaml               # Databricks App entrypoint/config
  docs/                  # Design specs and implementation notes
  projects/              # Optional project context folders
  prompts/
    system.md            # SAC/Datasphere system prompt (editable)
  tests/                 # pytest tests for annotator and parser
  requirements.txt       # Python dependencies
  .env.example           # Configuration template
  .env                   # Your configuration (not committed)
```

- [ ] **Step 3: Update the dependencies note**

In the Corporate Deployment section, replace:

```markdown
- **Minimal dependencies** — three well-known packages
```

With:

```markdown
- **Minimal dependencies** — four well-known packages (Streamlit, OpenAI SDK, python-dotenv, Pillow)
```

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: update README with annotated screenshot feature"
```

---

### Task 9: Final Verification

- [ ] **Step 1: Run the full test suite**

Run:
```bash
python -m pytest tests/ -v
```

Expected: All 16 tests pass.

- [ ] **Step 2: Verify the app starts cleanly**

Run:
```bash
streamlit run app.py &
sleep 3
kill %1
```

Expected: No errors on startup.

- [ ] **Step 3: Review all changed files**

Run:
```bash
git log --oneline -8
```

Expected output (8 commits from this plan):
```
<hash> docs: update README with annotated screenshot feature
<hash> feat: integrate annotation parser and annotated image rendering into chat
<hash> feat: add screenshot annotation instructions to system prompt
<hash> feat: add image annotator with circle, arrow, and highlight support
<hash> test: add image annotator tests (red)
<hash> feat: add response parser for annotation extraction
<hash> test: add response parser tests (red)
<hash> chore: add Pillow dependency and test infrastructure
```
