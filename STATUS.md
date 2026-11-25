# Status

Updated: 2026-11-25 12:41 UTC

## What was made

- Activity machine: `make_activities.py` + `activity_machine/` (flashcards, bingo, memory, pin images, section 11 checks).
- Episodes **1–7** built from `episodes.json` and **all checks passed**.
- GitHub Action: `.github/workflows/activities.yml` (every 6 hours + manual dispatch).
- Brand fonts bundled in `fonts/`; character cutouts in `characters/` (Liam cropped to the front-facing standing pose).

### Episodes

| Slug | Episode | Result |
|------|---------|--------|
| `zoo-day` | 1 — Ian's Zoo Day | PASS |
| `little-garden` | 2 — Ian's Little Garden | PASS |
| `shape-hunt` | 3 — Ian's Shape Hunt | PASS |
| `number-walk` | 4 — Ian's Number Walk | PASS |
| `ian-s-color-day` | 5 — Ian's Color Day | PASS |
| `ian-s-snowy-day` | 6 — Ian's Snowy Day | PASS |
| `ian-s-christmas-eve` | 7 — Ian's Christmas Eve | PASS |

Each episode has three activities (`flashcards`, `bingo`, `memory`), each with Letter PDF, A4 PDF, `pin.png` (1000×1500), and `meta.json`.

## Files

- Output files under `output/`: **84** (42 PDF, 21 PNG, 21 JSON)
- Character PNGs: **7**
- Font files: **3**

## Problems

- None blocking. Character studio backgrounds were removed (crop / transparency only; no redraw). Liam uses only the left front-facing standing pose as required.
- Google Fonts zip download was blocked in this environment; Baloo 2 ExtraBold was instantiated from the official variable font in `google/fonts` (OFL).
