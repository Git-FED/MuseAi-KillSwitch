"""Fail-closed run-loop guard."""
from __future__ import annotations
import functools
from .state import is_killed

class KilledError(RuntimeError):
    def __init__(self, agent: str, kill):
        super().__init__(f"agent '{agent}' blocked: {kill.level} ({kill.reason or 'no reason'})")
        self.agent, self.kill = agent, kill

def check_kill(agent: str) -> None:
    # Do not catch database errors. A missing/locked state store must halt work.
    current = is_killed(agent)
    if current is not None: raise KilledError(agent, current)

def guarded(agent: str):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            check_kill(agent)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
