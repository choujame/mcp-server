from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional, List
import time
import uuid


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


@dataclass
class CorpusEntry:
    text: str
    platform: str
    url: Optional[str] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "CorpusEntry":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Source:
    platform: str
    url: str
    account_slug: str
    added_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Source":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Person:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    slug: str = ""
    display_name: str = ""
    sources: List[Source] = field(default_factory=list)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Person":
        sources = [Source.from_dict(s) for s in d.get("sources", [])]
        return cls(
            id=d["id"],
            slug=d.get("slug", ""),
            display_name=d.get("display_name", ""),
            sources=sources,
            created_at=d.get("created_at", _now()),
            updated_at=d.get("updated_at", _now()),
        )

    def touch(self):
        self.updated_at = _now()
