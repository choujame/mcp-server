from __future__ import annotations
import re
from pathlib import Path
from typing import List, Optional

from .models import (
    Platform,
    AccountInput,
    PersonRecord,
    OperationResult,
    SkillBuildResult,
    StoredPersona,
    SourceRecord,
    CollectedAccount,
)
from .backends import Backend, build_backend_registry, platform_for_url, BackendError
from .runtime import RuntimeLayout
from .storage import PersonaStorage
from .service import PersonaDistiller
from .skills import SkillBuilder, _SKILL_HOST_CHOICES


def _now_str() -> str:
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class PersonaWorkflow:
    """
    High-level orchestration: collect → distill → store → build skill.
    """

    def __init__(
        self,
        *,
        storage_dir: Path,
        runtime_root: Path,
        claude_dir: Path,
    ) -> None:
        self.storage = PersonaStorage(Path(storage_dir))
        self.layout = RuntimeLayout(Path(runtime_root))
        self.claude_dir = Path(claude_dir)
        self.distiller = PersonaDistiller()
        self._registry: Optional[dict[Platform, Backend]] = None

    # ── internal helpers ──────────────────────────────────────────────────

    def _platform_for_url(self, url: str) -> Platform:
        return platform_for_url(url)

    def _account(self, url: str) -> AccountInput:
        platform = self._platform_for_url(url)
        return AccountInput(platform=platform, url=url)

    def _backend(self, platform: Platform) -> Backend:
        if self._registry is None:
            self._registry = build_backend_registry(self.layout)
        if platform not in self._registry:
            raise BackendError(f"No backend available for platform: {platform!r}")
        return self._registry[platform]

    def _slug(self, profile_id: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", profile_id.lower()).strip("-")[:40] or "account"

    def _source_for_collection(self, item: CollectedAccount) -> SourceRecord:
        corpus_path = ""
        return SourceRecord(
            platform=item.account.platform,
            url=item.account.url,
            corpus_path=corpus_path,
            collected_at=_now_str(),
        )

    # ── public API ────────────────────────────────────────────────────────

    def create_persona(self, urls: List[str]) -> tuple[OperationResult, Path]:
        """
        Collect from one or more URLs, distill a persona, and store it.
        Returns (OperationResult, person_dir).
        """
        collections: List[CollectedAccount] = []
        for url in urls:
            acct = self._account(url)
            backend = self._backend(acct.platform)
            print(f"[workflow] Collecting from {acct.platform}: {url}")
            collected = backend.collect(acct)
            print(f"[workflow] Collected {len(collected.corpus)} items from {url}")
            collections.append(collected)

        print("[workflow] Distilling persona with Claude...")
        person, markdown = self.distiller.create_person(collections)

        sources = [self._source_for_collection(c) for c in collections]
        stored = StoredPersona(person=person, markdown=markdown, sources=sources)

        # Persist corpus
        for c in collections:
            corpus_path = self.storage.append_corpus(
                person.person_id,
                str(c.account.platform),
                c.account.profile_id,
                c.corpus,
            )
            # update source corpus_path
            for s in sources:
                if s.url == c.account.url:
                    s.corpus_path = corpus_path

        stored_path = self.storage.save_stored_persona(stored)
        print(f"[workflow] Persona created: {person.person_id} ({person.persona_name})")

        result = OperationResult(person=person, stored_path=stored_path)
        return result, Path(stored_path)

    def attach_account(self, person_id: str, url: str) -> OperationResult:
        """
        Collect from a new URL and attach it to an existing persona,
        regenerating the persona markdown.
        """
        stored = self.storage.load_stored_persona(person_id)
        acct = self._account(url)
        backend = self._backend(acct.platform)
        print(f"[workflow] Collecting from {acct.platform}: {url}")
        collected = backend.collect(acct)
        print(f"[workflow] Collected {len(collected.corpus)} items from {url}")

        # Load full corpus for re-distillation
        existing_corpus = self.storage.load_corpus(person_id)

        print("[workflow] Regenerating persona with Claude...")
        person, markdown = self.distiller.attach_accounts(
            stored,
            [collected],
            extra_corpus=existing_corpus,
        )

        new_source = self._source_for_collection(collected)
        corpus_path = self.storage.append_corpus(
            person.person_id,
            str(collected.account.platform),
            collected.account.profile_id,
            collected.corpus,
        )
        new_source.corpus_path = corpus_path

        updated_stored = StoredPersona(
            person=person,
            markdown=markdown,
            sources=stored.sources + [new_source],
        )
        stored_path = self.storage.save_stored_persona(updated_stored)
        print(f"[workflow] Account attached to persona: {person.person_id}")
        return OperationResult(person=person, stored_path=stored_path)

    def build_skill(
        self,
        person_id: str,
        hosts: Optional[List[str]] = None,
        slug: Optional[str] = None,
    ) -> SkillBuildResult:
        """
        Build and install the Claude skill for the given persona.
        """
        builder = SkillBuilder(self.storage, self.claude_dir)
        return builder.build(person_id, hosts=hosts, slug=slug)
