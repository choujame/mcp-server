from __future__ import annotations
from pathlib import Path
from typing import List, Optional
import json

from .models import Person, Source, CorpusEntry


class PersonaStorage:
    def __init__(self, storage_dir: Path):
        self.root = Path(storage_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def _person_dir(self, person_id: str) -> Path:
        d = self.root / person_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _corpus_dir(self, person_id: str, platform: str) -> Path:
        d = self._person_dir(person_id) / "corpora" / platform
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _skill_dir(self, person_id: str) -> Path:
        d = self._person_dir(person_id) / "skill"
        d.mkdir(parents=True, exist_ok=True)
        return d

    # ── person ──────────────────────────────────────────────────────────

    def save_person(self, person: Person) -> None:
        person.touch()
        path = self._person_dir(person.id) / "person.json"
        path.write_text(json.dumps(person.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def load_person(self, person_id: str) -> Person:
        path = self._person_dir(person_id) / "person.json"
        if not path.exists():
            raise FileNotFoundError(f"Persona {person_id!r} not found in {self.root}")
        return Person.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_persons(self) -> List[Person]:
        persons = []
        for d in sorted(self.root.iterdir()):
            p = d / "person.json"
            if p.exists():
                try:
                    persons.append(Person.from_dict(json.loads(p.read_text(encoding="utf-8"))))
                except Exception:
                    pass
        return persons

    # ── sources ─────────────────────────────────────────────────────────

    def save_sources(self, person_id: str, sources: list) -> None:
        path = self._person_dir(person_id) / "sources.json"
        path.write_text(json.dumps([s.to_dict() for s in sources], ensure_ascii=False, indent=2), encoding="utf-8")

    # ── profile.md ──────────────────────────────────────────────────────

    def save_profile(self, person_id: str, markdown: str) -> None:
        path = self._person_dir(person_id) / "profile.md"
        path.write_text(markdown, encoding="utf-8")

    def load_profile(self, person_id: str) -> str:
        path = self._person_dir(person_id) / "profile.md"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    # ── corpus ──────────────────────────────────────────────────────────

    def append_corpus(self, person_id: str, platform: str, account_slug: str, entries: List[CorpusEntry]) -> None:
        path = self._corpus_dir(person_id, platform) / f"{account_slug}.jsonl"
        with path.open("a", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")

    def load_corpus(self, person_id: str) -> List[CorpusEntry]:
        corpus_root = self._person_dir(person_id) / "corpora"
        entries = []
        if not corpus_root.exists():
            return entries
        for platform_dir in sorted(corpus_root.iterdir()):
            for jsonl in sorted(platform_dir.glob("*.jsonl")):
                for line in jsonl.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line:
                        try:
                            entries.append(CorpusEntry.from_dict(json.loads(line)))
                        except Exception:
                            pass
        return entries

    # ── skill source files ───────────────────────────────────────────────

    def save_skill_sources(self, person_id: str, files: dict) -> None:
        skill_dir = self._skill_dir(person_id)
        for filename, content in files.items():
            (skill_dir / filename).write_text(content, encoding="utf-8")

    def load_skill_sources(self, person_id: str) -> dict:
        skill_dir = self._skill_dir(person_id)
        if not skill_dir.exists():
            return {}
        return {p.name: p.read_text(encoding="utf-8") for p in skill_dir.iterdir() if p.is_file()}
