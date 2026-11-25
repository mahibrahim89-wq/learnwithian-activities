"""Pinterest preview image: exactly 1000 x 1500 px."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import (
    BERRY,
    CARD_BORDER,
    CHARACTER_FILES,
    CHARACTERS_DIR,
    FONT_BODY_BOLD,
    FONT_HEADING,
    INK,
    LEAF,
    PAPER,
    RAINBOW,
    SKY,
    SUN,
    WORD_CHARACTERS,
)
from .icons import get_icon


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def _wrap(draw, text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for w in words:
        trial = (line + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def _activity_pin_title(activity: str, episode_title: str) -> str:
    short = episode_title.replace("Ian's ", "").replace("Ian’s ", "")
    labels = {
        "flashcards": f"FREE {short} Flashcards for Toddlers",
        "bingo": f"FREE {short} Bingo for Toddlers",
        "memory": f"FREE {short} Memory Game for Toddlers",
    }
    return labels.get(activity, f"FREE {short} Printable for Toddlers")


def build_pin(
    out_path: Path,
    episode,
    activity: str,
    preview_words: list[str] | None = None,
) -> Path:
    W, H = 1000, 1500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # soft atmospheric bands (not flat)
    for i in range(H):
        t = i / H
        # gentle warm wash
        r = int(255)
        g = int(249 - 10 * t)
        b = int(239 - 20 * t)
        d.line([(0, i), (W, i)], fill=(r, g, b))

    # decorative top arc
    d.ellipse([-200, -400, W + 200, 420], fill="#ffe9c2")

    heading = _font(FONT_HEADING, 42)
    body = _font(FONT_BODY_BOLD, 28)
    small = _font(FONT_BODY_BOLD, 26)

    # rainbow wordmark
    mark = "LEARN WITH IAN"
    mark_font = _font(FONT_HEADING, 36)
    total = d.textlength(mark, font=mark_font)
    x = (W - total) / 2
    y = 48
    for i, ch in enumerate(mark):
        color = RAINBOW[i % len(RAINBOW)]
        d.text((x, y), ch, font=mark_font, fill=color)
        x += d.textlength(ch, font=mark_font)

    # FREE badge text (not a floating sticker on hero media — this IS the composition)
    free_font = _font(FONT_HEADING, 64)
    d.text((W / 2, 120), "FREE", font=free_font, fill=BERRY, anchor="mt")

    title = _activity_pin_title(activity, episode.title)
    title_font = _font(FONT_HEADING, 48)
    lines = _wrap(d, title, title_font, W - 100)
    ty = 210
    for line in lines[:4]:
        d.text((W / 2, ty), line, font=title_font, fill=INK, anchor="mt")
        ty += 58

    # preview grid of icons
    words = preview_words or list(episode.words)[:6]
    words = words[:6]
    grid_top = ty + 30
    cols = 3
    cell = 220
    gap = 24
    grid_w = cols * cell + (cols - 1) * gap
    gx0 = (W - grid_w) // 2
    for i, word in enumerate(words):
        r, c = divmod(i, cols)
        x0 = gx0 + c * (cell + gap)
        y0 = grid_top + r * (cell + gap + 36)
        # soft tile (interaction preview, not a marketing card cluster)
        d.rounded_rectangle([x0, y0, x0 + cell, y0 + cell], radius=24, outline=CARD_BORDER, width=4, fill="#fffdf8")
        icon = get_icon(word, 180).convert("RGBA")
        icon = icon.resize((150, 150), Image.Resampling.LANCZOS)
        img.paste(icon, (x0 + 35, y0 + 20), icon)
        d.text((x0 + cell / 2, y0 + cell - 28), word, font=small, fill=INK, anchor="mt")

    # character
    ch_name = WORD_CHARACTERS.get((preview_words or episode.words)[0].lower(), "ian")
    ch_file = CHARACTER_FILES.get(ch_name, "ian.png")
    ch_path = CHARACTERS_DIR / ch_file
    if ch_path.exists():
        ch = Image.open(ch_path).convert("RGBA")
        max_h = 380
        scale = max_h / ch.height
        ch = ch.resize((int(ch.width * scale), int(ch.height * scale)), Image.Resampling.LANCZOS)
        img.paste(ch, (W - ch.width - 40, H - ch.height - 120), ch)

    # bottom brand
    d.rectangle([0, H - 90, W, H], fill="#fff3d6")
    d.text((W / 2, H - 45), "learnwithian.com", font=body, fill=INK, anchor="mm")

    # episode hint
    ep_font = _font(FONT_BODY_BOLD, 22)
    d.text(
        (40, H - 130),
        f"Goes with: {episode.title}",
        font=ep_font,
        fill=SKY,
    )

    assert img.size == (1000, 1500)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG")
    return out_path
