"""Bingo boards PDF generator (call sheet + 4 player boards)."""

from __future__ import annotations

import random
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics

from .config import CARD_BORDER, EPISODE_CHARACTER, INK, LEAF, SKY
from .icons import get_icon, to_bytes
from .pdf_common import (
    draw_corner_character,
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
    return f"{short} Bingo"


def _pick_boards(words: list[str], n_boards: int = 4, grid: int = 3, seed: int = 7) -> list[list[str]]:
    rng = random.Random(seed)
    pool = list(words)
    boards = []
    for _ in range(n_boards):
        if len(pool) >= grid * grid:
            cells = rng.sample(pool, grid * grid)
        else:
            cells = list(pool)
            while len(cells) < grid * grid:
                cells.append(rng.choice(pool))
            rng.shuffle(cells)
            cells = cells[: grid * grid]
            if len(set(cells)) < len(cells) and len(pool) >= grid * grid:
                cells = rng.sample(pool, grid * grid)
        boards.append(cells)
        rng.shuffle(pool)
    return boards


def build_bingo_pdf(
    out_path: Path,
    episode,
    size_name: str,
    qr_cache: dict | None = None,
    placements: list | None = None,
) -> int:
    words = list(episode.words)
    boards = _pick_boards(words, n_boards=4, grid=3, seed=episode.episode * 17 + 3)
    c, width, height, margin = make_canvas(out_path, size_name)
    footer_top = margin + 0.85 * inch + 8
    pages = 0
    char_name = EPISODE_CHARACTER.get(episode.episode, "ian")

    # --- Call sheet page ---
    fill_paper(c, width, height)
    y = draw_wordmark(c, width, height, margin)
    y = draw_title(c, width, y - 10, _activity_title(episode.title), 20)
    y = draw_episode_line(c, width, y, episode.title)
    y = draw_title(c, width, y - 4, "Caller Sheet", 16)

    rules = (
        "Rules: The grown-up calls out a word. Players cover that picture on their board. "
        "First to cover a full row, column, or the whole board wins. Ages 2 to 6 — help is welcome!"
    )
    c.setFillColor(HexColor(INK))
    text_obj = c.beginText(margin, y - 4)
    text_obj.setFont("Atkinson", 10)
    max_w = width - 2 * margin
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
    y = text_obj.getY() - 16

    cols = 4
    usable_bottom = footer_top + 100  # leave room for corner character
    cell_h = min(52, (y - usable_bottom) / ((len(words) + cols - 1) // cols + 0.5))
    cell_w = (width - 2 * margin) / cols
    for i, word in enumerate(words):
        col = i % cols
        row = i // cols
        x0 = margin + col * cell_w
        y0 = y - (row + 1) * cell_h
        if y0 < usable_bottom:
            break
        rounded_card(c, x0 + 3, y0 + 3, cell_w - 6, cell_h - 6, stroke=CARD_BORDER)
        icon = get_icon(word, 160)
        ib = image_reader_from_png_bytes(to_bytes(icon))
        isz = min(cell_h - 18, 32)
        c.drawImage(ib, x0 + 8, y0 + (cell_h - isz) / 2, isz, isz, mask="auto")
        c.setFillColor(HexColor(INK))
        c.setFont("Atkinson-Bold", 10)
        c.drawString(x0 + 12 + isz, y0 + cell_h / 2 - 4, word)

    draw_corner_character(c, char_name, width, height, margin, footer_top, placements, corner="right")
    draw_footer(c, width, height, margin, episode.youtube_url, qr_cache)
    c.showPage()
    pages += 1

    # --- Player boards (2 per page); character only on first player page ---
    for b_idx in range(0, len(boards), 2):
        fill_paper(c, width, height)
        y = draw_wordmark(c, width, height, margin)
        if pages == 1:
            y = draw_title(c, width, y - 6, "Player Boards", 18)
            y = draw_episode_line(c, width, y, episode.title)
        else:
            y = draw_title(c, width, y - 6, "Player Boards (continued)", 16)

        usable_top = y - 4
        usable_bottom = footer_top + 4
        board_h = (usable_top - usable_bottom) / 2 - 8

        for local_i in range(2):
            bi = b_idx + local_i
            if bi >= len(boards):
                break
            cells = boards[bi]
            top = usable_top - local_i * (board_h + 12)
            bottom = top - board_h
            c.setFillColor(HexColor(INK))
            c.setFont("Baloo2", 14)
            c.drawString(margin, top - 2, f"Board {bi + 1}")

            grid = 3
            grid_top = top - 18
            grid_h = grid_top - bottom - 4
            grid_w = width - 2 * margin
            cw, ch = grid_w / grid, grid_h / grid

            for r in range(grid):
                for col in range(grid):
                    word = cells[r * grid + col]
                    x0 = margin + col * cw
                    y0 = bottom + 4 + (grid - 1 - r) * ch
                    rounded_card(c, x0 + 3, y0 + 3, cw - 6, ch - 6, stroke=SKY if (r + col) % 2 == 0 else LEAF)
                    icon = get_icon(word, 200)
                    ib = image_reader_from_png_bytes(to_bytes(icon))
                    isz = min(cw, ch) * 0.5
                    c.drawImage(ib, x0 + (cw - isz) / 2, y0 + ch * 0.32, isz, isz, mask="auto")
                    c.setFillColor(HexColor(INK))
                    fs = 11 if len(word) < 10 else 9
                    c.setFont("Baloo2", fs)
                    c.drawCentredString(x0 + cw / 2, y0 + 10, word)

        if pages == 1:
            draw_corner_character(c, char_name, width, height, margin, footer_top, placements, corner="left")

        draw_footer(c, width, height, margin, episode.youtube_url, qr_cache)
        c.showPage()
        pages += 1

    c.save()
    return pages
