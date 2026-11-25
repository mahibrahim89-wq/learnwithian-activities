#!/usr/bin/env python3
"""Learn with Ian — printable activities machine.

Usage:
  python make_activities.py --all
  python make_activities.py --episode <youtube_id>
  python make_activities.py --new          # CSV rows with words and no output/ yet
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from activity_machine.build import build_episodes
from activity_machine.config import OUTPUT_DIR, ROOT
from activity_machine.episodes import find_episode, get_episodes, get_new_episodes


def write_status(results: dict, extra_notes: list[str] | None = None):
    status_path = ROOT / "STATUS.md"
    lines = [
        "# Status",
        "",
        f"Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## What was made",
        "",
    ]
    ok_n = sum(1 for r in results.values() if r["ok"])
    fail_n = len(results) - ok_n
    lines.append(f"- Episodes processed: **{len(results)}** ({ok_n} passed checks, {fail_n} failed)")
    lines.append("")
    for slug, r in results.items():
        mark = "PASS" if r["ok"] else "FAIL"
        lines.append(f"- `{slug}` (ep {r['episode']} — {r['title']}): **{mark}**")
        for e in r.get("errors") or []:
            lines.append(f"  - {e}")
    lines.append("")
    # file count
    files = list(OUTPUT_DIR.rglob("*")) if OUTPUT_DIR.exists() else []
    file_count = sum(1 for f in files if f.is_file())
    lines.append(f"## Files")
    lines.append("")
    lines.append(f"- Output files under `output/`: **{file_count}**")
    lines.append("")
    if extra_notes:
        lines.append("## Notes / problems")
        lines.append("")
        for n in extra_notes:
            lines.append(f"- {n}")
        lines.append("")
    status_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {status_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Learn with Ian printable activities")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="Build episodes 1–7 from episodes.json")
    g.add_argument("--episode", metavar="YOUTUBE_ID", help="Build one episode by YouTube id")
    g.add_argument("--new", action="store_true", help="Build new episodes from the public CSV")
    parser.add_argument("--no-status", action="store_true", help="Do not rewrite STATUS.md")
    args = parser.parse_args(argv)

    notes: list[str] = []
    # character check
    needed = ["ian.png", "mama_sana.png", "papa.png", "liam.png", "latte.png", "lisa.png", "lorie.png"]
    missing = [n for n in needed if not (ROOT / "characters" / n).exists()]
    if missing:
        notes.append(f"Missing character files: {missing}")
        if not args.no_status:
            write_status({}, notes)
        print("ERROR: missing characters", missing, file=sys.stderr)
        return 2

    if args.all:
        episodes = get_episodes(all_local=True)
    elif args.episode:
        ep = find_episode(args.episode)
        if not ep:
            print(f"Episode not found: {args.episode}", file=sys.stderr)
            return 1
        episodes = [ep]
    else:
        episodes = get_new_episodes()
        if not episodes:
            print("No new episodes to build.")
            if not args.no_status:
                write_status({}, ["No new episodes found in CSV (or all already have output/)."])
            return 0

    results = build_episodes(episodes)

    # If checks failed for an episode, remove its output so CI does not commit it
    if args.new:
        for slug, r in results.items():
            if not r["ok"]:
                ep_dir = OUTPUT_DIR / slug
                if ep_dir.exists():
                    import shutil

                    shutil.rmtree(ep_dir)
                    notes.append(f"Removed failed output for `{slug}` (not committed).")
                notes.extend(r.get("errors") or [])

    if not args.no_status:
        write_status(results, notes or None)

    return 0 if all(r["ok"] for r in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
