"""Execution-layer enforcement for queues and optional user timers."""
from __future__ import annotations
import os, subprocess, time
from pathlib import Path

# Kept static so break-glass operation does not depend on YAML parsing.
QUEUES = {"poster": os.path.expanduser("~/workspace/poster/queue"), "feed-promo": os.path.expanduser("~/workspace/feed-promo/queue")}
TIMERS = {"poster": "poster.timer", "feed-promo": "feed-promo.timer"}

def drain_queue(agent: str) -> int:
    queue = QUEUES.get(agent)
    if not queue or not os.path.isdir(queue): return 0
    drained = Path(queue) / ".drained"; drained.mkdir(exist_ok=True); count = 0
    for item in Path(queue).iterdir():
        if item.name == ".drained" or item.is_dir(): continue
        item.rename(drained / f"{int(time.time())}_{item.name}"); count += 1
    return count

def _timer(agent: str, action: str) -> bool:
    unit = TIMERS.get(agent)
    if not unit: return False
    try:
        subprocess.run(["systemctl", "--user", action, unit], check=True, timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired): return False

def stop_timer(agent: str) -> bool: return _timer(agent, "stop") and _timer(agent, "disable")
def resume_timer(agent: str) -> bool: return _timer(agent, "enable") and _timer(agent, "start")
def enforce(agent: str) -> dict: return {"agent": agent, "drained": drain_queue(agent), "timer_stopped": stop_timer(agent)}
def release(agent: str) -> dict: return {"agent": agent, "timer_resumed": resume_timer(agent), "queue_restored": False}
