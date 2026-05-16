from __future__ import annotations
import os
import json
import re
from typing import List, Optional
from pathlib import Path

from .models import CorpusEntry, Person


def _read_oauth_token() -> Optional[str]:
    fd_str = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR")
    if not fd_str:
        return os.environ.get("ANTHROPIC_API_KEY")
    try:
        with open(f"/proc/self/fd/{fd_str}", "r") as f:
            return f.read().strip()
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY")


def _call_claude(prompt: str, system: str = "", max_tokens: int = 4096) -> str:
    import requests as _req
    token = _read_oauth_token()
    if not token:
        raise RuntimeError("No Anthropic API key found. Set ANTHROPIC_API_KEY or run inside Claude Code.")
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
    resp = _req.post(f"{base_url}/v1/messages", headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def _corpus_sample(corpus: List[CorpusEntry], max_chars: int = 12000) -> str:
    texts = []
    total = 0
    for e in corpus:
        if total + len(e.text) > max_chars:
            break
        texts.append(f"[{e.platform}] {e.text}")
        total += len(e.text)
    return "\n\n---\n\n".join(texts)


def generate_persona_files(person: Person, corpus: List[CorpusEntry]) -> dict:
    sample = _corpus_sample(corpus)
    platform_list = list({s.platform for s in person.sources})

    system = (
        "You are an expert persona analyst. Given a corpus of posts from a social media user, "
        "you extract their personality, writing style, opinions, and characteristic expressions. "
        "Be specific and data-driven. Output only the requested format."
    )

    # ── profile.md ───────────────────────────────────────────────────────
    profile_prompt = f"""Analyze the following social media posts from user "{person.display_name}" and write a comprehensive profile.md.

Platform(s): {', '.join(platform_list)}

CORPUS SAMPLE:
{sample}

Write profile.md in this structure:
# {person.display_name}

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

Write in objective third-person analysis style."""

    profile_md = _call_claude(profile_prompt, system=system)

    # ── persona.md ────────────────────────────────────────────────────────
    persona_prompt = f"""Based on this profile analysis of "{person.display_name}":

{profile_md}

Write a persona.md that Claude can use to roleplay as this person. It should be in second person ("You are...") and describe:
- Identity and background
- Core values and worldview
- Characteristic way of thinking
- Topics of expertise and passion
- Communication style and voice
- What they would and wouldn't say
- Emotional register

Keep it to ~400 words. Write as if giving Claude a character briefing."""

    persona_md = _call_claude(persona_prompt, system=system)

    # ── style.md ──────────────────────────────────────────────────────────
    style_prompt = f"""Analyze the writing style of "{person.display_name}" from these posts:

{sample[:6000]}

Write style.md covering:
# Writing Style Guide: {person.display_name}

## Sentence Structure
[typical sentence length, complexity, rhythm]

## Vocabulary
[formal/informal, technical terms, slang, language preferences]

## Tone
[emotional register, humor, seriousness, irony]

## Formatting Habits
[use of line breaks, lists, emoji, punctuation quirks]

## Rhetorical Patterns
[how they make arguments, tell stories, ask questions]

## Do's and Don'ts
[specific things to do / avoid to sound like them]"""

    style_md = _call_claude(style_prompt, system=system)

    # ── examples.md ──────────────────────────────────────────────────────
    examples_prompt = f"""You are preparing training examples for roleplaying as "{person.display_name}".

Using their real posts as inspiration, create examples.md with 5 example exchanges showing how they would respond in different situations.

Format each as:
### Example N: [topic]
**User**: [question or prompt]
**{person.display_name}**: [response in their voice]

Topics to cover: 1) their main area of expertise, 2) casual conversation, 3) controversial opinion, 4) advice request, 5) something they're passionate about.

Real posts for reference:
{sample[:4000]}"""

    examples_md = _call_claude(examples_prompt, system=system)

    return {
        "profile.md": profile_md,
        "persona.md": persona_md,
        "style.md": style_md,
        "examples.md": examples_md,
    }
