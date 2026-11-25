"""Simple code-drawn icons for activity words. No generative AI."""

from __future__ import annotations

import math
from io import BytesIO

from PIL import Image, ImageDraw

from .config import BERRY, GRAPE, INK, LEAF, PAPER, SKY, SUN

# Named brand / clear colors
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
GRAY = "#90a4ae"
LIGHT_BLUE = "#81d4fa"
CREAM = "#fff8e1"
DARK_GREEN = "#2e7d32"
TAN = "#d7ccc8"


def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return tuple(int(c[i : i + 2], 16) for i in (0, 2, 4))


def blank(size: int = 256, bg=None) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0) if bg is None else _hex(bg) + (255,))
    return img, ImageDraw.Draw(img)


def to_bytes(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _ellipse(d, box, fill, outline=None, width=2):
    d.ellipse(box, fill=_hex(fill) + (255,), outline=_hex(outline or fill) + (255,), width=width)


def _rect(d, box, fill, outline=None, width=2):
    d.rectangle(box, fill=_hex(fill) + (255,), outline=_hex(outline or INK) + (255,), width=width)


def _polygon(d, pts, fill, outline=None, width=2):
    d.polygon(pts, fill=_hex(fill) + (255,), outline=_hex(outline or INK) + (255,), width=width)


def _line(d, pts, fill, width=4):
    d.line(pts, fill=_hex(fill) + (255,), width=width)


def _star_points(cx, cy, r_outer, r_inner, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = rot + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _heart_points(cx, cy, s):
    pts = []
    for t in [i / 40 * 2 * math.pi for i in range(41)]:
        x = 16 * math.sin(t) ** 3
        y = -(
            13 * math.cos(t)
            - 5 * math.cos(2 * t)
            - 2 * math.cos(3 * t)
            - math.cos(4 * t)
        )
        pts.append((cx + x * s / 16, cy + y * s / 16))
    return pts


def _count_items(draw_one, n: int, size: int = 256) -> Image.Image:
    img, d = blank(size)
    # layout grid
    cols = min(n, 3) if n <= 6 else 3
    rows = math.ceil(n / cols)
    cell_w = size / (cols + 0.4)
    cell_h = size / (rows + 0.4)
    item = int(min(cell_w, cell_h) * 0.75)
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= n:
                break
            cx = (c + 0.7) * (size / (cols + 0.2))
            cy = (r + 0.7) * (size / (rows + 0.2))
            draw_one(d, cx, cy, item)
            idx += 1
    return img


# --- Animal / zoo ---

def icon_elephant(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.25, s * 0.35, s * 0.75, s * 0.75], GRAY, INK)
    _ellipse(d, [s * 0.55, s * 0.25, s * 0.85, s * 0.55], GRAY, INK)  # head
    _ellipse(d, [s * 0.15, s * 0.4, s * 0.35, s * 0.7], GRAY, INK)  # ear
    _rect(d, [s * 0.72, s * 0.45, s * 0.82, s * 0.85], GRAY, INK)  # trunk
    _ellipse(d, [s * 0.7, s * 0.35, s * 0.76, s * 0.41], BLACK)  # eye
    return img


def icon_giraffe(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.42, s * 0.15, s * 0.58, s * 0.7], SUN, INK)
    for y in range(4):
        _ellipse(d, [s * 0.44, s * (0.2 + y * 0.12), s * 0.56, s * (0.28 + y * 0.12)], BROWN)
    _ellipse(d, [s * 0.38, s * 0.05, s * 0.68, s * 0.28], SUN, INK)
    _ellipse(d, [s * 0.55, s * 0.12, s * 0.6, s * 0.17], BLACK)
    _rect(d, [s * 0.3, s * 0.65, s * 0.7, s * 0.9], SUN, INK)
    return img


def icon_zebra(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.35, s * 0.8, s * 0.75], WHITE, INK)
    for i in range(5):
        x = s * (0.28 + i * 0.1)
        _rect(d, [x, s * 0.38, x + s * 0.05, s * 0.72], BLACK)
    _ellipse(d, [s * 0.65, s * 0.22, s * 0.9, s * 0.5], WHITE, INK)
    return img


def icon_lion(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.1, s * 0.15, s * 0.9, s * 0.9], ORANGE, BROWN)
    _ellipse(d, [s * 0.28, s * 0.32, s * 0.72, s * 0.78], SUN, INK)
    _ellipse(d, [s * 0.38, s * 0.48, s * 0.45, s * 0.55], BLACK)
    _ellipse(d, [s * 0.55, s * 0.48, s * 0.62, s * 0.55], BLACK)
    return img


def icon_tiger(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.25, s * 0.8, s * 0.85], ORANGE, INK)
    for i in range(4):
        y = s * (0.35 + i * 0.12)
        _line(d, [(s * 0.3, y), (s * 0.7, y)], BLACK, 4)
    _ellipse(d, [s * 0.38, s * 0.48, s * 0.45, s * 0.55], BLACK)
    _ellipse(d, [s * 0.55, s * 0.48, s * 0.62, s * 0.55], BLACK)
    return img


