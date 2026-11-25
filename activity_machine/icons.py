"""Word pictures from Google Noto Emoji (Apache 2.0) plus a few Noto-style composites."""

from __future__ import annotations

import math
from functools import lru_cache
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from .config import ROOT

ICONS_DIR = ROOT / "icons"

# Brand-adjacent clear colors for swatches / composites (Noto-like saturation)
RED = "#e53935"
BLUE = "#1e88e5"
YELLOW = "#fdd835"
ORANGE = "#fb8c00"
GREEN = "#43a047"
PURPLE = "#8e24aa"
BROWN = "#8d6e63"
PINK = "#ec407a"
WHITE = "#ffffff"
BLACK = "#212121"
INK = "#1d2b45"
CREAM = "#fff8e1"
DARK_GREEN = "#2e7d32"
METAL = "#90a4ae"
WOOD = "#a1887f"


def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return tuple(int(c[i : i + 2], 16) for i in (0, 2, 4))


def blank(size: int = 512) -> Image.Image:
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))


def to_bytes(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.convert("RGBA").save(buf, format="PNG")
    return buf.getvalue()


@lru_cache(maxsize=256)
def load_emoji(codepoint: str, size: int = 512) -> Image.Image:
    """Load a committed Noto emoji PNG by codepoint (e.g. '1f418')."""
    path = ICONS_DIR / f"emoji_u{codepoint.lower()}.png"
    if not path.exists():
        # try without leading zeros issues
        raise FileNotFoundError(f"Missing Noto emoji PNG: {path}")
    im = Image.open(path).convert("RGBA")
    if im.size != (size, size):
        im = im.resize((size, size), Image.Resampling.LANCZOS)
    return im


def paste_center(base: Image.Image, overlay: Image.Image, scale: float = 0.85, dy: int = 0) -> Image.Image:
    s = int(base.size[0] * scale)
    ov = overlay.resize((s, s), Image.Resampling.LANCZOS)
    x = (base.size[0] - s) // 2
    y = (base.size[1] - s) // 2 + dy
    base.alpha_composite(ov, (x, y))
    return base


def paste_at(base: Image.Image, overlay: Image.Image, cx: float, cy: float, scale: float) -> Image.Image:
    s = int(base.size[0] * scale)
    ov = overlay.resize((s, s), Image.Resampling.LANCZOS)
    x = int(cx * base.size[0] - s / 2)
    y = int(cy * base.size[1] - s / 2)
    base.alpha_composite(ov, (x, y))
    return base


def emoji_icon(codepoint: str, size: int = 512) -> Image.Image:
    img = blank(size)
    return paste_center(img, load_emoji(codepoint, 512), 0.92)


def count_emoji(codepoint: str, n: int, size: int = 512) -> Image.Image:
    """Exact count of one clear emoji object."""
    img = blank(size)
    emoji = load_emoji(codepoint, 512)
    cols = min(n, 3) if n <= 6 else 3
    rows = math.ceil(n / cols)
    cell = size / max(cols, rows)
    item = int(cell * 0.78)
    ov = emoji.resize((item, item), Image.Resampling.LANCZOS)
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= n:
                break
            # center grid
            cx = int((c + 0.5) * size / cols - item / 2)
            cy = int((r + 0.5) * size / rows - item / 2)
            img.alpha_composite(ov, (cx, cy))
            idx += 1
    return img


def color_with_object(swatch: str, object_cp: str, size: int = 512) -> Image.Image:
    """Color word: clear object in that color + color swatch."""
    img = blank(size)
    d = ImageDraw.Draw(img)
    # swatch circle bottom-left
    pad = int(size * 0.06)
    r = int(size * 0.22)
    d.ellipse([pad, size - pad - 2 * r, pad + 2 * r, size - pad], fill=_hex(swatch) + (255,), outline=_hex(INK) + (255,), width=4)
    # object large on the right/center
    paste_at(img, load_emoji(object_cp), 0.58, 0.42, 0.72)
    return img


def _rounded_rect(d, box, fill, outline=None, width=3, radius=24):
    d.rounded_rectangle(box, radius=radius, fill=_hex(fill) + (255,), outline=_hex(outline or fill) + (255,), width=width)


# --- Composites for words without a good single emoji ---

def icon_soil(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    # rich brown mound
    d.ellipse([int(size * 0.08), int(size * 0.48), int(size * 0.92), int(size * 0.95)], fill=_hex(BROWN) + (255,))
    d.ellipse([int(size * 0.15), int(size * 0.42), int(size * 0.85), int(size * 0.78)], fill=_hex("#6d4c41") + (255,))
    # soil crumbs
    for x, y in [(0.25, 0.62), (0.4, 0.7), (0.55, 0.6), (0.7, 0.68), (0.35, 0.78)]:
        rr = int(size * 0.03)
        d.ellipse([int(x * size) - rr, int(y * size) - rr, int(x * size) + rr, int(y * size) + rr], fill=_hex("#5d4037") + (255,))
    paste_at(img, load_emoji("1f331"), 0.5, 0.32, 0.55)
    return img


def icon_roots(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    # soil line
    d.rectangle([0, int(size * 0.42), size, size], fill=_hex("#efebe9") + (255,))
    d.ellipse([int(size * 0.05), int(size * 0.35), int(size * 0.95), int(size * 0.55)], fill=_hex(BROWN) + (220,))
    # sprout above ground
    paste_at(img, load_emoji("1f331"), 0.5, 0.22, 0.4)
    # branching roots (smooth tapered strokes)
    cx, cy = size // 2, int(size * 0.5)
    root_paths = [
        [(cx, cy), (cx - 40, cy + 60), (cx - 90, cy + 140), (cx - 120, cy + 200)],
        [(cx, cy), (cx + 10, cy + 80), (cx, cy + 160), (cx + 20, cy + 220)],
        [(cx, cy), (cx + 50, cy + 70), (cx + 110, cy + 150), (cx + 140, cy + 210)],
        [(cx - 20, cy + 40), (cx - 70, cy + 100), (cx - 60, cy + 180)],
        [(cx + 25, cy + 50), (cx + 80, cy + 110), (cx + 70, cy + 190)],
    ]
    for pts in root_paths:
        d.line(pts, fill=_hex("#5d4037") + (255,), width=max(6, size // 40), joint="curve")
        # root tips
        x, y = pts[-1]
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=_hex("#6d4c41") + (255,))
    return img


def icon_shovel(size=512):
    """Clean detailed shovel in a soft Noto-like style (no shovel emoji exists)."""
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    # wooden handle
    d.rounded_rectangle([s * 0.44, s * 0.08, s * 0.56, s * 0.55], radius=12, fill=_hex(WOOD) + (255,), outline=_hex("#6d4c41") + (255,), width=3)
    # D-grip
    d.rounded_rectangle([s * 0.34, s * 0.06, s * 0.66, s * 0.16], radius=10, fill=_hex(WOOD) + (255,), outline=_hex("#6d4c41") + (255,), width=3)
    d.rounded_rectangle([s * 0.40, s * 0.09, s * 0.60, s * 0.14], radius=6, fill=(0, 0, 0, 0))
    # metal shaft collar
    d.rounded_rectangle([s * 0.42, s * 0.50, s * 0.58, s * 0.58], radius=4, fill=_hex(METAL) + (255,), outline=_hex("#607d8b") + (255,), width=2)
    # blade
    blade = [
        (s * 0.28, s * 0.58),
        (s * 0.72, s * 0.58),
        (s * 0.68, s * 0.88),
        (s * 0.50, s * 0.95),
        (s * 0.32, s * 0.88),
    ]
    d.polygon(blade, fill=_hex("#78909c") + (255,), outline=_hex("#455a64") + (255,))
    # blade highlight
    d.line([(s * 0.38, s * 0.62), (s * 0.38, s * 0.82)], fill=_hex("#cfd8dc") + (255,), width=4)
    return img


def icon_watering_can(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    # body
    d.rounded_rectangle([s * 0.22, s * 0.38, s * 0.68, s * 0.78], radius=28, fill=_hex(BLUE) + (255,), outline=_hex("#1565c0") + (255,), width=4)
    # top opening
    d.ellipse([s * 0.28, s * 0.30, s * 0.62, s * 0.48], fill=_hex("#64b5f6") + (255,), outline=_hex("#1565c0") + (255,), width=3)
    # handle
    d.arc([s * 0.08, s * 0.40, s * 0.35, s * 0.72], 90, 270, fill=_hex("#1565c0") + (255,), width=14)
    # spout
    d.polygon([(s * 0.65, s * 0.48), (s * 0.92, s * 0.32), (s * 0.95, s * 0.40), (s * 0.68, s * 0.58)], fill=_hex(BLUE) + (255,), outline=_hex("#1565c0") + (255,))
    # droplets from spout
    paste_at(img, load_emoji("1f4a7"), 0.88, 0.55, 0.22)
    paste_at(img, load_emoji("1f4a7"), 0.82, 0.68, 0.16)
    return img


def icon_wreath(size=512):
    img = blank(size)
    leaf = load_emoji("1f33f", 512)
    berry = load_emoji("1f534", 512)
    bow = load_emoji("1f380", 512)
    for i in range(12):
        a = i * math.pi / 6
        paste_at(img, leaf, 0.5 + math.cos(a) * 0.32, 0.52 + math.sin(a) * 0.32, 0.28)
    for i in range(8):
        a = i * math.pi / 4 + 0.2
        paste_at(img, berry, 0.5 + math.cos(a) * 0.30, 0.52 + math.sin(a) * 0.30, 0.12)
    paste_at(img, bow, 0.5, 0.18, 0.35)
    return img


def icon_stocking(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    # cuff
    d.rounded_rectangle([s * 0.32, s * 0.12, s * 0.68, s * 0.28], radius=8, fill=_hex(WHITE) + (255,), outline=_hex(INK) + (255,), width=3)
    # leg
    d.rounded_rectangle([s * 0.36, s * 0.24, s * 0.64, s * 0.62], radius=12, fill=_hex(RED) + (255,), outline=_hex("#b71c1c") + (255,), width=3)
    # foot
    d.ellipse([s * 0.34, s * 0.52, s * 0.88, s * 0.88], fill=_hex(RED) + (255,), outline=_hex("#b71c1c") + (255,), width=3)
    d.rounded_rectangle([s * 0.36, s * 0.52, s * 0.64, s * 0.7], radius=4, fill=_hex(RED) + (255,))
    # white toe highlight + tiny gift emoji
    paste_at(img, load_emoji("1f381"), 0.55, 0.42, 0.22)
    return img


def icon_ornament(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    # cap
    d.rounded_rectangle([s * 0.40, s * 0.12, s * 0.60, s * 0.28], radius=6, fill=_hex(YELLOW) + (255,), outline=_hex(ORANGE) + (255,), width=3)
    d.arc([s * 0.44, s * 0.04, s * 0.56, s * 0.18], 180, 0, fill=_hex(METAL) + (255,), width=6)
    # bauble
    d.ellipse([s * 0.18, s * 0.24, s * 0.82, s * 0.90], fill=_hex(RED) + (255,), outline=_hex("#b71c1c") + (255,), width=4)
    # shine
    d.ellipse([s * 0.30, s * 0.35, s * 0.48, s * 0.55], fill=_hex("#ef9a9a") + (200,))
    # stripe
    d.arc([s * 0.22, s * 0.40, s * 0.78, s * 0.70], 200, 340, fill=_hex(YELLOW) + (255,), width=10)
    paste_at(img, load_emoji("1f380"), 0.5, 0.08, 0.2)
    return img


def icon_candy_cane(size=512):
    """Smooth red-and-white candy cane (no dedicated Noto emoji) in a soft emoji style."""
    s = size
    # Draw at 2x then downscale for smoother edges
    hi = s * 2
    cane = Image.new("RGBA", (hi, hi), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cane)
    thickness = int(hi * 0.13)
    pts = []
    for a in range(200, 375, 2):
        rad = math.radians(a)
        cx = hi * 0.50 + math.cos(rad) * hi * 0.22
        cy = hi * 0.34 + math.sin(rad) * hi * 0.20
        pts.append((cx, cy))
    last = pts[-1]
    for t in range(0, 110):
        pts.append((last[0], last[1] + t * hi * 0.005))
    # soft gray rim
    for x, y in pts:
        r = thickness // 2 + 6
        cd.ellipse([x - r, y - r, x + r, y + r], fill=(224, 224, 224, 255))
    body = Image.new("RGBA", (hi, hi), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    for x, y in pts:
        r = thickness // 2
        bd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 255))
    # glossy highlight along left
    gloss = Image.new("RGBA", (hi, hi), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    for i, (x, y) in enumerate(pts[::3]):
        if i % 2:
            continue
        r = max(4, thickness // 5)
        gd.ellipse([x - thickness // 3 - r, y - r, x - thickness // 3 + r, y + r], fill=(255, 255, 255, 160))
    stripe = Image.new("RGBA", (hi, hi), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripe)
    for i in range(0, len(pts) - 1, 14):
        x1, y1 = pts[i]
        x2, y2 = pts[min(i + 4, len(pts) - 1)]
        dx, dy = x2 - x1, y2 - y1
        px, py = -dy, dx
        plen = math.hypot(px, py) or 1
        px, py = px / plen * thickness * 0.55, py / plen * thickness * 0.55
        sd.line([(x1 - px, y1 - py), (x1 + px, y1 + py)], fill=_hex(RED) + (255,), width=max(14, thickness // 2))
    cane_mask = body.split()[-1]
    stripe.putalpha(ImageChops.multiply(stripe.split()[-1], cane_mask))
    gloss.putalpha(ImageChops.multiply(gloss.split()[-1], cane_mask))
    out = Image.new("RGBA", (hi, hi), (0, 0, 0, 0))
    out.alpha_composite(cane)
    out.alpha_composite(body)
    out.alpha_composite(stripe)
    out.alpha_composite(gloss)
    return out.resize((s, s), Image.Resampling.LANCZOS)


def icon_snowball(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    d.ellipse([s * 0.12, s * 0.12, s * 0.88, s * 0.88], fill=_hex("#e3f2fd") + (255,), outline=_hex("#90caf9") + (255,), width=6)
    d.ellipse([s * 0.25, s * 0.22, s * 0.45, s * 0.40], fill=_hex(WHITE) + (220,))
    paste_at(img, load_emoji("2744"), 0.7, 0.7, 0.28)
    paste_at(img, load_emoji("2744"), 0.3, 0.65, 0.18)
    return img


def icon_dig(size=512):
    img = icon_soil(size)
    paste_at(img, load_emoji("26cf"), 0.72, 0.35, 0.45)
    return img


def icon_blanket(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    # folded blanket with soft checks
    d.rounded_rectangle([s * 0.1, s * 0.2, s * 0.9, s * 0.85], radius=28, fill=_hex(PURPLE) + (255,), outline=_hex("#6a1b9a") + (255,), width=4)
    colors = [PURPLE, BLUE, "#ce93d8", "#90caf9"]
    for r in range(4):
        for c in range(4):
            d.rectangle(
                [s * (0.16 + c * 0.17), s * (0.28 + r * 0.12), s * (0.31 + c * 0.17), s * (0.38 + r * 0.12)],
                fill=_hex(colors[(r + c) % 4]) + (255,),
            )
    # fold edge
    d.polygon([(s * 0.1, s * 0.2), (s * 0.28, s * 0.12), (s * 0.9, s * 0.12), (s * 0.9, s * 0.2)], fill=_hex("#7e57c2") + (255,))
    return img


def icon_lights(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    # wire
    pts = [(s * 0.08, s * 0.35), (s * 0.25, s * 0.25), (s * 0.45, s * 0.4), (s * 0.65, s * 0.22), (s * 0.85, s * 0.38), (s * 0.95, s * 0.3)]
    d.line(pts, fill=_hex(DARK_GREEN) + (255,), width=6, joint="curve")
    bulbs = ["1f534", "1f7e8", "1f7e9", "1f535", "1f7ea", "1f7e7"]
    for i, cp in enumerate(bulbs):
        t = i / (len(bulbs) - 1)
        # sample along polyline approx
        x = 0.12 + t * 0.78
        y = 0.28 + (0.08 if i % 2 == 0 else -0.05)
        paste_at(img, load_emoji(cp), x, y + 0.12, 0.2)
    paste_at(img, load_emoji("2728"), 0.5, 0.7, 0.35)
    return img


def icon_rug(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    d.rounded_rectangle([s * 0.08, s * 0.22, s * 0.92, s * 0.82], radius=20, fill=_hex(RED) + (255,), outline=_hex("#b71c1c") + (255,), width=5)
    d.rounded_rectangle([s * 0.16, s * 0.30, s * 0.84, s * 0.74], radius=14, fill=_hex(CREAM) + (255,), outline=_hex(ORANGE) + (255,), width=4)
    # center medallion via star emoji
    paste_at(img, load_emoji("2b50"), 0.5, 0.52, 0.35)
    return img


def icon_scarf(size=512):
    # Prefer Noto scarf emoji when present
    path = ICONS_DIR / "emoji_u1f9e3.png"
    if path.exists():
        return emoji_icon("1f9e3", size)
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    d.rounded_rectangle([s * 0.15, s * 0.28, s * 0.85, s * 0.48], radius=20, fill=_hex(GREEN) + (255,))
    d.rounded_rectangle([s * 0.55, s * 0.4, s * 0.78, s * 0.88], radius=16, fill=_hex(GREEN) + (255,))
    return img


def icon_rectangle(size=512):
    img = blank(size)
    d = ImageDraw.Draw(img)
    s = size
    d.rounded_rectangle([s * 0.08, s * 0.28, s * 0.92, s * 0.72], radius=28, fill=_hex(BLUE) + (255,), outline=_hex("#1565c0") + (255,), width=6)
    return img


def icon_orange_color(size=512):
    return color_with_object(ORANGE, "1f34a", size)


def icon_orange_fruit(size=512):
    return emoji_icon("1f34a", size)


# Primary word -> renderer
def _simple(cp: str):
    return lambda size=512, _cp=cp: emoji_icon(_cp, size)


ICON_BUILDERS = {
    # zoo
    "elephant": _simple("1f418"),
    "giraffe": _simple("1f992"),
    "zebra": _simple("1f993"),
    "lion": _simple("1f981"),
    "tiger": _simple("1f42f"),
    "cheetah": _simple("1f406"),
    "gorilla": _simple("1f98d"),
    "penguin": _simple("1f427"),
    "hippo": _simple("1f99b"),
    "rhino": _simple("1f98f"),
    "panda": _simple("1f43c"),
    "koala": _simple("1f428"),
    "kangaroo": _simple("1f998"),
    "flamingo": _simple("1f9a9"),
    "bear": _simple("1f43b"),
    # garden
    "seed": _simple("1f331"),
    "soil": icon_soil,
    "shovel": icon_shovel,
    "watering can": icon_watering_can,
    "dig": icon_dig,
    "plant": _simple("1fab4"),
    "water": _simple("1f4a7"),
    "sunlight": _simple("2600"),
    "roots": icon_roots,
    "sprout": _simple("1f331"),
    "flower": _simple("1f338"),
    "bee": _simple("1f41d"),
    "worm": _simple("1fab1"),
    "ladybug": _simple("1f41e"),
    "butterfly": _simple("1f98b"),
    "tomato": _simple("1f345"),
    "carrot": _simple("1f955"),
    "sunflower": _simple("1f33b"),
    # shapes
    "circle": _simple("1f535"),
    "square": _simple("1f7e6"),
    "triangle": _simple("1f53a"),
    "rectangle": icon_rectangle,
    "star": _simple("2b50"),
    "heart": _simple("2764"),
    "plate": _simple("1f37d"),
    "clock": _simple("1f552"),
    "cracker": _simple("1f358"),
    "block": _simple("1f9f1"),
    "sandwich": _simple("1f96a"),
    "flag": _simple("1f6a9"),
    "door": _simple("1f6aa"),
    "book": _simple("1f4d6"),
    "rug": icon_rug,
    "cookie": _simple("1f36a"),
    # numbers
    "one": lambda s=512: count_emoji("1f34e", 1, s),
    "two": lambda s=512: count_emoji("1f34e", 2, s),
    "three": lambda s=512: count_emoji("1f34e", 3, s),
    "four": lambda s=512: count_emoji("1f34e", 4, s),
    "five": lambda s=512: count_emoji("1f34e", 5, s),
    "ball": _simple("26bd"),
    "cats": lambda s=512: count_emoji("1f431", 3, s),
    "cookies": lambda s=512: count_emoji("1f36a", 4, s),
    "cups": lambda s=512: count_emoji("1f375", 3, s),
    "tomatoes": lambda s=512: count_emoji("1f345", 5, s),
    "ducks": lambda s=512: count_emoji("1f986", 2, s),
    "steps": _simple("1fa9c"),
    "walk": _simple("1f6b6"),
    "count": _simple("1f522"),
    # colors
    "red": lambda s=512: color_with_object(RED, "1f34e", s),
    "blue": lambda s=512: color_with_object(BLUE, "1f535", s),
    "yellow": lambda s=512: color_with_object(YELLOW, "1f34b", s),
    "orange": icon_orange_color,
    "green": lambda s=512: color_with_object(GREEN, "1f34f", s),
    "purple": lambda s=512: color_with_object(PURPLE, "1f347", s),
    "yarn": _simple("1f9f6"),
    "banana": _simple("1f34c"),
    "orange fruit": icon_orange_fruit,
    "boots": _simple("1f462"),
    "grass": _simple("1f33f"),
    "blanket": icon_blanket,
    "picnic": _simple("1f9fa"),
    # snow
    "snow": _simple("1f328"),
    "snowflake": _simple("2744"),
    "snowman": _simple("26c4"),
    "snowball": icon_snowball,
    "cold": _simple("1f976"),
    "warm": _simple("1f31e"),
    "hat": _simple("1f9e2"),
    "scarf": icon_scarf,
    "gloves": _simple("1f9e4"),
    "coat": _simple("1f9e5"),
    "winter": _simple("2744"),
    "window": _simple("1fa9f"),
    "ice": _simple("1f9ca"),
    # christmas
    "tree": _simple("1f384"),
    "wreath": icon_wreath,
    "stocking": icon_stocking,
    "lights": icon_lights,
    "bell": _simple("1f514"),
    "ornament": icon_ornament,
    "candy cane": icon_candy_cane,
    "reindeer": _simple("1f98c"),
    "present": _simple("1f381"),
    "candle": _simple("1f56f"),
    "card": _simple("1f48c"),
    "box": _simple("1f4e6"),
    "ribbon": _simple("1f380"),
    "bow": _simple("1f380"),
}

# Back-compat for checks that look for ICON_MAP
ICON_MAP = ICON_BUILDERS


def get_icon(word: str, size: int = 256) -> Image.Image:
    key = word.strip().lower()
    fn = ICON_BUILDERS.get(key)
    if fn is None:
        img = blank(max(size, 256))
        return img.resize((size, size), Image.Resampling.LANCZOS) if size != img.size[0] else img
    im = fn(512)
    if size != 512:
        im = im.resize((size, size), Image.Resampling.LANCZOS)
    return im
