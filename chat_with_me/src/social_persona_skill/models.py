from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
import time
import uuid


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class Platform(StrEnum):
    X = "x"
    GITHUB = "github"
    XIAOHONGSHU = "xiaohongshu"
    INSTAGRAM = "instagram"
    ZHIHU = "zhihu"


@dataclass(slots=True, frozen=True)
class AccountInput:
    platform: Platform
    url: str


@dataclass(slots=True)
class AccountRecord:
    platform: Platform
    url: str
    profile_id: str
    display_name: str

    def to_dict(self) -> dict:
        return {
            "platform": str(self.platform),
            "url": self.url,
            "profile_id": self.profile_id,
            "display_name": self.display_name,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "AccountRecord":
        return cls(
            platform=Platform(d["platform"]),
            url=d["url"],
            profile_id=d["profile_id"],
            display_name=d["display_name"],
        )


@dataclass(slots=True)
class CorpusRecord:
    platform: Platform
    account_url: str
    account_id: str
    item_id: str
    item_type: str  # "post" or "bio"
    text: str
    created_at: str
    source_url: str
    collector: str

    def to_dict(self) -> dict:
        return {
            "platform": str(self.platform),
            "account_url": self.account_url,
            "account_id": self.account_id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "text": self.text,
            "created_at": self.created_at,
            "source_url": self.source_url,
            "collector": self.collector,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CorpusRecord":
        return cls(
            platform=Platform(d["platform"]),
            account_url=d["account_url"],
            account_id=d["account_id"],
            item_id=d["item_id"],
            item_type=d["item_type"],
            text=d["text"],
            created_at=d["created_at"],
            source_url=d["source_url"],
            collector=d["collector"],
        )


@dataclass(slots=True)
class CollectedAccount:
    account: AccountRecord
    corpus: list[CorpusRecord]


@dataclass(slots=True)
class PersonRecord:
    person_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    persona_name: str = ""
    accounts: list[AccountRecord] = field(default_factory=list)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def touch(self) -> None:
        self.updated_at = _now()

    def to_dict(self) -> dict:
        return {
            "person_id": self.person_id,
            "persona_name": self.persona_name,
            "accounts": [a.to_dict() for a in self.accounts],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "PersonRecord":
        accounts = [AccountRecord.from_dict(a) for a in d.get("accounts", [])]
        return cls(
            person_id=d["person_id"],
            persona_name=d.get("persona_name", ""),
            accounts=accounts,
            created_at=d.get("created_at", _now()),
            updated_at=d.get("updated_at", _now()),
        )


@dataclass(slots=True)
class SourceRecord:
    platform: Platform
    url: str
    corpus_path: str
    collected_at: str = ""

    def to_dict(self) -> dict:
        return {
            "platform": str(self.platform),
            "url": self.url,
            "corpus_path": self.corpus_path,
            "collected_at": self.collected_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "SourceRecord":
        return cls(
            platform=Platform(d["platform"]),
            url=d["url"],
            corpus_path=d["corpus_path"],
            collected_at=d.get("collected_at", ""),
        )


@dataclass(slots=True)
class StoredPersona:
    person: PersonRecord
    markdown: str
    sources: list[SourceRecord] = field(default_factory=list)


@dataclass(slots=True)
class OperationResult:
    person: PersonRecord
    stored_path: str = ""


@dataclass(slots=True)
class SkillBuildResult:
    person_id: str
    installed_skill_dir: str
    skill_name: str = ""
