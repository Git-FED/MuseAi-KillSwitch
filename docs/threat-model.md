# Threat Model

| Threat | Control | Residual risk |
|---|---|---|
| Agent ignores an in-process flag | State is external and checked each loop | Long-running single tool call may finish before the next check |
| Agent tries to revive itself | Revive is an operator/CLI action, not agent API | Host compromise can bypass file permissions |
| Slack is down | Network-free break-glass CLI | Operator needs host access |
| Database is unavailable | Guard fails closed | Agents remain unavailable until storage recovers |
| Budget runaway | Thresholds pause and notify | Usage telemetry must be accurate |
| Stale queue executes later | Scheduler enforcement plus queue drain | External schedulers require correct mapping |
| Audit tampering | Append-only JSONL and restricted permissions | Local root can alter any local file |

This suite reduces blast radius; it does not replace host hardening, least privilege, secret rotation, or a production incident-response program.
