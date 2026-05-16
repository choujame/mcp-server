from __future__ import annotations
import json
import re
from pathlib import Path

from .models import Person
from .storage import PersonaStorage


def _make_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug[:40] or "persona"


class SkillCompiler:
    def __init__(self, storage: PersonaStorage, claude_dir: Path):
        self.storage = storage
        self.claude_dir = Path(claude_dir)

    def build(self, person_id: str, slug: str | None = None) -> Path:
        person = self.storage.load_person(person_id)
        skill_sources = self.storage.load_skill_sources(person_id)

        if not slug:
            slug = person.slug or _make_slug(person.display_name)

        skill_dir = self.claude_dir / "skills" / f"persona-{slug}"
        skill_dir.mkdir(parents=True, exist_ok=True)

        persona_md = skill_sources.get("persona.md", "")
        style_md = skill_sources.get("style.md", "")
        examples_md = skill_sources.get("examples.md", "")

        # ── skill.md (main prompt file) ───────────────────────────────────
        skill_content = f"""# Persona Skill: {person.display_name}

{persona_md}

---

## Style Guide

{style_md}

---

## Example Exchanges

{examples_md}

---

## Usage

This skill supports three modes. Start your message with one of:

- `roleplay: <your message>` — Respond as {person.display_name} would
- `ask: <question>` — Answer questions about {person.display_name}'s views and style
- `rewrite: <text>` — Rewrite the given text in {person.display_name}'s voice

"""
        (skill_dir / "skill.md").write_text(skill_content, encoding="utf-8")

        # ── manifest.json ─────────────────────────────────────────────────
        manifest = {
            "name": f"persona-{slug}",
            "description": f"Chat, analyze, and rewrite in the style of {person.display_name}",
            "version": "1.0.0",
            "person_id": person_id,
            "slug": slug,
            "sources": [s.to_dict() for s in person.sources],
        }
        (skill_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        # ── commands.json ─────────────────────────────────────────────────
        commands = {
            "modes": {
                "roleplay": f"Respond as {person.display_name}. Stay fully in character.",
                "ask": f"Answer questions about {person.display_name}'s public persona, views, and style.",
                "rewrite": f"Rewrite the given text in the voice and style of {person.display_name}.",
            }
        }
        (skill_dir / "commands.json").write_text(
            json.dumps(commands, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        # ── also update readable source copies ───────────────────────────
        self.storage.save_skill_sources(person_id, {
            **skill_sources,
            "manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2),
            "commands.json": json.dumps(commands, ensure_ascii=False, indent=2),
        })

        print(f"[skill] Built skill at: {skill_dir}")
        print(f"[skill] In Claude Code, use: /{f'persona-{slug}'}")
        return skill_dir
