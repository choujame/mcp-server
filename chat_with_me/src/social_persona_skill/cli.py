from __future__ import annotations
import argparse
import sys
from pathlib import Path

from .skills import _SKILL_HOST_CHOICES


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
    bootstrap_p.add_argument(
        "platform",
        choices=["x", "xiaohongshu"],
        help="Platform to bootstrap",
    )

    login_p = backend_sub.add_parser("login", help="Authenticate a backend")
    login_p.add_argument(
        "platform",
        choices=["x", "xiaohongshu"],
        help="Platform to login",
    )

    # ── persona ───────────────────────────────────────────────────────────
    persona_p = sub.add_parser("persona", help="Manage personas")
    persona_sub = persona_p.add_subparsers(dest="persona_cmd", metavar="ACTION")

    create_p = persona_sub.add_parser("create", help="Create a new persona from URL(s)")
    create_p.add_argument("urls", nargs="+", metavar="URL", help="Social media profile URL(s)")

    attach_p = persona_sub.add_parser(
        "attach", help="Attach a new account to an existing persona"
    )
    attach_p.add_argument(
        "--person-id", required=True, metavar="ID", help="Existing persona ID"
    )
    attach_p.add_argument("url", metavar="URL", help="Social media profile URL to attach")

    _list_p = persona_sub.add_parser("list", help="List all personas")

    # ── skill ─────────────────────────────────────────────────────────────
    skill_p = sub.add_parser("skill", help="Compile Claude skills")
    skill_sub = skill_p.add_subparsers(dest="skill_cmd", metavar="ACTION")

    build_p = skill_sub.add_parser("build", help="Build a Claude skill from a persona")
    build_p.add_argument(
        "--person-id", required=True, metavar="ID", help="Persona ID to compile"
    )
    build_p.add_argument(
        "--host",
        dest="hosts",
        action="append",
        choices=_SKILL_HOST_CHOICES,
        metavar="CHOICE",
        help=(
            f"Target host(s) for skill installation "
            f"(choices: {', '.join(_SKILL_HOST_CHOICES)}; may repeat; default: claude)"
        ),
    )
    build_p.add_argument(
        "--slug",
        default=None,
        metavar="SLUG",
        help="Override skill slug",
    )

    return parser


# ── command handlers ──────────────────────────────────────────────────────────


def _cmd_backend_bootstrap(args) -> None:
    from .runtime import RuntimeLayout
    from .models import Platform
    layout = RuntimeLayout(Path(args.runtime_root))
    layout.bootstrap(Platform(args.platform))


def _cmd_backend_login(args) -> None:
    from .runtime import RuntimeLayout
    from .models import Platform
    layout = RuntimeLayout(Path(args.runtime_root))
    layout.login(Platform(args.platform))


def _cmd_persona_create(args) -> None:
    from .workflow import PersonaWorkflow
    wf = PersonaWorkflow(
        storage_dir=Path(args.storage_dir),
        runtime_root=Path(args.runtime_root),
        claude_dir=Path(args.claude_dir),
    )
    result, person_dir = wf.create_persona(args.urls)
    person = result.person
    print(f"\nPersona created!")
    print(f"   ID:   {person.person_id}")
    print(f"   Name: {person.persona_name}")
    print(f"   Dir:  {person_dir}")
    print(f"\nNext step — build the Claude skill:")
    print(
        f"   python -m social_persona_skill.cli"
        f" --runtime-root {args.runtime_root}"
        f" --storage-dir {args.storage_dir}"
        f" --claude-dir {args.claude_dir}"
        f" skill build --person-id {person.person_id}"
    )


def _cmd_persona_attach(args) -> None:
    from .workflow import PersonaWorkflow
    wf = PersonaWorkflow(
        storage_dir=Path(args.storage_dir),
        runtime_root=Path(args.runtime_root),
        claude_dir=Path(args.claude_dir),
    )
    result = wf.attach_account(args.person_id, args.url)
    print(f"\nAccount attached to persona {result.person.person_id}")


def _cmd_persona_list(args) -> None:
    from .storage import PersonaStorage
    storage = PersonaStorage(Path(args.storage_dir))
    persons = storage.list_persons()
    if not persons:
        print("No personas found.")
        return
    print(f"{'ID':<14} {'Name':<30} {'Accounts'}")
    print("-" * 80)
    for p in persons:
        accts = ", ".join(
            f"{a.platform}:{a.profile_id}" for a in p.accounts
        )
        print(f"{p.person_id:<14} {p.persona_name:<30} {accts}")


def _cmd_skill_build(args) -> None:
    from .workflow import PersonaWorkflow
    wf = PersonaWorkflow(
        storage_dir=Path(args.storage_dir),
        runtime_root=Path(args.runtime_root),
        claude_dir=Path(args.claude_dir),
    )
    hosts = args.hosts or ["claude"]
    result = wf.build_skill(
        args.person_id,
        hosts=hosts,
        slug=args.slug,
    )
    skill_name = result.skill_name
    print(f"\nSkill compiled to: {result.installed_skill_dir}")
    print(f"\nIn Claude Code, use:")
    print(f"   /{skill_name}")
    print(f"   roleplay: <your message>")
    print(f"   ask: <question about this persona>")
    print(f"   rewrite: <text to rewrite in their style>")


# ── main ──────────────────────────────────────────────────────────────────────


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