def icon_cheetah(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.4, s * 0.85, s * 0.75], SUN, INK)
    _ellipse(d, [s * 0.6, s * 0.25, s * 0.9, s * 0.55], SUN, INK)
    for i in range(8):
        x = s * (0.25 + (i % 4) * 0.12)
        y = s * (0.48 + (i // 4) * 0.12)
        _ellipse(d, [x, y, x + s * 0.05, y + s * 0.05], BLACK)
    return img


def icon_gorilla(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.2, s * 0.8, s * 0.85], "#5d4037", INK)
    _ellipse(d, [s * 0.3, s * 0.4, s * 0.7, s * 0.75], TAN, INK)
    _ellipse(d, [s * 0.38, s * 0.48, s * 0.46, s * 0.56], BLACK)
    _ellipse(d, [s * 0.54, s * 0.48, s * 0.62, s * 0.56], BLACK)
    return img


def icon_penguin(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.28, s * 0.15, s * 0.72, s * 0.85], BLACK, INK)
    _ellipse(d, [s * 0.35, s * 0.35, s * 0.65, s * 0.8], WHITE)
    _ellipse(d, [s * 0.4, s * 0.28, s * 0.48, s * 0.36], WHITE)
    _ellipse(d, [s * 0.52, s * 0.28, s * 0.6, s * 0.36], WHITE)
    _polygon(d, [(s * 0.5, s * 0.38), (s * 0.42, s * 0.45), (s * 0.58, s * 0.45)], ORANGE)
    return img


def icon_hippo(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.35, s * 0.85, s * 0.8], GRAY, INK)
    _ellipse(d, [s * 0.25, s * 0.45, s * 0.75, s * 0.7], "#b0bec5")
    _ellipse(d, [s * 0.38, s * 0.5, s * 0.45, s * 0.57], BLACK)
    _ellipse(d, [s * 0.55, s * 0.5, s * 0.62, s * 0.57], BLACK)
    return img


def icon_rhino(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.4, s * 0.8, s * 0.8], GRAY, INK)
    _ellipse(d, [s * 0.55, s * 0.3, s * 0.9, s * 0.65], GRAY, INK)
    _polygon(d, [(s * 0.88, s * 0.4), (s * 0.98, s * 0.35), (s * 0.88, s * 0.5)], TAN, INK)
    return img


def icon_panda(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.25, s * 0.8, s * 0.85], WHITE, INK)
    _ellipse(d, [s * 0.22, s * 0.18, s * 0.4, s * 0.38], BLACK)
    _ellipse(d, [s * 0.6, s * 0.18, s * 0.78, s * 0.38], BLACK)
    _ellipse(d, [s * 0.35, s * 0.45, s * 0.48, s * 0.58], BLACK)
    _ellipse(d, [s * 0.52, s * 0.45, s * 0.65, s * 0.58], BLACK)
    return img


def icon_koala(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.08, s * 0.25, s * 0.35, s * 0.55], GRAY, INK)
    _ellipse(d, [s * 0.65, s * 0.25, s * 0.92, s * 0.55], GRAY, INK)
    _ellipse(d, [s * 0.22, s * 0.3, s * 0.78, s * 0.85], GRAY, INK)
    _ellipse(d, [s * 0.38, s * 0.5, s * 0.48, s * 0.6], BLACK)
    _ellipse(d, [s * 0.52, s * 0.5, s * 0.62, s * 0.6], BLACK)
    _ellipse(d, [s * 0.42, s * 0.62, s * 0.58, s * 0.72], "#efebe9")
    return img


def icon_kangaroo(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.3, s * 0.35, s * 0.7, s * 0.75], BROWN, INK)
    _ellipse(d, [s * 0.45, s * 0.15, s * 0.75, s * 0.45], BROWN, INK)
    _polygon(d, [(s * 0.35, s * 0.7), (s * 0.15, s * 0.9), (s * 0.45, s * 0.85)], BROWN, INK)
    return img


def icon_flamingo(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.35, s * 0.2, s * 0.7, s * 0.5], PINK, INK)
    _line(d, [(s * 0.5, s * 0.5), (s * 0.45, s * 0.85)], PINK, 6)
    _polygon(d, [(s * 0.7, s * 0.32), (s * 0.9, s * 0.28), (s * 0.7, s * 0.4)], ORANGE)
    return img


def icon_bear(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.12, s * 0.38, s * 0.35], BROWN, INK)
    _ellipse(d, [s * 0.62, s * 0.12, s * 0.85, s * 0.35], BROWN, INK)
    _ellipse(d, [s * 0.2, s * 0.25, s * 0.8, s * 0.85], BROWN, INK)
    _ellipse(d, [s * 0.38, s * 0.48, s * 0.46, s * 0.56], BLACK)
    _ellipse(d, [s * 0.54, s * 0.48, s * 0.62, s * 0.56], BLACK)
    return img


# --- Garden ---

def icon_seed(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.35, s * 0.4, s * 0.65, s * 0.7], BROWN, INK)
    return img


def icon_soil(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.1, s * 0.45, s * 0.9, s * 0.85], BROWN, INK)
    for i in range(6):
        _ellipse(d, [s * (0.2 + i * 0.1), s * 0.55, s * (0.28 + i * 0.1), s * 0.65], "#5d4037")
    return img


def icon_shovel(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.45, s * 0.1, s * 0.55, s * 0.55], BROWN, INK)
    _polygon(d, [(s * 0.35, s * 0.55), (s * 0.65, s * 0.55), (s * 0.58, s * 0.9), (s * 0.42, s * 0.9)], GRAY, INK)
    return img


def icon_watering_can(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.25, s * 0.4, s * 0.7, s * 0.75], SKY, INK)
    _line(d, [(s * 0.7, s * 0.5), (s * 0.9, s * 0.35)], SKY, 8)
    _ellipse(d, [s * 0.2, s * 0.35, s * 0.4, s * 0.55], SKY, INK)
    return img


def icon_dig(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.1, s * 0.55, s * 0.9, s * 0.85], BROWN, INK)
    _polygon(d, [(s * 0.4, s * 0.55), (s * 0.6, s * 0.55), (s * 0.7, s * 0.35), (s * 0.3, s * 0.35)], "#a1887f")
    return img


