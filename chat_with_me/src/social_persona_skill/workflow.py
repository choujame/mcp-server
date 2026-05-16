from __future__ import annotations
import re
from pathlib import Path
from typing import List, Optional

from .models import Person, Source
from .storage import PersonaStorage
from .runtime import RuntimeManager
from .backends import get_backend, detect_platform, slug_from_url
from .service import generate_persona_files
from .skills import SkillCompiler, _make_slug


def _infer_display_name(url: str, backend) -> str:
    try:
        return backend.display_name(url)
    except Exception:
        return slug_from_url(url)


def create_persona(
    urls: List[str],
    runtime_root: Path,
    storage_dir: Path,
    claude_dir: Optional[Path] = None,
) -> Person:
    runtime = RuntimeManager(runtime_root)
    storage = PersonaStorage(storage_dir)

    person = Person()
    all_entries = []

    for url in urls:
        platform = detect_platform(url)
        backend = get_backend(platform, runtime)
        account_slug = slug_from_url(url)

        print(f"[workflow] Collecting from {platform}: {url}")
        entries = backend.collect(url)
        print(f"[workflow] Collected {len(entries)} entries from {url}")

        source = Source(platform=platform, url=url, account_slug=account_slug)
        person.sources.append(source)

        if not person.display_name:
            person.display_name = _infer_display_name(url, backend)
        if not person.slug:
            person.slug = _make_slug(person.display_name)

        storage.append_corpus(person.id, platform, account_slug, entries)
        all_entries.extend(entries)

    storage.save_person(person)
    storage.save_sources(person.id, person.sources)

    print(f"[workflow] Generating persona files using Claude...")
    skill_files = generate_persona_files(person, all_entries)
    storage.save_skill_sources(person.id, skill_files)
    storage.save_profile(person.id, skill_files.get("profile.md", ""))

    print(f"[workflow] Persona created: {person.id} ({person.display_name})")
    return person


def attach_account(
    person_id: str,
    url: str,
    runtime_root: Path,
    storage_dir: Path,
) -> Person:
    runtime = RuntimeManager(runtime_root)
    storage = PersonaStorage(storage_dir)

    person = storage.load_person(person_id)
    platform = detect_platform(url)
    backend = get_backend(platform, runtime)
    account_slug = slug_from_url(url)

    print(f"[workflow] Attaching {platform} account: {url}")
    entries = backend.collect(url)
    print(f"[workflow] Collected {len(entries)} new entries")

    source = Source(platform=platform, url=url, account_slug=account_slug)
    person.sources.append(source)

    storage.append_corpus(person.id, platform, account_slug, entries)
    storage.save_person(person)
    storage.save_sources(person.id, person.sources)

    # Regenerate persona with full corpus
    corpus = storage.load_corpus(person_id)
    print(f"[workflow] Regenerating persona files ({len(corpus)} total entries)...")
    skill_files = generate_persona_files(person, corpus)
    storage.save_skill_sources(person.id, skill_files)
    storage.save_profile(person.id, skill_files.get("profile.md", ""))

    print(f"[workflow] Account attached to persona: {person.id}")
    return person


def build_skill(
    person_id: str,
    storage_dir: Path,
    claude_dir: Path,
    slug: Optional[str] = None,
) -> Path:
    storage = PersonaStorage(storage_dir)
    compiler = SkillCompiler(storage, claude_dir)
    return compiler.build(person_id, slug=slug)
