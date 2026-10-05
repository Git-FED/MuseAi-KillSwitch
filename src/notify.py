"""Best-effort Slack notification adapter; safety never depends on it."""
from __future__ import annotations
import os

def post(channel: str, text: str) -> None:
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token: print(f"[notify:no-token] {channel}: {text}"); return
    try:
        import requests
        requests.post("https://slack.com/api/chat.postMessage", headers={"Authorization": f"Bearer {token}"}, json={"channel": channel, "text": text}, timeout=5).raise_for_status()
    except Exception as exc: print(f"[notify:error] {exc}")

def dm(text: str) -> None:
    post(os.getenv("KILLSWITCH_OWNER_ID", "owner"), text)