def icon_plant(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.35, s * 0.55, s * 0.65, s * 0.9], BROWN, INK)
    _ellipse(d, [s * 0.3, s * 0.25, s * 0.5, s * 0.5], LEAF, INK)
    _ellipse(d, [s * 0.5, s * 0.2, s * 0.7, s * 0.45], LEAF, INK)
    _line(d, [(s * 0.5, s * 0.55), (s * 0.5, s * 0.3)], DARK_GREEN, 4)
    return img


def icon_water(size=256):
    img, d = blank(size)
    s = size
    for i, x in enumerate([0.3, 0.5, 0.7]):
        _ellipse(d, [s * (x - 0.08), s * (0.25 + i * 0.05), s * (x + 0.08), s * (0.45 + i * 0.05)], SKY)
    _ellipse(d, [s * 0.25, s * 0.55, s * 0.75, s * 0.85], LIGHT_BLUE, SKY)
    return img


def icon_sunlight(size=256):
    img, d = blank(size)
    s = size
    cx, cy, r = s / 2, s / 2, s * 0.22
    _ellipse(d, [cx - r, cy - r, cx + r, cy + r], SUN, ORANGE)
    for i in range(8):
        a = i * math.pi / 4
        _line(
            d,
            [
                (cx + math.cos(a) * r * 1.3, cy + math.sin(a) * r * 1.3),
                (cx + math.cos(a) * r * 1.9, cy + math.sin(a) * r * 1.9),
            ],
            SUN,
            6,
        )
    return img


def icon_roots(size=256):
    img, d = blank(size)
    s = size
    _line(d, [(s * 0.5, s * 0.15), (s * 0.5, s * 0.45)], BROWN, 5)
    _line(d, [(s * 0.5, s * 0.45), (s * 0.3, s * 0.8)], BROWN, 4)
    _line(d, [(s * 0.5, s * 0.45), (s * 0.7, s * 0.8)], BROWN, 4)
    _line(d, [(s * 0.5, s * 0.5), (s * 0.5, s * 0.85)], BROWN, 4)
    return img


def icon_sprout(size=256):
    img, d = blank(size)
    s = size
    _line(d, [(s * 0.5, s * 0.85), (s * 0.5, s * 0.4)], LEAF, 5)
    _ellipse(d, [s * 0.28, s * 0.25, s * 0.5, s * 0.45], LEAF, INK)
    _ellipse(d, [s * 0.5, s * 0.2, s * 0.72, s * 0.4], LEAF, INK)
    return img


def icon_flower(size=256):
    img, d = blank(size)
    s = size
    cx, cy = s / 2, s * 0.4
    for i in range(6):
        a = i * math.pi / 3
        _ellipse(
            d,
            [cx + math.cos(a) * s * 0.18 - s * 0.1, cy + math.sin(a) * s * 0.18 - s * 0.1,
             cx + math.cos(a) * s * 0.18 + s * 0.1, cy + math.sin(a) * s * 0.18 + s * 0.1],
            PINK,
            BERRY,
        )
    _ellipse(d, [cx - s * 0.08, cy - s * 0.08, cx + s * 0.08, cy + s * 0.08], SUN)
    _line(d, [(cx, cy + s * 0.1), (cx, s * 0.9)], LEAF, 5)
    return img


def icon_bee(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.25, s * 0.35, s * 0.75, s * 0.7], SUN, INK)
    _rect(d, [s * 0.4, s * 0.35, s * 0.48, s * 0.7], BLACK)
    _rect(d, [s * 0.55, s * 0.35, s * 0.63, s * 0.7], BLACK)
    _ellipse(d, [s * 0.35, s * 0.2, s * 0.55, s * 0.4], WHITE, INK)
    _ellipse(d, [s * 0.5, s * 0.18, s * 0.7, s * 0.38], WHITE, INK)
    return img


def icon_worm(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.45, s * 0.8, s * 0.65], PINK, INK)
    _ellipse(d, [s * 0.65, s * 0.48, s * 0.72, s * 0.55], BLACK)
    return img


def icon_ladybug(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.3, s * 0.8, s * 0.8], RED, INK)
    _ellipse(d, [s * 0.35, s * 0.18, s * 0.65, s * 0.4], BLACK)
    for x, y in [(0.35, 0.45), (0.55, 0.45), (0.4, 0.6), (0.6, 0.6)]:
        _ellipse(d, [s * x, s * y, s * (x + 0.1), s * (y + 0.1)], BLACK)
    _line(d, [(s * 0.5, s * 0.3), (s * 0.5, s * 0.8)], BLACK, 3)
    return img


def icon_butterfly(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.1, s * 0.25, s * 0.5, s * 0.65], GRAPE, INK)
    _ellipse(d, [s * 0.5, s * 0.25, s * 0.9, s * 0.65], SKY, INK)
    _ellipse(d, [s * 0.42, s * 0.35, s * 0.58, s * 0.75], BLACK)
    return img


def icon_tomato(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.22, s * 0.3, s * 0.78, s * 0.85], RED, INK)
    _polygon(d, [(s * 0.5, s * 0.2), (s * 0.4, s * 0.35), (s * 0.6, s * 0.35)], LEAF)
    return img


def icon_carrot(size=256):
    img, d = blank(size)
    s = size
    _polygon(d, [(s * 0.5, s * 0.85), (s * 0.3, s * 0.3), (s * 0.7, s * 0.3)], ORANGE, INK)
    _ellipse(d, [s * 0.35, s * 0.12, s * 0.5, s * 0.32], LEAF)
    _ellipse(d, [s * 0.5, s * 0.1, s * 0.65, s * 0.3], LEAF)
    return img


