"""Shared PDF drawing: fonts, wordmark, footer QR, page helpers."""

from __future__ import annotations

import io
from pathlib import Path

import qrcode
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .config import (
    A4,
    A4_MARGIN,
    BERRY,
    CARD_BORDER,
    CHARACTER_FILES,
    CHARACTERS_DIR,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_HEADING,
    INK,
    LETTER,
    LETTER_MARGIN,
    PAPER,
    RAINBOW,
)

_FONTS_READY = False


def ensure_fonts():
    global _FONTS_READY
    if _FONTS_READY:
        return
    pdfmetrics.registerFont(TTFont("Baloo2", FONT_HEADING))
    pdfmetrics.registerFont(TTFont("Atkinson", FONT_BODY))
    pdfmetrics.registerFont(TTFont("Atkinson-Bold", FONT_BODY_BOLD))
    _FONTS_READY = True


def page_setup(size_name: str):
    if size_name == "a4":
        return A4, A4_MARGIN
    return LETTER, LETTER_MARGIN


def make_canvas(path: Path, size_name: str) -> tuple[canvas.Canvas, float, float, float]:
    ensure_fonts()
    pagesize, margin = page_setup(size_name)
    c = canvas.Canvas(str(path), pagesize=pagesize)
    return c, pagesize[0], pagesize[1], margin


def fill_paper(c: canvas.Canvas, width: float, height: float):
    c.setFillColor(HexColor(PAPER))
    c.rect(0, 0, width, height, fill=1, stroke=0)


def draw_wordmark(c: canvas.Canvas, width: float, height: float, margin: float, y: float | None = None):
    """Rainbow LEARN WITH IAN wordmark near the top."""
    ensure_fonts()
    text = "LEARN WITH IAN"
    font_size = 18
    c.setFont("Baloo2", font_size)
    total = pdfmetrics.stringWidth(text, "Baloo2", font_size)
    x = (width - total) / 2
    if y is None:
        y = height - margin - 8
    for i, ch in enumerate(text):
        c.setFillColor(HexColor(RAINBOW[i % len(RAINBOW)]))
        c.drawString(x, y, ch)
        x += pdfmetrics.stringWidth(ch, "Baloo2", font_size)
    return y - 8


def make_qr_image(url: str, box_size: int = 10) -> bytes:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2, box_size=box_size)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=INK, back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def draw_footer(
    c: canvas.Canvas,
    width: float,
    height: float,
    margin: float,
    youtube_url: str,
    qr_cache: dict | None = None,
):
    """Footer: brand left, Scan + QR right. QR at least 0.8 inch."""
    ensure_fonts()
    qr_size = 0.85 * inch
    y_base = margin * 0.35
    c.setFillColor(HexColor(INK))
    c.setFont("Atkinson", 9)
    c.drawString(margin, y_base + qr_size * 0.35, "Learn with Ian · learnwithian.com")

    label = "Scan to watch the episode"
    c.setFont("Atkinson", 8)
    label_w = pdfmetrics.stringWidth(label, "Atkinson", 8)
    qr_x = width - margin - qr_size
    c.drawRightString(qr_x - 6, y_base + qr_size * 0.55, label)

    if qr_cache is not None and youtube_url in qr_cache:
        qr_bytes = qr_cache[youtube_url]
    else:
        qr_bytes = make_qr_image(youtube_url)
        if qr_cache is not None:
            qr_cache[youtube_url] = qr_bytes
    qr_reader = ImageReader(io.BytesIO(qr_bytes))
    c.drawImage(qr_reader, qr_x, y_base, qr_size, qr_size, mask="auto")
    return y_base + qr_size + 6  # content should stay above this


def image_reader_from_png_bytes(data: bytes) -> ImageReader:
    return ImageReader(io.BytesIO(data))


def draw_episode_line(c: canvas.Canvas, width: float, y: float, title: str):
    ensure_fonts()
    c.setFillColor(HexColor(INK))
    c.setFont("Atkinson", 11)
    line = f"Goes with the episode: {title}"
    c.drawCentredString(width / 2, y, line)
    return y - 16


def draw_title(c: canvas.Canvas, width: float, y: float, title: str, size: int = 22):
    ensure_fonts()
    c.setFillColor(HexColor(INK))
    c.setFont("Baloo2", size)
    c.drawCentredString(width / 2, y, title)
    return y - size - 6


def draw_cut_line(c: canvas.Canvas, x1, y1, x2, y2):
    c.setStrokeColor(HexColor(CARD_BORDER))
    c.setDash(3, 3)
    c.setLineWidth(0.7)
    c.line(x1, y1, x2, y2)
    c.setDash()


def character_path(name: str) -> Path | None:
    fname = CHARACTER_FILES.get(name)
    if not fname:
        return None
    p = CHARACTERS_DIR / fname
    return p if p.exists() else None


def draw_character_proportional(
    c: canvas.Canvas,
    name: str,
    x: float,
    y: float,
    max_w: float,
    max_h: float,
    placements: list | None = None,
):
    """Draw character preserving aspect ratio (no stretching)."""
    from PIL import Image

    path = character_path(name)
    if not path:
        return
    im = Image.open(path)
    iw, ih = im.size
    scale = min(max_w / iw, max_h / ih)
    w, h = iw * scale, ih * scale
    dx = x + (max_w - w) / 2
    dy = y + (max_h - h) / 2
    c.drawImage(str(path), dx, dy, width=w, height=h, mask="auto")
    if placements is not None:
        placements.append({"name": name, "src_w": iw, "src_h": ih, "dst_w": w, "dst_h": h})


def rounded_card(c, x, y, w, h, stroke=CARD_BORDER, fill=None, radius=8):
    c.saveState()
    if fill:
        c.setFillColor(HexColor(fill))
    else:
        c.setFillColor(HexColor(PAPER))
    c.setStrokeColor(HexColor(stroke))
    c.setLineWidth(1.5)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    c.restoreState()
