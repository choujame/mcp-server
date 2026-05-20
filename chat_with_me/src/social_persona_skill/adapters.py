from __future__ import annotations
from typing import List
import uuid

from .models import Platform, AccountRecord, CorpusRecord


def _now_str() -> str:
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def normalize_x_posts(account: AccountRecord, raw: List[dict]) -> List[CorpusRecord]:
    records: List[CorpusRecord] = []
    for item in raw:
        text = (
            item.get("full_text")
            or item.get("text")
            or item.get("Tweet")
            or ""
        ).strip()
        if not text:
            continue
        source_url = item.get("url") or item.get("Tweet URL") or account.url
        ts = item.get("created_at") or item.get("Datetime") or _now_str()
        item_id = item.get("id") or item.get("id_str") or uuid.uuid4().hex[:16]
        records.append(CorpusRecord(
            platform=Platform.X,
            account_url=account.url,
            account_id=account.profile_id,
            item_id=str(item_id),
            item_type="post",
            text=text,
            created_at=str(ts),
            source_url=str(source_url),
            collector="scweet",
        ))
    return records


def normalize_xiaohongshu_notes(account: AccountRecord, raw: List[dict]) -> List[CorpusRecord]:
    records: List[CorpusRecord] = []
    for item in raw:
        title = item.get("title") or item.get("note_title") or ""
        desc = item.get("desc") or item.get("note_content") or ""
        text = f"{title}\n{desc}".strip() if title else desc.strip()
        if not text:
            continue
        source_url = item.get("note_url") or item.get("url") or account.url
        ts = item.get("time") or item.get("last_update_time") or _now_str()
        item_id = item.get("id") or item.get("note_id") or uuid.uuid4().hex[:16]
        records.append(CorpusRecord(
            platform=Platform.XIAOHONGSHU,
            account_url=account.url,
            account_id=account.profile_id,
            item_id=str(item_id),
            item_type="post",
            text=text,
            created_at=str(ts),
            source_url=str(source_url),
            collector="mediacrawler",
        ))
    return records


def normalize(platform: Platform, account: AccountRecord, raw: List[dict]) -> List[CorpusRecord]:
    if platform == Platform.X:
        return normalize_x_posts(account, raw)
    elif platform == Platform.XIAOHONGSHU:
        return normalize_xiaohongshu_notes(account, raw)
    raise ValueError(f"Unknown platform: {platform!r}")