def icon_sunflower(size=256):
    img, d = blank(size)
    s = size
    cx, cy = s / 2, s * 0.4
    for i in range(10):
        a = i * math.pi / 5
        _ellipse(
            d,
            [cx + math.cos(a) * s * 0.22 - s * 0.08, cy + math.sin(a) * s * 0.22 - s * 0.08,
             cx + math.cos(a) * s * 0.22 + s * 0.08, cy + math.sin(a) * s * 0.22 + s * 0.08],
            SUN,
            ORANGE,
        )
    _ellipse(d, [cx - s * 0.12, cy - s * 0.12, cx + s * 0.12, cy + s * 0.12], BROWN)
    _line(d, [(cx, cy + s * 0.15), (cx, s * 0.9)], LEAF, 6)
    return img


# --- Shapes ---

def icon_circle(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.15, s * 0.85, s * 0.85], SKY, INK, 4)
    return img


def icon_square(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.18, s * 0.18, s * 0.82, s * 0.82], BERRY, INK, 4)
    return img


def icon_triangle(size=256):
    img, d = blank(size)
    s = size
    _polygon(d, [(s * 0.5, s * 0.15), (s * 0.15, s * 0.85), (s * 0.85, s * 0.85)], LEAF, INK, 4)
    return img


def icon_rectangle(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.12, s * 0.3, s * 0.88, s * 0.7], GRAPE, INK, 4)
    return img


def icon_star(size=256):
    img, d = blank(size)
    s = size
    _polygon(d, _star_points(s / 2, s / 2, s * 0.4, s * 0.18), SUN, ORANGE, 3)
    return img


def icon_heart(size=256):
    img, d = blank(size)
    s = size
    _polygon(d, _heart_points(s / 2, s * 0.45, s * 0.4), BERRY, INK, 3)
    return img


def icon_plate(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.1, s * 0.15, s * 0.9, s * 0.85], WHITE, GRAY, 4)
    _ellipse(d, [s * 0.25, s * 0.3, s * 0.75, s * 0.7], CREAM, GRAY, 2)
    return img


def icon_clock(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.12, s * 0.12, s * 0.88, s * 0.88], WHITE, INK, 4)
    _line(d, [(s / 2, s / 2), (s / 2, s * 0.28)], INK, 5)
    _line(d, [(s / 2, s / 2), (s * 0.7, s / 2)], INK, 5)
    return img


def icon_cracker(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.2, s * 0.2, s * 0.8, s * 0.8], SUN, BROWN, 3)
    for i in range(3):
        for j in range(3):
            x, y = s * (0.32 + i * 0.15), s * (0.32 + j * 0.15)
            _ellipse(d, [x, y, x + s * 0.06, y + s * 0.06], BROWN)
    return img


def icon_block(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.2, s * 0.35, s * 0.7, s * 0.85], RED, INK, 3)
    _polygon(d, [(s * 0.2, s * 0.35), (s * 0.35, s * 0.2), (s * 0.85, s * 0.2), (s * 0.7, s * 0.35)], "#ef5350", INK)
    _polygon(d, [(s * 0.7, s * 0.35), (s * 0.85, s * 0.2), (s * 0.85, s * 0.7), (s * 0.7, s * 0.85)], "#c62828", INK)
    return img


def icon_sandwich(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.15, s * 0.3, s * 0.85, s * 0.42], SUN, BROWN)
    _rect(d, [s * 0.18, s * 0.42, s * 0.82, s * 0.52], LEAF)
    _rect(d, [s * 0.18, s * 0.52, s * 0.82, s * 0.62], RED)
    _rect(d, [s * 0.15, s * 0.62, s * 0.85, s * 0.74], SUN, BROWN)
    return img


def icon_flag(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.25, s * 0.15, s * 0.32, s * 0.9], BROWN, INK)
    _polygon(d, [(s * 0.32, s * 0.15), (s * 0.85, s * 0.35), (s * 0.32, s * 0.55)], BERRY, INK)
    return img


def icon_door(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.25, s * 0.1, s * 0.75, s * 0.9], BROWN, INK, 3)
    _ellipse(d, [s * 0.58, s * 0.48, s * 0.68, s * 0.58], SUN)
    return img


def icon_book(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.2, s * 0.2, s * 0.8, s * 0.85], SKY, INK, 3)
    _rect(d, [s * 0.2, s * 0.2, s * 0.32, s * 0.85], "#1565c0")
    _line(d, [(s * 0.4, s * 0.4), (s * 0.7, s * 0.4)], WHITE, 3)
    _line(d, [(s * 0.4, s * 0.55), (s * 0.7, s * 0.55)], WHITE, 3)
    return img


def icon_rug(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.1, s * 0.25, s * 0.9, s * 0.75], BERRY, INK, 3)
    _rect(d, [s * 0.2, s * 0.35, s * 0.8, s * 0.65], SUN)
    return img


def icon_cookie(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.15, s * 0.85, s * 0.85], BROWN, INK)
    for x, y in [(0.35, 0.35), (0.55, 0.4), (0.4, 0.55), (0.6, 0.6), (0.45, 0.7)]:
        _ellipse(d, [s * x, s * y, s * (x + 0.08), s * (y + 0.08)], "#3e2723")
    return img


# --- Numbers ---

def _ball_at(d, cx, cy, item, color=RED):
    r = item / 2
    _ellipse(d, [cx - r, cy - r, cx + r, cy + r], color, INK)


def icon_ball(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.2, s * 0.8, s * 0.8], RED, INK)
    _line(d, [(s * 0.2, s * 0.5), (s * 0.8, s * 0.5)], WHITE, 3)
    _line(d, [(s * 0.5, s * 0.2), (s * 0.5, s * 0.8)], WHITE, 3)
    return img


