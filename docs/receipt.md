# Receipt / Demo Plan

The strongest proof is a small, reproducible receipt rather than a claim.

```bash
export KILLSWITCH_DB="$PWD/demo-state.db"
export KILLSWITCH_AUDIT="$PWD/demo-audit.log"
./bin/kill.sh status
./bin/kill.sh pause poster "demo pause"
./bin/kill.sh status
python hooks/agent_loop_example.py   # exits cleanly when pointed at poster
./bin/kill.sh revive poster
./bin/kill.sh status
```

Capture the terminal output, the active-kill transition, the clean exit, and the JSONL audit line. Do not screenshot or publish real secrets, tokens, private channels, or production identifiers.
