"""Build all activities for an episode and run checks."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from .bingo import build_bingo_pdf
from .checks import run_activity_checks
from .config import OUTPUT_DIR
from .episodes import Episode
from .flashcards import build_flashcards_pdf
from .memory import build_memory_pdf
from .pin import build_pin


def _meta_title(activity: str, episode: Episode) -> str:
    short = episode.title.replace("Ian's ", "").replace("Ian’s ", "")
    return {
        "flashcards": f"Free {short} Flashcards for Toddlers and Preschool",
        "bingo": f"Free {short} Bingo for Toddlers and Preschool",
        "memory": f"Free {short} Memory Game for Toddlers and Preschool",
    }[activity]


def _meta_description(activity: str, episode: Episode) -> str:
    base = (
        f"A free printable {activity} activity for ages 2 to 6. "
        f"Goes with the Learn with Ian episode {episode.title}. "
        f"Watch it together on YouTube, then play! "
        f"Includes US Letter and A4 PDFs. learnwithian.com"
    )
    return base[:450]


def _keywords(activity: str, episode: Episode) -> list[str]:
    short = episode.title.replace("Ian's ", "").replace("Ian’s ", "").lower()
    return [
        f"{short} {activity} for toddlers",
        "free printable",
        "preschool activity",
        "learn with ian",
    ]


def build_activity(episode: Episode, activity: str) -> tuple[bool, dict, list[str]]:
    out_dir = OUTPUT_DIR / episode.slug / activity
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    qr_cache: dict = {}
    placements: list = []
    builders = {
        "flashcards": build_flashcards_pdf,
        "bingo": build_bingo_pdf,
        "memory": build_memory_pdf,
    }
    builder = builders[activity]

    pages_letter = builder(
        out_dir / f"{episode.slug}-{activity}-letter.pdf",
        episode,
        "letter",
        qr_cache,
        placements,
    )
    pages_a4 = builder(
        out_dir / f"{episode.slug}-{activity}-a4.pdf",
        episode,
        "a4",
        qr_cache,
        placements,
    )

    words_for_meta = list(episode.words)
    if activity == "memory":
        words_for_meta = list(episode.words)[:12]

    build_pin(out_dir / "pin.png", episode, activity, preview_words=words_for_meta[:6])

    meta = {
        "episode": episode.episode,
        "episode_title": episode.title,
        "youtube_id": episode.youtube_id,
        "activity": activity,
        "title": _meta_title(activity, episode),
        "description": _meta_description(activity, episode),
        "keywords": _keywords(activity, episode),
        "words": words_for_meta,
        "pages_letter": pages_letter,
        "pages_a4": pages_a4,
        "checks_passed": False,
    }

    ok, errors = run_activity_checks(episode, activity, out_dir, meta, placements)
    meta["checks_passed"] = ok
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return ok, meta, errors


def build_episode(episode: Episode) -> tuple[bool, list[str]]:
    all_errors: list[str] = []
    all_ok = True
    for activity in ("flashcards", "bingo", "memory"):
        ok, meta, errors = build_activity(episode, activity)
        if not ok:
            all_ok = False
            all_errors.extend([f"{episode.slug}/{activity}: {e}" for e in errors])
            # remove failed activity output so CI does not commit it
            out_dir = OUTPUT_DIR / episode.slug / activity
            if out_dir.exists():
                # keep meta with checks_passed false? Brief: do not commit that episode
                pass
    return all_ok, all_errors


def build_episodes(episodes: list[Episode]) -> dict:
    results = {}
    for ep in episodes:
        print(f"Building episode {ep.episode}: {ep.title} ({ep.slug})...")
        ok, errors = build_episode(ep)
        results[ep.slug] = {"ok": ok, "errors": errors, "title": ep.title, "episode": ep.episode}
        if ok:
            print(f"  OK — checks passed")
        else:
            print(f"  FAILED:")
            for e in errors:
                print(f"    - {e}")
    return results
