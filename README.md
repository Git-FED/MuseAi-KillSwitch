# Muse Kill Switch Suite

<img width="2560" height="1440" alt="fed-kill-switch-panic" src="https://github.com/user-attachments/assets/91a4acb7-891c-437d-b212-54184bb1b68b" />

> A defense-in-depth control plane for autonomous agents: external state, fail-closed guards, budget tripwires, queue enforcement, audit receipts, and a beautiful operator reference site.

**Status:** runnable reference implementation · **Python:** 3.10+ · **State:** SQLite · **UI:** standalone HTML · **macOS:** deliberately excluded from wrapper targets

## What is included

| Surface | Purpose |
|---|---|
| `src/` | External SQLite-backed kill state, guards, budgets, audit logging, scheduler enforcement, and best-effort notifications |
| `bin/kill.sh` | Network-free break-glass CLI |
| `config/` | Explicit fleet, essential-agent, and budget policy registries |
| `hooks/` | Copy-ready examples for adding fail-closed checks to agent loops |
| `docs/` | Operator runbook, threat model, and receipt/demo plan |
| `site/` | Eye-catching, printable HTML build reference with copy buttons and responsive navigation |
| `site/*.html` | Support tab, plain-language legal drafts, accessibility statement, and gated private-communities flow |
| `web2app/` | Detailed prompts and repository blueprint for Android, iOS, Windows, Linux, and PWA packaging — no macOS target |
| favicon kit | `favicon.svg`, manifest, browser config, and reproducible generation script |

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
export KILLSWITCH_DB="$PWD/state.db"
python -m src.state --init
./bin/kill.sh status
pytest -q
```

## Operator commands

```bash
./bin/kill.sh kill poster "unsafe outbound behavior"
./bin/kill.sh pause feed-promo "budget threshold"
./bin/kill.sh status
./bin/kill.sh revive poster
./bin/kill.sh kill-all "emergency stop"   # explicit confirmation required
```

For a visual reference, open `site/index.html` directly in a browser. It has no build step and works from `file://`.

## Safety invariants

1. Kill state lives outside each agent process; an agent cannot override its own stop signal.
2. Slack, CLI, and budget paths share one SQLite source of truth.
3. Global state supersedes agent state.
4. Every transition is recorded in append-only JSONL audit output.
5. Guard checks fail closed: database errors halt the agent rather than allowing work to continue.
6. Revive is deliberate and separately audited.
7. Budget automation can pause, but never autonomously issue a hard `KILL`.
8. Queued work is drained to an auditable directory, never silently deleted.

## Important deployment note

This is a reference implementation, not a substitute for a production security review. Put the database on durable storage, restrict who can execute the break-glass script, and test the kill path during a controlled incident drill before connecting it to real agents.
