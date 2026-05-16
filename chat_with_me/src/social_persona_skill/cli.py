from __future__ import annotations
import argparse
import sys
from pathlib import Path


def _make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m social_persona_skill.cli",
        description="chat_with_me — Persona Skill builder from social media",
    )
    parser.add_argument(
        "--runtime-root",
        default=".runtime",
        metavar="DIR",
        help="Root directory for runtime state (default: .runtime)",
    )
    parser.add_argument(
        "--storage-dir",
        default="personas",
        metavar="DIR",
        help="Directory for persona storage (default: personas)",
    )
    parser.add_argument(
        "--claude-dir",
        default=".claude",
        metavar="DIR",
        help="Claude Code directory for skill output (default: .claude)",
    )

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ── backend ───────────────────────────────────────────────────────────
    backend_p = sub.add_parser("backend", help="Manage collection backends")
    backend_sub = backend_p.add_subparsers(dest="backend_cmd", metavar="ACTION")

    bootstrap_p = backend_sub.add_parser("bootstrap", help="Install a backend")
    bootstrap_p.add_argument("platform", choices=["x", "xiaohongshu"], help="Platform to bootstrap")

    login_p = backend_sub.add_parser("login", help="Authenticate a backend")
    login_p.add_argument("platform", choices=["x", "xiaohongshu"], help="Platform to login")

    # ── persona ───────────────────────────────────────────────────────────
    persona_p = sub.add_parser("persona", help="Manage personas")
    persona_sub = persona_p.add_subparsers(dest="persona_cmd", metavar="ACTION")

    create_p = persona_sub.add_parser("create", help="Create a new persona from URL(s)")
    create_p.add_argument("urls", nargs="+", metavar="URL", help="Social media profile URL(s)")

    attach_p = persona_sub.add_parser("attach", help="Attach a new account to an existing persona")
    attach_p.add_argument("--person-id", required=True, metavar="ID", help="Existing persona ID")
    attach_p.add_argument("url", metavar="URL", help="Social media profile URL to attach")

    list_p = persona_sub.add_parser("list", help="List all personas")

    # ── skill ─────────────────────────────────────────────────────────────
    skill_p = sub.add_parser("skill", help="Compile Claude skills")
    skill_sub = skill_p.add_subparsers(dest="skill_cmd", metavar="ACTION")

    build_p = skill_sub.add_parser("build", help="Build a Claude skill from a persona")
    build_p.add_argument("--person-id", required=True, metavar="ID", help="Persona ID to compile")
    build_p.add_argument("--slug", default=None, metavar="SLUG", help="Override skill slug")

    return parser


def _cmd_backend_bootstrap(args) -> None:
    from .runtime import RuntimeManager
    runtime = RuntimeManager(Path(args.runtime_root))
    runtime.bootstrap(args.platform)


def _cmd_backend_login(args) -> None:
    from .runtime import RuntimeManager
    runtime = RuntimeManager(Path(args.runtime_root))
    runtime.login(args.platform)


def _cmd_persona_create(args) -> None:
    from .workflow import create_persona
    person = create_persona(
        urls=args.urls,
        runtime_root=Path(args.runtime_root),
        storage_dir=Path(args.storage_dir),
        claude_dir=Path(args.claude_dir),
    )
    print(f"\n✅ Persona created!")
    print(f"   ID:   {person.id}")
    print(f"   Name: {person.display_name}")
    print(f"   Slug: {person.slug}")
    print(f"\nNext step — build the Claude skill:")
    print(f"   python -m social_persona_skill.cli --runtime-root {args.runtime_root} --storage-dir {args.storage_dir} skill build --person-id {person.id}")


def _cmd_persona_attach(args) -> None:
    from .workflow import attach_account
    person = attach_account(
        person_id=args.person_id,
        url=args.url,
        runtime_root=Path(args.runtime_root),
        storage_dir=Path(args.storage_dir),
    )
    print(f"\n✅ Account attached to persona {person.id}")


def _cmd_persona_list(args) -> None:
    from .storage import PersonaStorage
    storage = PersonaStorage(Path(args.storage_dir))
    persons = storage.list_persons()
    if not persons:
        print("No personas found.")
        return
    print(f"{'ID':<14} {'Slug':<25} {'Name':<30} {'Sources'}")
    print("-" * 80)
    for p in persons:
        srcs = ", ".join(f"{s.platform}:{s.account_slug}" for s in p.sources)
        print(f"{p.id:<14} {p.slug:<25} {p.display_name:<30} {srcs}")


def _cmd_skill_build(args) -> None:
    from .workflow import build_skill
    skill_dir = build_skill(
        person_id=args.person_id,
        storage_dir=Path(args.storage_dir),
        claude_dir=Path(args.claude_dir),
        slug=args.slug,
    )
    slug = skill_dir.name.removeprefix("persona-")
    print(f"\n✅ Skill compiled to: {skill_dir}")
    print(f"\nIn Claude Code, use:")
    print(f"   /persona-{slug}")
    print(f"   roleplay: <your message>")
    print(f"   ask: <question about this persona>")
    print(f"   rewrite: <text to rewrite in their style>")


def main(argv=None) -> None:
    parser = _make_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "backend":
            if args.backend_cmd == "bootstrap":
                _cmd_backend_bootstrap(args)
            elif args.backend_cmd == "login":
                _cmd_backend_login(args)
            else:
                parser.parse_args(["backend", "--help"])

        elif args.command == "persona":
            if args.persona_cmd == "create":
                _cmd_persona_create(args)
            elif args.persona_cmd == "attach":
                _cmd_persona_attach(args)
            elif args.persona_cmd == "list":
                _cmd_persona_list(args)
            else:
                parser.parse_args(["persona", "--help"])

        elif args.command == "skill":
            if args.skill_cmd == "build":
                _cmd_skill_build(args)
            else:
                parser.parse_args(["skill", "--help"])

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
