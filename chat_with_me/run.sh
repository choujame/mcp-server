#!/usr/bin/env bash
# chat_with_me CLI wrapper
# Usage: ./run.sh [options] COMMAND [args...]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHONPATH="$SCRIPT_DIR/src" exec python3 -m social_persona_skill.cli "$@"
