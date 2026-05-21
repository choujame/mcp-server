from __future__ import annotations
import os
import json
from typing import Iterable, List, Optional
import time

from .models import (
    PersonRecord,
    CorpusRecord,
    CollectedAccount,
    StoredPersona,
    SourceRecord,
    AccountRecord,
)


# ── Claude API helpers ────────────────────────────────────────────────────────


def _read_oauth_token() -> Optional[str]:
    fd_str = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR")
    if fd_str:
        try:
            with open(f"/proc/self/fd/{fd_str}", "r") as f:
                return f.read().strip()
        except Exception:
            pass
    token_file = os.environ.get("CLAUDE_SESSION_INGRESS_TOKEN_FILE")
    if token_file:
        try:
            with open(token_file, "r") as f:
                return f.read().strip()
        except Exception:
            pass
    return os.environ.get("ANTHROPIC_API_KEY")


def _call_claude(prompt: str, system: str = "", max_tokens: int = 4096) -> str:
    import requests as _req
    token = _read_oauth_token()
    if not token:
        raise RuntimeError(
            "No Anthropic API key found. Set ANTHROPIC_API_KEY or run inside Claude Code."
        )
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    headers = {
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
    }
    payload: dict = {
        "model": "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        payload["system"] = system
    resp = _req.post(
        f"{base_url}/v1/messages",
        headers=headers,
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


# ── corpus helpers ────────────────────────────────────────────────────────────


def _corpus_sample(corpus: List[CorpusRecord], max_chars: int = 12000) -> str:
    texts = []
    total = 0
    for e in corpus:
        if total + len(e.text) > max_chars:
            break
        texts.append(f"[{e.platform}] {e.text}")
        total += len(e.text)
    return "\n\n---\n\n".join(texts)


def _display_name_from_accounts(accounts: List[AccountRecord]) -> str:
    if accounts:
        return accounts[0].display_name or accounts[0].profile_id
    return "Unknown"


# ── PersonaDistiller ──────────────────────────────────────────────────────────


class PersonaDistiller:
    """Uses Claude API to distill corpus into a persona markdown."""

    def create_person(
        self,
        collections: Iterable[CollectedAccount],
    ) -> tuple[PersonRecord, str]:
        """
        Given collected accounts, create a new PersonRecord and generate
        persona markdown. Returns (PersonRecord, markdown_str).
        """
        collections = list(collections)
        all_corpus: List[CorpusRecord] = []
        accounts: List[AccountRecord] = []
        for c in collections:
            accounts.append(c.account)
            all_corpus.extend(c.corpus)

        person = PersonRecord(
            accounts=accounts,
            persona_name=_display_name_from_accounts(accounts),
        )
        markdown = self._generate_markdown(person, all_corpus)
        return person, markdown

    def attach_accounts(
        self,
        stored: StoredPersona,
        collections: Iterable[CollectedAccount],
        extra_corpus: Optional[List[CorpusRecord]] = None,
    ) -> tuple[PersonRecord, str]:
        """
        Attach new accounts to an existing StoredPersona and regenerate markdown.
        Returns (updated PersonRecord, new markdown_str).
        """
        collections = list(collections)
        all_corpus: List[CorpusRecord] = list(extra_corpus or [])
        for c in collections:
            stored.person.accounts.append(c.account)
            all_corpus.extend(c.corpus)

        stored.person.touch()
        markdown = self._generate_markdown(stored.person, all_corpus)
        return stored.person, markdown

    def _generate_markdown(self, person: PersonRecord, corpus: List[CorpusRecord]) -> str:
        display_name = person.persona_name or _display_name_from_accounts(person.accounts)
        sample = _corpus_sample(corpus)
        platforms = list({str(r.platform) for r in corpus})

        system = (
            "You are an expert persona analyst. Given a corpus of social media posts, "
            "extract the person's personality, writing style, opinions, and characteristic expressions. "
            "Be specific and data-driven. Output only the requested Markdown."
        )

        prompt = f"""Analyze the following social media posts from "{display_name}" and write a comprehensive persona profile.

Platform(s): {', '.join(platforms) if platforms else 'unknown'}

CORPUS SAMPLE:
{sample}

Write the persona profile in this Markdown structure:

# {display_name}

## Overview
[2-3 sentence summary of who this person is]

## Core Topics
[bullet list of main topics they post about]

## Personality Traits
[bullet list of personality characteristics]

## Communication Style
[how they write: tone, vocabulary, sentence structure]

## Recurring Themes
[ideas or viewpoints that appear repeatedly]

## Notable Phrases / Expressions
[characteristic phrases, sentence starters, or expressions they use]

## Roleplay Guidance
[In second person — "You are..." — instructions for Claude to embody this persona]

Write in objective, analysis style for the sections above Overview through Notable Phrases,
then switch to direct second-person instructions for the Roleplay Guidance section.
"""
        return _call_claude(prompt, system=system)
