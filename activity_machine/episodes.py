"""Load episodes from local JSON and/or the public extras CSV."""

from __future__ import annotations

import csv
import io
import json
import re
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

from .config import CSV_URL, EPISODES_JSON, OUTPUT_DIR


@dataclass
class Episode:
    episode: int
    youtube_id: str
    slug: str
    title: str
    words: list[str] = field(default_factory=list)

    @property
    def youtube_url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    @property
    def output_dir(self):
        return OUTPUT_DIR / self.slug


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def fetch_youtube_title(youtube_id: str) -> Optional[str]:
    url = (
        "https://www.youtube.com/oembed?"
        f"url=https://www.youtube.com/watch?v={youtube_id}&format=json"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LearnWithIanBot/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        title = data.get("title") or ""
        # Strip channel suffix if present
        title = re.sub(r"\s*\|\s*Learn with Ian.*$", "", title, flags=re.I).strip()
        return title or None
    except Exception:
        return None


def clean_youtube_title(title: str) -> str:
    """Trim SEO suffixes from oEmbed titles into a short episode name."""
    t = title.strip()
    t = re.sub(r"\s*\|\s*Learn with Ian.*$", "", t, flags=re.I).strip()
    t = re.sub(r"\s*-\s*Learn with Ian.*$", "", t, flags=re.I).strip()
    return t


def load_local_episodes() -> list[Episode]:
    raw = json.loads(EPISODES_JSON.read_text(encoding="utf-8"))
    episodes = []
    for row in raw:
        # Prefer curated titles in episodes.json (match website names).
        title = row.get("title")
        if not title:
            yt = fetch_youtube_title(row["youtube_id"])
            title = clean_youtube_title(yt) if yt else f"Episode {row['episode']}"
        episodes.append(
            Episode(
                episode=int(row["episode"]),
                youtube_id=row["youtube_id"],
                slug=row.get("slug") or slugify(title),
                title=title,
                words=[w.strip() for w in row["words"] if w.strip()],
            )
        )
    return episodes


def fetch_csv_episodes() -> list[Episode]:
    try:
        req = urllib.request.Request(CSV_URL, headers={"User-Agent": "LearnWithIanBot/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8")
    except Exception:
        return []

    reader = csv.DictReader(io.StringIO(text))
    episodes = []
    for row in reader:
        youtube_id = (row.get("youtube_id") or "").strip()
        words_raw = (row.get("activity_words") or "").strip()
        if not youtube_id or not words_raw:
            continue
        ep_num = row.get("episode") or row.get("Episode") or "0"
        try:
            ep_i = int(str(ep_num).strip())
        except ValueError:
            ep_i = 0
        words = [w.strip() for w in words_raw.split("|") if w.strip()]
        title = fetch_youtube_title(youtube_id) or f"Episode {ep_i}"
        slug = slugify(title)
        # Prefer known website slugs from local file when ids match
        episodes.append(
            Episode(
                episode=ep_i,
                youtube_id=youtube_id,
                slug=slug,
                title=title,
                words=words,
            )
        )
    return episodes


def merge_with_known_slugs(episodes: list[Episode], local: list[Episode]) -> list[Episode]:
    by_id = {e.youtube_id: e for e in local}
    out = []
    for e in episodes:
        if e.youtube_id in by_id:
            known = by_id[e.youtube_id]
            e.slug = known.slug
            if not e.words:
                e.words = known.words
            if known.title and (not e.title or e.title.startswith("Episode")):
                e.title = known.title
        out.append(e)
    return out


def get_episodes(all_local: bool = True) -> list[Episode]:
    local = load_local_episodes()
    if all_local:
        return local
    csv_eps = fetch_csv_episodes()
    if not csv_eps:
        return local
    return merge_with_known_slugs(csv_eps, local)


def get_new_episodes() -> list[Episode]:
    """Episodes from CSV (or local) that have words and no output folder yet."""
    local = load_local_episodes()
    csv_eps = fetch_csv_episodes()
    pool = merge_with_known_slugs(csv_eps, local) if csv_eps else local
    new = []
    for e in pool:
        if not e.words:
            continue
        if e.output_dir.exists():
            continue
        new.append(e)
    return new


def find_episode(youtube_id: str) -> Optional[Episode]:
    for e in get_episodes(all_local=True):
        if e.youtube_id == youtube_id:
            return e
    # Try CSV
    for e in fetch_csv_episodes():
        if e.youtube_id == youtube_id:
            local = load_local_episodes()
            return merge_with_known_slugs([e], local)[0]
    return None
