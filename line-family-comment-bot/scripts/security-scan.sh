#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

echo "Scanning: $ROOT"

echo
echo "1) Files that should not be committed:"
find "$ROOT" \
  \( -name '.env' -o -name 'database.sqlite' -o -name '*.sqlite' -o -name '*.db' -o -name 'config' -o -name '*.log' \) \
  -not -path '*/.git/*' \
  -print

echo
echo "2) Suspicious secret-like strings:"
SECRET_PATTERN='(Bearer [A-Za-z0-9._~+/=-]{20,}|sk-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{20,}|[A-Za-z0-9+/]{80,}={0,2})'
if command -v rg >/dev/null 2>&1; then
  rg -n --hidden --glob '!*.md' --glob '!scripts/security-scan.sh' \
    --glob '!.git/**' \
    "$SECRET_PATTERN" "$ROOT" || true
else
  grep -RInE \
    "$SECRET_PATTERN" "$ROOT" || true
fi

echo
echo "3) Suspicious strings in git history:"
if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  while IFS= read -r revision; do
    git -C "$ROOT" grep -n -I -E "$SECRET_PATTERN" "$revision" || true
  done < <(git -C "$ROOT" rev-list --all)
else
  echo "Skipped: not a git repository."
fi

echo
echo "If sections 2 and 3 are empty, no obvious long token was found."
