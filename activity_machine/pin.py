"""Pinterest preview image: exactly 1000 x 1500 px."""

from __future__ import annotations

import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import (
    BERRY,
    CARD_BORDER,
    CHARACTER_FILES,
    CHARACTERS_DIR,
    EPISODE_CHARACTER,
    FONT_BODY_BOLD,
    FONT_HEADING,
    INK,
    PAPER,
    RAINBOW,
    SKY,
)
from .icons import get_icon

_THUMB_CACHE: dict[str, Image.Image] = {}


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
        "flashcards": f"{short} Flashcards for Toddlers",
        "bingo": f"{short} Bingo for Toddlers",
        "memory": f"{short} Memory Game for Toddlers",
    }
    return labels.get(activity, f"{short} Printable for Toddlers")


def fetch_episode_thumb(youtube_id: str) -> Image.Image | None:
    if youtube_id in _THUMB_CACHE:
        return _THUMB_CACHE[youtube_id].copy()
    for name in ("maxresdefault.jpg", "hqdefault.jpg", "sddefault.jpg"):
        url = f"https://i.ytimg.com/vi/{youtube_id}/{name}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            from io import BytesIO

            im = Image.open(BytesIO(data)).convert("RGB")
            # reject tiny placeholders
            if im.size[0] < 200 or im.size[1] < 100:
                continue
            _THUMB_CACHE[youtube_id] = im
            return im.copy()
        except Exception:
            continue
    return None


def _rounded_thumb(im: Image.Image, size: tuple[int, int], radius: int = 28) -> Image.Image:
    im = im.copy()
    # cover-fit
    tw, th = size
    scale = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    mask = Image.new("L", size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, tw - 1, th - 1], radius=radius, fill=255)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(im.convert("RGBA"), (0, 0))
    out.putalpha(mask)
    return out


def build_pin(
    out_path: Path,
    episode,
    activity: str,
    preview_words: list[str] | None = None,
) -> Path:
    W, H = 1000, 1500
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # soft warm atmosphere
    for i in range(H):
        t = i / H
        r = 255
        g = int(249 - 8 * t)
        b = int(239 - 16 * t)
        d.line([(0, i), (W, i)], fill=(r, g, b))

    # soft top wash
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([-180, -360, W + 180, 380], fill=(255, 233, 194, 120))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    heading = _font(FONT_HEADING, 34)
    body = _font(FONT_BODY_BOLD, 26)
    small = _font(FONT_BODY_BOLD, 24)

    # rainbow wordmark
    mark = "LEARN WITH IAN"
    total = d.textlength(mark, font=heading)
    x = (W - total) / 2
    y = 36
    for i, ch in enumerate(mark):
        d.text((x, y), ch, font=heading, fill=RAINBOW[i % len(RAINBOW)])
        x += d.textlength(ch, font=heading)

    # Small "Free" badge once, top-right corner
    badge_font = _font(FONT_BODY_BOLD, 22)
    badge_text = "Free"
    bw = d.textlength(badge_text, font=badge_font) + 28
    bh = 40
    bx, by = W - 36 - bw, 28
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=BERRY)
    d.text((bx + bw / 2, by + bh / 2), badge_text, font=badge_font, fill="white", anchor="mm")

    # Title — does NOT start with FREE
    title = _activity_pin_title(activity, episode.title)
    title_font = _font(FONT_HEADING, 46)
    lines = _wrap(d, title, title_font, W - 100)
    ty = 110
    for line in lines[:3]:
        d.text((W / 2, ty), line, font=title_font, fill=INK, anchor="mt")
        ty += 54

    # preview grid of icons
    words = preview_words or list(episode.words)[:6]
    words = words[:6]
    grid_top = ty + 18
    cols = 3
    cell = 200
    gap = 20
    grid_w = cols * cell + (cols - 1) * gap
    gx0 = (W - grid_w) // 2
    for i, word in enumerate(words):
        r, c = divmod(i, cols)
        x0 = gx0 + c * (cell + gap)
        y0 = grid_top + r * (cell + gap + 30)
        d.rounded_rectangle(
            [x0, y0, x0 + cell, y0 + cell],
            radius=22,
            outline=CARD_BORDER,
            width=4,
            fill="#fffdf8",
        )
        icon = get_icon(word, 180).convert("RGBA")
        icon = icon.resize((140, 140), Image.Resampling.LANCZOS)
        img.paste(icon, (x0 + 30, y0 + 16), icon)
        d.text((x0 + cell / 2, y0 + cell - 26), word, font=small, fill=INK, anchor="mt")

    # Bottom product preview block: episode thumbnail + character + captions
    bottom_top = 980
    d.rounded_rectangle([40, bottom_top, W - 40, H - 70], radius=32, fill="#fffdf8", outline=CARD_BORDER, width=4)

    thumb = fetch_episode_thumb(episode.youtube_id)
    thumb_box = (70, bottom_top + 36, 520, 280)
    if thumb is not None:
        framed = _rounded_thumb(thumb, (thumb_box[2], thumb_box[3]), radius=24)
        # frame ring
        d.rounded_rectangle(
            [thumb_box[0] - 6, thumb_box[1] - 6, thumb_box[0] + thumb_box[2] + 6, thumb_box[1] + thumb_box[3] + 6],
            radius=28,
            outline=SKY,
            width=5,
        )
        img.paste(framed, (thumb_box[0], thumb_box[1]), framed)
    else:
        d.rounded_rectangle(
            [thumb_box[0], thumb_box[1], thumb_box[0] + thumb_box[2], thumb_box[1] + thumb_box[3]],
            radius=24,
            fill="#ffe9c2",
            outline=SKY,
            width=4,
        )

    # one full character on the right of the thumb (never cropped)
    ch_name = EPISODE_CHARACTER.get(episode.episode, "ian")
    ch_file = CHARACTER_FILES.get(ch_name, "ian.png")
    ch_path = CHARACTERS_DIR / ch_file
    if ch_path.exists():
        ch = Image.open(ch_path).convert("RGBA")
        max_h = 340
        scale = max_h / ch.height
        # never crop; fit fully
        ch = ch.resize((int(ch.width * scale), int(ch.height * scale)), Image.Resampling.LANCZOS)
        cx = W - 70 - ch.width
        cy = bottom_top + 20
        # keep inside bottom card
        if cy + ch.height > H - 90:
            scale2 = (H - 90 - cy) / ch.height
            ch = ch.resize((int(ch.width * scale2), int(ch.height * scale2)), Image.Resampling.LANCZOS)
            cx = W - 70 - ch.width
        img.paste(ch, (cx, cy), ch)

    ep_font = _font(FONT_BODY_BOLD, 24)
    d.text(
        (70, bottom_top + 330),
        f"Goes with the episode {episode.title}",
        font=ep_font,
        fill=SKY,
    )

    # bottom brand bar
    d.rectangle([0, H - 70, W, H], fill="#fff3d6")
    d.text((W / 2, H - 35), "learnwithian.com", font=body, fill=INK, anchor="mm")

    assert img.size == (1000, 1500)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG")
    return out_path