def icon_number_word(word: str, size=256):
    counts = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    n = counts[word]

    def draw_one(d, cx, cy, item):
        _ball_at(d, cx, cy, item, RED)

    return _count_items(draw_one, n, size)


def icon_cats(size=256):
    def draw_one(d, cx, cy, item):
        r = item / 2
        _ellipse(d, [cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], ORANGE, INK)
        _ellipse(d, [cx - r * 0.5, cy - r, cx - r * 0.1, cy - r * 0.5], ORANGE)
        _ellipse(d, [cx + r * 0.1, cy - r, cx + r * 0.5, cy - r * 0.5], ORANGE)

    return _count_items(draw_one, 3, size)


def icon_cookies(size=256):
    def draw_one(d, cx, cy, item):
        r = item / 2
        _ellipse(d, [cx - r, cy - r, cx + r, cy + r], BROWN, INK)

    return _count_items(draw_one, 4, size)


def icon_cups(size=256):
    def draw_one(d, cx, cy, item):
        w, h = item * 0.6, item * 0.8
        _polygon(d, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2),
                     (cx + w / 3, cy + h / 2), (cx - w / 3, cy + h / 2)], SKY, INK)

    return _count_items(draw_one, 3, size)


def icon_tomatoes(size=256):
    def draw_one(d, cx, cy, item):
        r = item / 2
        _ellipse(d, [cx - r, cy - r, cx + r, cy + r], RED, INK)

    return _count_items(draw_one, 5, size)


def icon_ducks(size=256):
    def draw_one(d, cx, cy, item):
        r = item / 2
        _ellipse(d, [cx - r, cy - r * 0.4, cx + r * 0.5, cy + r * 0.5], SUN, INK)
        _ellipse(d, [cx + r * 0.2, cy - r * 0.8, cx + r, cy - r * 0.1], SUN, INK)
        _polygon(d, [(cx + r, cy - r * 0.5), (cx + r * 1.4, cy - r * 0.4), (cx + r, cy - r * 0.3)], ORANGE)

    return _count_items(draw_one, 2, size)


def icon_steps(size=256):
    img, d = blank(size)
    s = size
    for i in range(4):
        _rect(d, [s * (0.15 + i * 0.05), s * (0.7 - i * 0.15), s * 0.85, s * (0.85 - i * 0.15)], GRAY, INK)
    return img


def icon_walk(size=256):
    img, d = blank(size)
    s = size
    # simple footprints
    for i, (x, y) in enumerate([(0.3, 0.6), (0.45, 0.45), (0.6, 0.6), (0.75, 0.45)]):
        _ellipse(d, [s * x, s * y, s * (x + 0.12), s * (y + 0.2)], BROWN, INK)
    return img


def icon_count(size=256):
    img, d = blank(size)
    s = size
    for i, n in enumerate("123"):
        # draw dots
        _ellipse(d, [s * (0.2 + i * 0.25), s * 0.35, s * (0.35 + i * 0.25), s * 0.55], SKY, INK)
    return img


# --- Colors ---

def icon_color_swatch(color: str, size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.15, s * 0.85, s * 0.85], color, INK, 4)
    return img


def icon_yarn(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.2, s * 0.8, s * 0.8], BERRY, INK)
    for i in range(4):
        _ellipse(d, [s * 0.25, s * (0.3 + i * 0.1), s * 0.75, s * (0.4 + i * 0.1)], None if False else BERRY)
        d.arc([s * 0.25, s * (0.25 + i * 0.1), s * 0.75, s * (0.55 + i * 0.1)], 0, 180, fill=_hex(INK) + (255,), width=3)
    return img


def icon_banana(size=256):
    img, d = blank(size)
    s = size
    _polygon(
        d,
        [(s * 0.2, s * 0.35), (s * 0.35, s * 0.2), (s * 0.8, s * 0.55), (s * 0.7, s * 0.75), (s * 0.3, s * 0.55)],
        YELLOW,
        INK,
    )
    return img


def icon_orange_fruit(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.2, s * 0.85, s * 0.9], ORANGE, INK, 3)
    _ellipse(d, [s * 0.45, s * 0.12, s * 0.6, s * 0.25], LEAF)
    # highlight so it's clearly fruit not color swatch
    _ellipse(d, [s * 0.3, s * 0.35, s * 0.45, s * 0.5], "#ffb74d")
    return img


def icon_boots(size=256):
    img, d = blank(size)
    s = size
    for x in (0.2, 0.55):
        _rect(d, [s * x, s * 0.25, s * (x + 0.25), s * 0.7], RED, INK)
        _rect(d, [s * x, s * 0.65, s * (x + 0.35), s * 0.85], RED, INK)
    return img


def icon_grass(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.05, s * 0.55, s * 0.95, s * 0.9], LEAF, DARK_GREEN)
    for i in range(8):
        x = s * (0.1 + i * 0.1)
        _polygon(d, [(x, s * 0.55), (x + s * 0.04, s * 0.25), (x + s * 0.08, s * 0.55)], LEAF)
    return img


def icon_blanket(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.1, s * 0.2, s * 0.9, s * 0.8], GRAPE, INK, 3)
    for i in range(3):
        for j in range(3):
            if (i + j) % 2 == 0:
                _rect(
                    d,
                    [s * (0.15 + i * 0.25), s * (0.28 + j * 0.18), s * (0.35 + i * 0.25), s * (0.42 + j * 0.18)],
                    SKY,
                )
    return img


