from __future__ import annotations
from typing import List
from .models import CorpusEntry


def normalize_x_posts(raw: List[dict]) -> List[CorpusEntry]:
    entries = []
    for item in raw:
        text = (
            item.get("full_text")
            or item.get("text")
            or item.get("Tweet")
            or ""
        ).strip()
        if not text:
            continue
        url = item.get("url") or item.get("Tweet URL") or None
        ts = item.get("created_at") or item.get("Datetime") or None
        entries.append(CorpusEntry(text=text, platform="x", url=url, timestamp=ts))
    return entries


def normalize_xiaohongshu_notes(raw: List[dict]) -> List[CorpusEntry]:
    entries = []
    for item in raw:
        title = item.get("title") or item.get("note_title") or ""
        desc = item.get("desc") or item.get("note_content") or ""
        text = f"{title}\n{desc}".strip() if title else desc.strip()
        if not text:
            continue
        url = item.get("note_url") or item.get("url") or None
        ts = item.get("time") or item.get("last_update_time") or None
        entries.append(CorpusEntry(text=text, platform="xiaohongshu", url=url, timestamp=ts))
    return entries


def normalize(platform: str, raw: List[dict]) -> List[CorpusEntry]:
    if platform == "x":
        return normalize_x_posts(raw)
    elif platform == "xiaohongshu":
        return normalize_xiaohongshu_notes(raw)
    raise ValueError(f"Unknown platform: {platform!r}")
