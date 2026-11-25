"""Memory matching game PDF generator."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics

from .config import EPISODE_CHARACTER, GRAPE, INK, SKY
from .icons import get_icon, to_bytes
from .pdf_common import (
    draw_corner_character,
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
    return f"{short} Memory Game"


def build_memory_pdf(
    out_path: Path,
    episode,
    size_name: str,
    qr_cache: dict | None = None,
    placements: list | None = None,
) -> int:
    # Pairing rule: two identical picture+word cards per word.
    words = list(episode.words)[:12]
    cards = []
    for w in words:
        cards.append(w)
        cards.append(w)

    c, width, height, margin = make_canvas(out_path, size_name)
    footer_top = margin + 0.85 * inch + 8
    pages = 0
    char_name = EPISODE_CHARACTER.get(episode.episode, "ian")

    cols, rows = 3, 4
    idx = 0

    while idx < len(cards):
        fill_paper(c, width, height)
        y = draw_wordmark(c, width, height, margin)
        if pages == 0:
            y = draw_title(c, width, y - 10, _activity_title(episode.title), 20)
            y = draw_episode_line(c, width, y, episode.title)
            rules = (
                "Rules: Mix the cards and place them face down. Take turns flipping two cards. "
                "If the pictures match, keep the pair! Same word = match. Ages 2 to 6."
            )
            c.setFillColor(HexColor(INK))
            text_obj = c.beginText(margin, y)
            text_obj.setFont("Atkinson", 10)
            max_w = width - 2 * margin - 80  # leave corner clear of rules if needed
            line = ""
            for w in rules.split():
                trial = (line + " " + w).strip()
                if pdfmetrics.stringWidth(trial, "Atkinson", 10) > max_w:
                    text_obj.textLine(line)
                    line = w
                else:
                    line = trial
            if line:
                text_obj.textLine(line)
            c.drawText(text_obj)
            y = text_obj.getY() - 10
        else:
            y = draw_title(c, width, y - 6, "Memory Cards (continued)", 16)

        usable_top = y - 6
        usable_bottom = footer_top + (100 if pages == 0 else 4)
        usable_h = usable_top - usable_bottom
        usable_w = width - 2 * margin
        card_w = usable_w / cols
        card_h = usable_h / rows

        for r in range(rows):
            for col in range(cols):
                if idx >= len(cards):
                    break
                word = cards[idx]
                idx += 1
                x0 = margin + col * card_w
                y0 = usable_bottom + (rows - 1 - r) * card_h
                pad = 5
                stroke = SKY if (r + col) % 2 == 0 else GRAPE
                rounded_card(c, x0 + pad, y0 + pad, card_w - 2 * pad, card_h - 2 * pad, stroke=stroke)

                icon = get_icon(word, 240)
                ib = image_reader_from_png_bytes(to_bytes(icon))
                isz = min(card_w, card_h) * 0.52
                c.drawImage(ib, x0 + (card_w - isz) / 2, y0 + card_h * 0.30, isz, isz, mask="auto")

                c.setFillColor(HexColor(INK))
                fs = 12 if len(word) < 12 else 10
                c.setFont("Baloo2", fs)
                c.drawCentredString(x0 + card_w / 2, y0 + pad + 10, word)

                if col < cols - 1:
                    draw_cut_line(c, x0 + card_w, y0 + 3, x0 + card_w, y0 + card_h - 3)
                if r < rows - 1:
                    draw_cut_line(c, x0 + 3, y0, x0 + card_w - 3, y0)

        if pages == 0:
            draw_corner_character(
                c, char_name, width, height, margin, footer_top, placements, corner="right"
            )

        draw_footer(c, width, height, margin, episode.youtube_url, qr_cache)
        c.showPage()
        pages += 1

    c.save()
    return pages
