"""Budget tripwire: automation may pause, never hard-kill."""
from __future__ import annotations
import os, yaml
from . import audit, notify, scheduler, state

ROOT = os.path.dirname(os.path.dirname(__file__))
_fired: set[float] = set()

def _load(name):
    with open(os.path.join(ROOT, "config", name), encoding="utf-8") as fh: return yaml.safe_load(fh)

def reset(): _fired.clear()

def check_and_act(usage_pct: float, actor: str = "budget-tripwire") -> list[dict]:
    thresholds = sorted(_load("thresholds.yaml")["thresholds"], key=lambda x: x["pct"])
    agents = _load("agents.yaml")["agents"]; essential = set(_load("essential.yaml")["essential"]); actions = []
    for threshold in thresholds:
        pct, action = float(threshold["pct"]), threshold["action"]
        if usage_pct < pct or pct in _fired: continue
        _fired.add(pct); summary = {"threshold": pct, "action": action, "usage_pct": usage_pct}
        if action == "notify":
            notify.post(threshold.get("channel", "#muse-linkup"), f"Budget notice: usage crossed {pct:.1f}% ({usage_pct:.1f}%).")
        elif action == "pause_non_essential":
            for item in agents:
                if item["name"] in essential: continue
                state.kill("agent", item["name"], "PAUSE", actor, f"budget crossed {pct:.1f}%"); scheduler.enforce(item["name"])
            notify.post(threshold.get("channel", "#muse-linkup"), f"Paused non-essential agents at {usage_pct:.1f}% usage.")
        elif action == "pause_all_and_prompt_kill":
            for item in agents:
                state.kill("agent", item["name"], "PAUSE", actor, f"budget crossed {pct:.1f}%"); scheduler.enforce(item["name"])
            message = f"Paused all agents at {usage_pct:.1f}% usage. Reply /kill all to escalate."
            notify.post(threshold.get("channel", "#muse-linkup"), message)
            if threshold.get("dm"): notify.dm(message)
        audit.record("budget_action", actor, "global", None, "PAUSE", action, summary); actions.append(summary)
    return actions
