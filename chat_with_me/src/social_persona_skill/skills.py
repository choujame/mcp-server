from __future__ import annotations
import json
import re
from pathlib import Path
from typing import List, Optional

from .models import PersonRecord, SkillBuildResult
from .storage import PersonaStorage


_SKILL_HOST_CHOICES = ["claude", "codex", "opencode", "all"]


def _make_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug[:40] or "persona"


def _build_skill_md(person: PersonRecord, persona_markdown: str) -> str:
    display_name = person.persona_name or (person.accounts[0].display_name if person.accounts else "Unknown")
    return f"""# Persona Skill: {display_name}

{persona_markdown}

---

## Usage

This skill supports three modes. Start your message with one of:

- `roleplay: <your message>` — Respond as {display_name} would
- `ask: <question>` — Answer questions about {display_name}'s views and style
- `rewrite: <text>` — Rewrite the given text in {display_name}'s voice

"""


def _build_manifest(person: PersonRecord, slug: str) -> dict:
    display_name = person.persona_name or (person.accounts[0].display_name if person.accounts else "Unknown")
    return {
        "name": f"persona-{slug}",
        "description": f"Chat, analyze, and rewrite in the style of {display_name}",
        "version": "1.0.0",
        "person_id": person.person_id,
        "slug": slug,
        "accounts": [a.to_dict() for a in person.accounts],
    }


class SkillBuilder:
    """
    Installs persona skills into one or more host directories.
    Writes SKILL.md (uppercase) as the main skill file.
    """

    def __init__(self, storage: PersonaStorage, claude_dir: Path) -> None:
        self.storage = storage
        self.claude_dir = Path(claude_dir)

    def build(
        self,
        person_id: str,
        hosts: Optional[List[str]] = None,
        slug: Optional[str] = None,
    ) -> SkillBuildResult:
        """
        Build and install the skill. hosts can be ["claude"], ["codex"],
        ["opencode"], or ["all"] (installs everywhere).
        Returns a SkillBuildResult with the primary installed_skill_dir.
        """
        person = self.storage.load_person(person_id)
        markdown = self.storage.load_markdown(person_id)

        display_name = person.persona_name or (
            person.accounts[0].display_name if person.accounts else "Unknown"
        )
        if not slug:
            slug = _make_slug(display_name)

        skill_name = f"persona-{slug}"
        skill_md_content = _build_skill_md(person, markdown)
        manifest = _build_manifest(person, slug)
        manifest_json = json.dumps(manifest, ensure_ascii=False, indent=2)

        # Resolve which host directories to install into
        host_dirs = _resolve_host_dirs(hosts or ["claude"], self.claude_dir, slug)

        primary_dir: Optional[Path] = None
        for host_dir in host_dirs:
            host_dir.mkdir(parents=True, exist_ok=True)
            # SKILL.md — uppercase, as per original spec
            (host_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")
            (host_dir / "manifest.json").write_text(manifest_json, encoding="utf-8")
            print(f"[skill] Installed skill at: {host_dir}")
            if primary_dir is None:
                primary_dir = host_dir

        if primary_dir is None:
            raise RuntimeError("No host directories were resolved for skill installation.")

        # Also persist sources in storage
        self.storage.save_skill_sources(person_id, {
            "SKILL.md": skill_md_content,
            "manifest.json": manifest_json,
        })

        print(f"[skill] Skill name: /{skill_name}")
        return SkillBuildResult(
            person_id=person_id,
            installed_skill_dir=str(primary_dir),
            skill_name=skill_name,
        )


def _resolve_host_dirs(hosts: List[str], claude_dir: Path, slug: str) -> List[Path]:
    """
    Map host names to skill install directories.
    "claude"   → <claude_dir>/skills/persona-<slug>/
    "codex"    → ~/.codex/skills/persona-<slug>/
    "opencode" → ~/.opencode/skills/persona-<slug>/
    "all"      → all of the above
    """
    skill_rel = Path("skills") / f"persona-{slug}"

    host_map: dict[str, Path] = {
        "claude": claude_dir / skill_rel,
        "codex": Path.home() / ".codex" / skill_rel,
        "opencode": Path.home() / ".opencode" / skill_rel,
    }

    resolved: List[Path] = []
    for h in hosts:
        h = h.lower()
        if h == "all":
            resolved.extend(host_map.values())
        elif h in host_map:
            resolved.append(host_map[h])
        else:
            raise ValueError(
                f"Unknown host {h!r}. Choices: {_SKILL_HOST_CHOICES}"
            )
    # deduplicate while preserving order
    seen = set()
    unique: List[Path] = []
    for p in resolved:
        key = str(p)
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique
