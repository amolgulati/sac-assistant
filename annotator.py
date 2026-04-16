"""annotator.py — Draw spatial markers on a screenshot image.

Public API:
    annotate(image_bytes: bytes, annotations: list[dict]) -> bytes
        Returns a PNG of the image with circles, arrows, and highlights drawn on it.
        Falls back to the original image bytes on any error.

Annotation dict schemas:
    circle:    {"type": "circle",    "x": int, "y": int, "radius": int, "label": str, "color": str}
    arrow:     {"type": "arrow",     "start": [x,y], "end": [x,y], "label": str, "color": str}
    highlight: {"type": "highlight", "x": int, "y": int, "w": int, "h": int, "label": str, "color": str}

Colors: "red" (default), "green", "blue", "yellow", "orange"
"""

import io
import logging
import math

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

_COLOR_MAP = {
    "red":    (220,  50,  50),
    "green":  ( 50, 180,  50),
    "blue":   ( 50, 100, 220),
    "yellow": (220, 180,   0),
    "orange": (220, 120,   0),
}
_DEFAULT_COLOR = _COLOR_MAP["red"]


def _clamp(val: float, lo: float, hi: float) -> int:
    return int(max(lo, min(hi, val)))


def _rgb(color_str: str) -> tuple:
    return _COLOR_MAP.get((color_str or "").lower(), _DEFAULT_COLOR)


def _get_font(size: int = 13) -> ImageFont.ImageFont:
    for name in ("DejaVuSans-Bold.ttf", "arial.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except (IOError, OSError):
            pass
    return ImageFont.load_default()


def _draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, rgb: tuple) -> None:
    """Draw a small filled badge with white text centred at (x, y)."""
    if not label:
        return
    font = _get_font(13)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 4
    rx0, ry0 = x - tw // 2 - pad, y - th // 2 - pad
    rx1, ry1 = x + tw // 2 + pad, y + th // 2 + pad
    draw.rectangle([rx0, ry0, rx1, ry1], fill=rgb)
    draw.text((rx0 + pad, ry0 + pad), label, fill=(255, 255, 255), font=font)


def _draw_circle(draw: ImageDraw.ImageDraw, img_size: tuple, ann: dict) -> None:
    w, h = img_size
    x = _clamp(ann.get("x", 0), 0, w)
    y = _clamp(ann.get("y", 0), 0, h)
    r = max(10, min(ann.get("radius", 25), min(w, h) // 4))
    rgb = _rgb(ann.get("color", "red"))
    bbox = [x - r, y - r, x + r, y + r]
    draw.ellipse(bbox, outline=rgb, width=3)
    _draw_badge(draw, x, y - r - 14, str(ann.get("label", "")), rgb)


def _draw_arrow(draw: ImageDraw.ImageDraw, img_size: tuple, ann: dict) -> None:
    w, h = img_size
    start = ann.get("start", [0, 0])
    end = ann.get("end", [0, 0])
    x0, y0 = _clamp(start[0], 0, w), _clamp(start[1], 0, h)
    x1, y1 = _clamp(end[0], 0, w), _clamp(end[1], 0, h)
    rgb = _rgb(ann.get("color", "red"))

    draw.line([(x0, y0), (x1, y1)], fill=rgb, width=3)

    # Arrowhead at (x1, y1)
    angle = math.atan2(y1 - y0, x1 - x0)
    head = 16
    for a in (2.5, -2.5):
        ax = x1 - head * math.cos(angle + a)
        ay = y1 - head * math.sin(angle + a)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=rgb, width=3)

    _draw_badge(draw, (x0 + x1) // 2, (y0 + y1) // 2 - 14,
                str(ann.get("label", "")), rgb)


def _apply_highlight(img: Image.Image, ann: dict) -> None:
    """Semi-transparent rectangle composited directly onto *img* (RGBA mode required)."""
    w, h = img.size
    x  = _clamp(ann.get("x", 0), 0, w)
    y  = _clamp(ann.get("y", 0), 0, h)
    x2 = _clamp(x + ann.get("w", 100), 0, w)
    y2 = _clamp(y + ann.get("h", 40),  0, h)
    rgb = _rgb(ann.get("color", "green"))

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay)
    ov.rectangle([x, y, x2, y2], fill=rgb + (50,), outline=rgb + (220,), width=2)
    img.alpha_composite(overlay)

    # Label badge on top of the freshly composited image
    draw = ImageDraw.Draw(img)
    _draw_badge(draw, x + 16, y + 10, str(ann.get("label", "")), rgb)


def annotate(image_bytes: bytes, annotations: list) -> bytes:
    """Return PNG bytes of *image_bytes* with *annotations* drawn on it.

    Always returns valid image bytes — falls back to the original on any error.
    """
    if not annotations:
        return image_bytes

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

        # First pass: highlights (need alpha_composite, mutate img)
        for ann in annotations:
            if ann.get("type") == "highlight":
                try:
                    _apply_highlight(img, ann)
                except Exception:
                    logger.warning("Failed to draw highlight: %s", ann, exc_info=True)

        # Second pass: circles and arrows on top
        draw = ImageDraw.Draw(img)
        for ann in annotations:
            ann_type = ann.get("type", "")
            try:
                if ann_type == "circle":
                    _draw_circle(draw, img.size, ann)
                elif ann_type == "arrow":
                    _draw_arrow(draw, img.size, ann)
                elif ann_type != "highlight":
                    logger.warning("Unknown annotation type: %s", ann_type)
            except Exception:
                logger.warning("Failed to draw annotation: %s", ann, exc_info=True)

        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="PNG")
        return buf.getvalue()

    except Exception:
        logger.error("annotate() failed, returning original image", exc_info=True)
        return image_bytes
