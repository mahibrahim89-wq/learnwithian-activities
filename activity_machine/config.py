"""Brand colors, fonts, paths, and page sizes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARACTERS_DIR = ROOT / "characters"
FONTS_DIR = ROOT / "fonts"
ICONS_DIR = ROOT / "icons"
OUTPUT_DIR = ROOT / "output"
EPISODES_JSON = ROOT / "episodes.json"

# Brand colors (learnwithian.com)
PAPER = "#fff9ef"
INK = "#1d2b45"
BERRY = "#ec4f7b"
SUN = "#ffb321"
LEAF = "#3fae5a"
SKY = "#2f8fe6"
GRAPE = "#8e5ce6"
CARD_BORDER = "#ecdcbc"

RAINBOW = [BERRY, SUN, LEAF, SKY, GRAPE]

FONT_HEADING = str(FONTS_DIR / "Baloo2-ExtraBold.ttf")
FONT_BODY = str(FONTS_DIR / "AtkinsonHyperlegible-Regular.ttf")
FONT_BODY_BOLD = str(FONTS_DIR / "AtkinsonHyperlegible-Bold.ttf")

# Page sizes in points (1 inch = 72 pt)
LETTER = (612.0, 792.0)  # 8.5 x 11 in
A4 = (595.28, 841.89)  # 210 x 297 mm
LETTER_MARGIN = 36.0  # 0.5 inch
A4_MARGIN = 36.0  # 12.7 mm ≈ 36 pt

CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1oxDQWj9UmokHvhHp05L9GPgZxyOlyMZ3ctli8nORgsc/export?format=csv"
)

CHARACTER_FILES = {
    "ian": "ian.png",
    "mama_sana": "mama_sana.png",
    "papa": "papa.png",
    "liam": "liam.png",
    "latte": "latte.png",
    "lisa": "lisa.png",
    "lorie": "lorie.png",
}

# At most one full character per page (corner). Chosen by episode theme.
EPISODE_CHARACTER = {
    1: "ian",
    2: "ian",
    3: "liam",
    4: "ian",
    5: "lisa",
    6: "papa",
    7: "mama_sana",
}
