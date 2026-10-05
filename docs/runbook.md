# Operator Runbook

## Incident sequence

1. Use `./bin/kill.sh status` to establish the current state.
2. For one agent: `./bin/kill.sh kill poster "reason"`.
3. For fleet panic: `./bin/kill.sh kill all "reason"`, then type `KILL ALL`.
4. Verify the target loop exits. Inspect `audit.log`.
5. Drain or preserve queued work; never delete it during an incident.
6. Investigate, document the decision, and revive only after a deliberate review.

## Drill checklist

- [ ] Run the drill in a non-production workspace.
- [ ] Confirm global kill blocks every agent.
- [ ] Confirm a scoped kill leaves unrelated agents running.
- [ ] Rename or lock the database temporarily and verify the guard fails closed.
- [ ] Confirm notifications may fail without weakening the state transition.
- [ ] Confirm revives are separately recorded.

## Recovery rule

A revive restores permission to run; it does not restore queued work automatically. Queue replay must be an explicit, reviewed action.
