# Learn with Ian — free printable activities machine

Builds free toddler/preschool printables (flashcards, bingo, memory) plus a
Pinterest image for each Learn with Ian episode. Every page links back to the
episode with a QR code.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Character art lives in `characters/` (already committed). Fonts are in `fonts/`.

## Run

Build episodes 1–7 from `episodes.json`:

```bash
python make_activities.py --all
```

Build one episode by YouTube id:

```bash
python make_activities.py --episode TAyFj_YT8KM
```

Build only **new** episodes from the public extras CSV (used by GitHub Actions):

```bash
python make_activities.py --new
```

Outputs land in `output/<episode-slug>/<activity>/` as Letter + A4 PDFs, `pin.png`,
and `meta.json`. Section 11 checks run automatically; failed episodes are not
kept for `--new` runs.

## GitHub Action

`.github/workflows/activities.yml` runs every 6 hours and on manual dispatch. It
builds new CSV episodes, checks them, and commits only new `output/` folders with
the message `New activities for <slug>`.