def icon_picnic(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.1, s * 0.4, s * 0.9, s * 0.85], RED, INK)
    for i in range(4):
        for j in range(3):
            if (i + j) % 2:
                _rect(
                    d,
                    [s * (0.1 + i * 0.2), s * (0.4 + j * 0.15), s * (0.3 + i * 0.2), s * (0.55 + j * 0.15)],
                    WHITE,
                )
    _ellipse(d, [s * 0.35, s * 0.2, s * 0.65, s * 0.45], BROWN)  # basket hint
    return img


# --- Snow / winter ---

def icon_snow(size=256):
    img, d = blank(size)
    s = size
    for x, y, r in [(0.3, 0.3, 0.08), (0.6, 0.25, 0.1), (0.45, 0.5, 0.09), (0.25, 0.65, 0.07), (0.7, 0.6, 0.1)]:
        _ellipse(d, [s * (x - r), s * (y - r), s * (x + r), s * (y + r)], LIGHT_BLUE, SKY)
    return img


def icon_snowflake(size=256):
    img, d = blank(size)
    s = size
    cx, cy = s / 2, s / 2
    for i in range(6):
        a = i * math.pi / 3
        x2, y2 = cx + math.cos(a) * s * 0.4, cy + math.sin(a) * s * 0.4
        _line(d, [(cx, cy), (x2, y2)], SKY, 5)
        _line(d, [(cx + math.cos(a) * s * 0.25, cy + math.sin(a) * s * 0.25),
                  (cx + math.cos(a + 0.4) * s * 0.35, cy + math.sin(a + 0.4) * s * 0.35)], SKY, 3)
    return img


def icon_snowman(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.28, s * 0.55, s * 0.72, s * 0.95], WHITE, INK)
    _ellipse(d, [s * 0.32, s * 0.3, s * 0.68, s * 0.65], WHITE, INK)
    _ellipse(d, [s * 0.38, s * 0.1, s * 0.62, s * 0.38], WHITE, INK)
    _ellipse(d, [s * 0.44, s * 0.2, s * 0.48, s * 0.24], BLACK)
    _ellipse(d, [s * 0.52, s * 0.2, s * 0.56, s * 0.24], BLACK)
    _polygon(d, [(s * 0.5, s * 0.26), (s * 0.65, s * 0.28), (s * 0.5, s * 0.3)], ORANGE)
    # winter hat
    _rect(d, [s * 0.36, s * 0.02, s * 0.64, s * 0.14], RED, INK)
    _rect(d, [s * 0.3, s * 0.12, s * 0.7, s * 0.18], RED, INK)
    return img


def icon_snowball(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.2, s * 0.2, s * 0.8, s * 0.8], WHITE, SKY, 3)
    return img


def icon_cold(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.35, s * 0.15, s * 0.65, s * 0.7], LIGHT_BLUE, SKY)
    _ellipse(d, [s * 0.3, s * 0.6, s * 0.7, s * 0.9], SKY, INK)
    # frost marks
    _line(d, [(s * 0.4, s * 0.3), (s * 0.45, s * 0.4)], WHITE, 3)
    return img


def icon_warm(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.25, s * 0.25, s * 0.75, s * 0.75], SUN, ORANGE)
    for i in range(8):
        a = i * math.pi / 4
        _line(d, [(s / 2 + math.cos(a) * s * 0.3, s / 2 + math.sin(a) * s * 0.3),
                  (s / 2 + math.cos(a) * s * 0.42, s / 2 + math.sin(a) * s * 0.42)], ORANGE, 5)
    return img


def icon_hat(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.25, s * 0.35, s * 0.75, s * 0.7], BERRY, INK)
    _rect(d, [s * 0.15, s * 0.6, s * 0.85, s * 0.75], BERRY, INK)
    _ellipse(d, [s * 0.42, s * 0.2, s * 0.58, s * 0.4], WHITE)
    return img


def icon_scarf(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.2, s * 0.25, s * 0.8, s * 0.45], LEAF, INK)
    _rect(d, [s * 0.55, s * 0.4, s * 0.75, s * 0.85], LEAF, INK)
    for y in range(3):
        _line(d, [(s * 0.55, s * (0.7 + y * 0.05)), (s * 0.75, s * (0.7 + y * 0.05))], DARK_GREEN, 2)
    return img


def icon_gloves(size=256):
    img, d = blank(size)
    s = size
    for x in (0.15, 0.55):
        _ellipse(d, [s * x, s * 0.35, s * (x + 0.3), s * 0.8], SKY, INK)
        _ellipse(d, [s * (x + 0.18), s * 0.22, s * (x + 0.32), s * 0.42], SKY, INK)
    return img


def icon_coat(size=256):
    img, d = blank(size)
    s = size
    _polygon(
        d,
        [(s * 0.25, s * 0.2), (s * 0.75, s * 0.2), (s * 0.85, s * 0.85), (s * 0.15, s * 0.85)],
        "#1565c0",
        INK,
    )
    _line(d, [(s * 0.5, s * 0.2), (s * 0.5, s * 0.85)], INK, 3)
    _ellipse(d, [s * 0.42, s * 0.45, s * 0.48, s * 0.51], SUN)
    return img


def icon_winter(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.15, s * 0.55, s * 0.85, s * 0.9], WHITE, SKY)
    _polygon(d, [(s * 0.5, s * 0.15), (s * 0.2, s * 0.6), (s * 0.8, s * 0.6)], "#90caf9", SKY)
    return img


def icon_window(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.15, s * 0.15, s * 0.85, s * 0.85], LIGHT_BLUE, BROWN, 5)
    _line(d, [(s * 0.5, s * 0.15), (s * 0.5, s * 0.85)], BROWN, 5)
    _line(d, [(s * 0.15, s * 0.5), (s * 0.85, s * 0.5)], BROWN, 5)
    return img


