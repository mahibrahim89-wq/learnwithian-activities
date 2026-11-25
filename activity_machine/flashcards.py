"""Word flashcards PDF generator."""

from __future__ import annotations

import io
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics

from .config import CARD_BORDER, INK, PAPER, WORD_CHARACTERS
from .icons import get_icon, to_bytes
from .pdf_common import (
    draw_character_proportional,
    draw_cut_line,
    draw_episode_line,
    draw_footer,
    draw_title,
    draw_wordmark,
    fill_paper,
    image_reader_from_png_bytes,
    make_canvas,
    rounded_card,
)


def _activity_title(episode_title: str) -> str:
    short = episode_title.replace("Ian's ", "").replace("Ian’s ", "")
    return f"Free {short} Word Flashcards"


def build_flashcards_pdf(
    out_path: Path,
    episode,
    size_name: str,
    qr_cache: dict | None = None,
    placements: list | None = None,
) -> int:
    words = list(episode.words)
    c, width, height, margin = make_canvas(out_path, size_name)
    footer_top = margin + 0.85 * inch + 8
    top = height - margin

    cols, rows = 2, 3
    cards_per_page = cols * rows
    pages = 0
    idx = 0

    while idx < len(words) or pages == 0:
        fill_paper(c, width, height)
        y = draw_wordmark(c, width, height, margin)
        y -= 6
        if pages == 0:
            y = draw_title(c, width, y - 10, _activity_title(episode.title), 20)
            y = draw_episode_line(c, width, y, episode.title)
        else:
            y = draw_title(c, width, y - 6, "Word Flashcards (continued)", 16)

        usable_top = y - 8
        usable_bottom = footer_top + 4
        usable_h = usable_top - usable_bottom
        usable_w = width - 2 * margin
        card_w = usable_w / cols
        card_h = usable_h / rows

        for r in range(rows):
            for col in range(cols):
                if idx >= len(words):
                    break
                word = words[idx]
                idx += 1
                x0 = margin + col * card_w
                y0 = usable_bottom + (rows - 1 - r) * card_h
                pad = 6
                rounded_card(c, x0 + pad, y0 + pad, card_w - 2 * pad, card_h - 2 * pad)

                # icon
                icon = get_icon(word, 256)
                icon_buf = image_reader_from_png_bytes(to_bytes(icon))
                icon_size = min(card_w, card_h) * 0.42
                ix = x0 + (card_w - icon_size) / 2
                iy = y0 + card_h * 0.38
                c.drawImage(icon_buf, ix, iy, icon_size, icon_size, mask="auto")

                # character sometimes
                ch = WORD_CHARACTERS.get(word.lower())
                if ch:
                    draw_character_proportional(
                        c, ch, x0 + pad + 4, y0 + pad + 4, card_w * 0.28, card_h * 0.35, placements
                    )

                # word label
                c.setFillColor(HexColor(INK))
                font_size = 16 if len(word) < 12 else 13
                c.setFont("Baloo2", font_size)
                c.drawCentredString(x0 + card_w / 2, y0 + pad + 14, word)

                # cut lines between cards
                if col < cols - 1:
                    draw_cut_line(c, x0 + card_w, y0 + 4, x0 + card_w, y0 + card_h - 4)
                if r < rows - 1:
                    draw_cut_line(c, x0 + 4, y0, x0 + card_w - 4, y0)

        draw_footer(c, width, height, margin, episode.youtube_url, qr_cache)
        c.showPage()
        pages += 1
        if idx >= len(words):
            break

    c.save()
    return pages
