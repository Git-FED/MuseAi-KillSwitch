"""Append-only JSONL audit receipts."""
from __future__ import annotations
import json, os, time
from typing import Any

AUDIT_PATH = os.environ.get("KILLSWITCH_AUDIT", os.path.expanduser("~/workspace/killswitch/audit.log"))
EVENTS = {"kill", "revive", "budget_action", "break_glass"}

def record(event: str, actor: str, scope: str, target: str | None, level: str = "", reason: str = "", extra: dict[str, Any] | None = None) -> None:
    if event not in EVENTS: raise ValueError(f"event must be one of {sorted(EVENTS)}")
    path = os.path.abspath(os.path.expanduser(AUDIT_PATH)); os.makedirs(os.path.dirname(path), exist_ok=True)
    entry = {"ts": time.time(), "event": event, "actor": actor, "scope": scope, "target": target, "level": level, "reason": reason, "extra": extra or {}}
    with open(path, "a", encoding="utf-8") as fh: fh.write(json.dumps(entry, sort_keys=True) + "\n")

def tail(n: int = 20) -> list[dict[str, Any]]:
    if not os.path.exists(os.path.expanduser(AUDIT_PATH)): return []
    with open(os.path.expanduser(AUDIT_PATH), encoding="utf-8") as fh: lines = fh.readlines()[-n:]
    return [json.loads(line) for line in lines if line.strip()]