def icon_ice(size=256):
    img, d = blank(size)
    s = size
    _polygon(d, [(s * 0.5, s * 0.1), (s * 0.85, s * 0.5), (s * 0.5, s * 0.9), (s * 0.15, s * 0.5)], LIGHT_BLUE, SKY, 3)
    return img


# --- Christmas ---

def icon_tree(size=256):
    img, d = blank(size)
    s = size
    _polygon(d, [(s * 0.5, s * 0.1), (s * 0.2, s * 0.45), (s * 0.8, s * 0.45)], LEAF, INK)
    _polygon(d, [(s * 0.5, s * 0.3), (s * 0.15, s * 0.65), (s * 0.85, s * 0.65)], LEAF, INK)
    _polygon(d, [(s * 0.5, s * 0.5), (s * 0.1, s * 0.85), (s * 0.9, s * 0.85)], LEAF, INK)
    _rect(d, [s * 0.42, s * 0.85, s * 0.58, s * 0.95], BROWN)
    return img


def icon_wreath(size=256):
    img2, d2 = blank(size)
    s = size
    _ellipse(d2, [s * 0.15, s * 0.2, s * 0.85, s * 0.9], LEAF, DARK_GREEN, 4)
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([s * 0.32, s * 0.37, s * 0.68, s * 0.73], fill=255)
    clear = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    img2.paste(clear, mask=mask)
    d2 = ImageDraw.Draw(img2)
    _polygon(d2, [(s * 0.45, s * 0.15), (s * 0.55, s * 0.15), (s * 0.5, s * 0.28)], BERRY)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        cx = s / 2 + math.cos(rad) * s * 0.28
        cy = s * 0.55 + math.sin(rad) * s * 0.28
        _ellipse(d2, [cx - 6, cy - 6, cx + 6, cy + 6], RED)
    return img2


def icon_stocking(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.35, s * 0.15, s * 0.65, s * 0.55], RED, INK)
    _rect(d, [s * 0.35, s * 0.15, s * 0.65, s * 0.28], WHITE, INK)
    _ellipse(d, [s * 0.35, s * 0.45, s * 0.85, s * 0.85], RED, INK)
    return img


def icon_lights(size=256):
    img, d = blank(size)
    s = size
    colors = [RED, SUN, LEAF, SKY, GRAPE, BERRY]
    _line(d, [(s * 0.1, s * 0.3), (s * 0.9, s * 0.5)], LEAF, 3)
    for i, c in enumerate(colors):
        x = s * (0.15 + i * 0.12)
        y = s * (0.35 + (i % 2) * 0.15)
        _ellipse(d, [x, y, x + s * 0.1, y + s * 0.14], c, INK)
    return img


def icon_bell(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.25, s * 0.25, s * 0.75, s * 0.75], SUN, ORANGE)
    _rect(d, [s * 0.2, s * 0.65, s * 0.8, s * 0.78], SUN, ORANGE)
    _ellipse(d, [s * 0.45, s * 0.75, s * 0.55, s * 0.88], ORANGE)
    _ellipse(d, [s * 0.42, s * 0.12, s * 0.58, s * 0.28], GRAY)
    return img


def icon_ornament(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.25, s * 0.3, s * 0.75, s * 0.85], BERRY, INK)
    _rect(d, [s * 0.42, s * 0.18, s * 0.58, s * 0.32], SUN, INK)
    _ellipse(d, [s * 0.35, s * 0.45, s * 0.5, s * 0.6], "#f48fb1")
    return img


def icon_candy_cane(size=256):
    img, d = blank(size)
    s = size
    # curved cane approximated with thick arcs/rects
    _ellipse(d, [s * 0.3, s * 0.15, s * 0.7, s * 0.5], WHITE, RED, 12)
    # clear lower left of ellipse
    d.rectangle([s * 0.3, s * 0.35, s * 0.5, s * 0.5], fill=(0, 0, 0, 0))
    _rect(d, [s * 0.55, s * 0.35, s * 0.68, s * 0.9], WHITE, RED, 3)
    for i in range(5):
        y = s * (0.4 + i * 0.1)
        _line(d, [(s * 0.55, y), (s * 0.68, y + s * 0.04)], RED, 5)
    return img


def icon_reindeer(size=256):
    img, d = blank(size)
    s = size
    _ellipse(d, [s * 0.3, s * 0.4, s * 0.7, s * 0.8], BROWN, INK)
    _ellipse(d, [s * 0.35, s * 0.25, s * 0.65, s * 0.5], BROWN, INK)
    _ellipse(d, [s * 0.45, s * 0.38, s * 0.55, s * 0.48], RED)  # nose
    _line(d, [(s * 0.4, s * 0.3), (s * 0.25, s * 0.1)], BROWN, 4)
    _line(d, [(s * 0.6, s * 0.3), (s * 0.75, s * 0.1)], BROWN, 4)
    return img


def icon_present(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.2, s * 0.35, s * 0.8, s * 0.85], BERRY, INK, 3)
    _rect(d, [s * 0.45, s * 0.35, s * 0.55, s * 0.85], SUN)
    _rect(d, [s * 0.2, s * 0.55, s * 0.8, s * 0.65], SUN)
    _polygon(d, [(s * 0.5, s * 0.2), (s * 0.35, s * 0.35), (s * 0.65, s * 0.35)], SUN)
    return img


def icon_candle(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.4, s * 0.35, s * 0.6, s * 0.85], CREAM, INK)
    _ellipse(d, [s * 0.42, s * 0.15, s * 0.58, s * 0.4], SUN, ORANGE)
    _rect(d, [s * 0.3, s * 0.8, s * 0.7, s * 0.9], RED, INK)
    return img


