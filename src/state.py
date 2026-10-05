"""External, SQLite-backed source of truth for kill state.

No agent should hold a private kill flag in process memory. If this module cannot
read state, callers must stop: the guard intentionally fails closed.
"""
from __future__ import annotations
import argparse, os, sqlite3, time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional

DB_PATH = os.environ.get("KILLSWITCH_DB", os.path.expanduser("~/workspace/killswitch/state.db"))
SCHEMA = """
CREATE TABLE IF NOT EXISTS kills (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 scope TEXT NOT NULL CHECK(scope IN ('global','agent')),
 target TEXT,
 level TEXT NOT NULL CHECK(level IN ('PAUSE','STOP','KILL')),
 actor TEXT NOT NULL,
 reason TEXT NOT NULL DEFAULT '',
 created_at REAL NOT NULL,
 revoked_at REAL,
 revoked_by TEXT
);
CREATE INDEX IF NOT EXISTS idx_active ON kills(scope, target) WHERE revoked_at IS NULL;
"""

@dataclass(frozen=True)
class Kill:
    id: int
    scope: str
    target: Optional[str]
    level: str
    actor: str
    reason: str
    created_at: float

@contextmanager
def _conn():
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db() -> None:
    parent = os.path.dirname(os.path.abspath(os.path.expanduser(DB_PATH)))
    os.makedirs(parent, exist_ok=True)
    with _conn() as conn:
        conn.executescript(SCHEMA)

def kill(scope: str, target: Optional[str], level: str, actor: str, reason: str = "") -> int:
    if scope not in {"global", "agent"}: raise ValueError("scope must be global or agent")
    if level not in {"PAUSE", "STOP", "KILL"}: raise ValueError("invalid level")
    if scope == "agent" and not target: raise ValueError("agent kills require target")
    with _conn() as conn:
        cur = conn.execute("INSERT INTO kills(scope,target,level,actor,reason,created_at) VALUES (?,?,?,?,?,?)", (scope, target, level, actor, reason, time.time()))
        return int(cur.lastrowid)

def revive(scope: str, target: Optional[str], actor: str) -> int:
    if scope not in {"global", "agent"}: raise ValueError("scope must be global or agent")
    with _conn() as conn:
        if scope == "global":
            cur = conn.execute("UPDATE kills SET revoked_at=?, revoked_by=? WHERE scope='global' AND revoked_at IS NULL", (time.time(), actor))
        else:
            if not target: raise ValueError("agent revive requires target")
            cur = conn.execute("UPDATE kills SET revoked_at=?, revoked_by=? WHERE scope='agent' AND target=? AND revoked_at IS NULL", (time.time(), actor, target))
        return cur.rowcount

def is_killed(agent: str) -> Optional[Kill]:
    with _conn() as conn:
        row = conn.execute("SELECT id,scope,target,level,actor,reason,created_at FROM kills WHERE revoked_at IS NULL AND (scope='global' OR (scope='agent' AND target=?)) ORDER BY CASE WHEN scope='global' THEN 0 ELSE 1 END, created_at DESC LIMIT 1", (agent,)).fetchone()
        return Kill(**dict(row)) if row else None

def list_active_kills() -> list[Kill]:
    with _conn() as conn:
        return [Kill(**dict(row)) for row in conn.execute("SELECT id,scope,target,level,actor,reason,created_at FROM kills WHERE revoked_at IS NULL ORDER BY created_at DESC")]

class KillState:
    init = staticmethod(init_db)
    kill = staticmethod(kill)
    revive = staticmethod(revive)
    is_killed = staticmethod(is_killed)
    active = staticmethod(list_active_kills)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect the external kill state")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()
    if args.init: init_db(); print(f"initialized {os.path.abspath(os.path.expanduser(DB_PATH))}")
    if args.show:
        for item in list_active_kills(): print(f"[{item.level}] {item.scope}:{item.target or '*'} by {item.actor} — {item.reason}")
