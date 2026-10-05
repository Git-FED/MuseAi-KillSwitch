#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
python3 -m venv .venv; . .venv/bin/activate; pip install -e '.[test]'; python -m src.state --init
printf 'Initialized %s\n' "$ROOT/state.db"
printf 'Next: copy .env.example to .env, then add check_kill(agent) to each run loop.\n'