def icon_card(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.2, s * 0.2, s * 0.8, s * 0.8], WHITE, BERRY, 4)
    _polygon(d, _heart_points(s / 2, s * 0.5, s * 0.2), BERRY)
    return img


def icon_box(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.2, s * 0.4, s * 0.8, s * 0.85], TAN, INK, 3)
    _polygon(d, [(s * 0.2, s * 0.4), (s * 0.35, s * 0.25), (s * 0.95, s * 0.25), (s * 0.8, s * 0.4)], "#bcaaa4", INK)
    return img


def icon_ribbon(size=256):
    img, d = blank(size)
    s = size
    _rect(d, [s * 0.15, s * 0.4, s * 0.85, s * 0.55], BERRY, INK)
    _ellipse(d, [s * 0.35, s * 0.25, s * 0.5, s * 0.45], BERRY)
    _ellipse(d, [s * 0.5, s * 0.25, s * 0.65, s * 0.45], BERRY)
    return img


def icon_bow(size=256):
    img, d = blank(size)
    s = size
    _polygon(d, [(s * 0.5, s * 0.5), (s * 0.15, s * 0.25), (s * 0.15, s * 0.75)], BERRY, INK)
    _polygon(d, [(s * 0.5, s * 0.5), (s * 0.85, s * 0.25), (s * 0.85, s * 0.75)], BERRY, INK)
    _ellipse(d, [s * 0.4, s * 0.4, s * 0.6, s * 0.6], SUN)
    return img


ICON_MAP = {
    "elephant": icon_elephant,
    "giraffe": icon_giraffe,
    "zebra": icon_zebra,
    "lion": icon_lion,
    "tiger": icon_tiger,
    "cheetah": icon_cheetah,
    "gorilla": icon_gorilla,
    "penguin": icon_penguin,
    "hippo": icon_hippo,
    "rhino": icon_rhino,
    "panda": icon_panda,
    "koala": icon_koala,
    "kangaroo": icon_kangaroo,
    "flamingo": icon_flamingo,
    "bear": icon_bear,
    "seed": icon_seed,
    "soil": icon_soil,
    "shovel": icon_shovel,
    "watering can": icon_watering_can,
    "dig": icon_dig,
    "plant": icon_plant,
    "water": icon_water,
    "sunlight": icon_sunlight,
    "roots": icon_roots,
    "sprout": icon_sprout,
    "flower": icon_flower,
    "bee": icon_bee,
    "worm": icon_worm,
    "ladybug": icon_ladybug,
    "butterfly": icon_butterfly,
    "tomato": icon_tomato,
    "carrot": icon_carrot,
    "sunflower": icon_sunflower,
    "circle": icon_circle,
    "square": icon_square,
    "triangle": icon_triangle,
    "rectangle": icon_rectangle,
    "star": icon_star,
    "heart": icon_heart,
    "plate": icon_plate,
    "clock": icon_clock,
    "cracker": icon_cracker,
    "block": icon_block,
    "sandwich": icon_sandwich,
    "flag": icon_flag,
    "door": icon_door,
    "book": icon_book,
    "rug": icon_rug,
    "cookie": icon_cookie,
    "one": lambda s=256: icon_number_word("one", s),
    "two": lambda s=256: icon_number_word("two", s),
    "three": lambda s=256: icon_number_word("three", s),
    "four": lambda s=256: icon_number_word("four", s),
    "five": lambda s=256: icon_number_word("five", s),
    "ball": icon_ball,
    "cats": icon_cats,
    "cookies": icon_cookies,
    "cups": icon_cups,
    "tomatoes": icon_tomatoes,
    "ducks": icon_ducks,
    "steps": icon_steps,
    "walk": icon_walk,
    "count": icon_count,
    "red": lambda s=256: icon_color_swatch(RED, s),
    "blue": lambda s=256: icon_color_swatch(BLUE, s),
    "yellow": lambda s=256: icon_color_swatch(YELLOW, s),
    "orange": lambda s=256: icon_color_swatch(ORANGE, s),
    "green": lambda s=256: icon_color_swatch(GREEN, s),
    "purple": lambda s=256: icon_color_swatch(PURPLE, s),
    "yarn": icon_yarn,
    "banana": icon_banana,
    "orange fruit": icon_orange_fruit,
    "boots": icon_boots,
    "grass": icon_grass,
    "blanket": icon_blanket,
    "picnic": icon_picnic,
    "snow": icon_snow,
    "snowflake": icon_snowflake,
    "snowman": icon_snowman,
    "snowball": icon_snowball,
    "cold": icon_cold,
    "warm": icon_warm,
    "hat": icon_hat,
    "scarf": icon_scarf,
    "gloves": icon_gloves,
    "coat": icon_coat,
    "winter": icon_winter,
    "window": icon_window,
    "ice": icon_ice,
    "tree": icon_tree,
    "wreath": icon_wreath,
    "stocking": icon_stocking,
    "lights": icon_lights,
    "bell": icon_bell,
    "ornament": icon_ornament,
    "candy cane": icon_candy_cane,
    "reindeer": icon_reindeer,
    "present": icon_present,
    "candle": icon_candle,
    "card": icon_card,
    "box": icon_box,
    "ribbon": icon_ribbon,
    "bow": icon_bow,
}


def get_icon(word: str, size: int = 256) -> Image.Image:
    key = word.strip().lower()
    fn = ICON_MAP.get(key)
    if fn is None:
        # fallback: labeled circle
        img, d = blank(size)
        _ellipse(d, [size * 0.15, size * 0.15, size * 0.85, size * 0.85], SKY, INK)
        return img
    return fn(size)
