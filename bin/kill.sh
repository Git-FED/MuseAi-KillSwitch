#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; export PYTHONPATH="$ROOT:${PYTHONPATH:-}"; export KILLSWITCH_DB="${KILLSWITCH_DB:-$ROOT/state.db}"; export KILLSWITCH_AUDIT="${KILLSWITCH_AUDIT:-$ROOT/audit.log}"
python3 - "$@" <<'PY'
import os, sys
from src import state, audit
state.init_db(); args=sys.argv[1:]
if not args or args[0] == 'status':
    active=state.list_active_kills(); print('ACTIVE KILLS' if active else 'CLEAR — no active kills')
    for k in active: print(f'[{k.level}] {k.scope}:{k.target or "*"} by {k.actor} — {k.reason}')
elif args[0] == 'kill-all':
    args = ['kill', 'all'] + args[1:]
    target=args[1]; reason=' '.join(args[2:]) or 'operator action'; level='KILL'; scope='global'
    answer=os.getenv('KILLSWITCH_CONFIRM') or input('Type KILL ALL to confirm: '); assert answer=='KILL ALL', 'not confirmed'
    ident=state.kill(scope, None, level, 'break-glass', reason); audit.record('break_glass','break-glass',scope,None,level,reason); print(f'activated kill #{ident}')
elif args[0] in ('kill','pause') and len(args) >= 2:
    target=args[1]; reason=' '.join(args[2:]) or 'operator action'; level='KILL' if args[0]=='kill' else 'PAUSE'; scope='global' if target=='all' else 'agent'
    if scope=='global':
        answer=input('Type KILL ALL to confirm: '); assert answer=='KILL ALL', 'not confirmed'
    ident=state.kill(scope, None if scope=='global' else target, level, 'break-glass', reason); audit.record('break_glass','break-glass',scope,None if scope=='global' else target,level,reason); print(f'activated kill #{ident}')
elif args[0]=='revive' and len(args)==2:
    target=args[1]; changed=state.revive('global' if target=='all' else 'agent', None if target=='all' else target, 'break-glass'); audit.record('revive','break-glass','global' if target=='all' else 'agent',None if target=='all' else target,reason='manual revive'); print(f'revoked {changed} active kill(s)')
else: raise SystemExit('usage: kill.sh [status|kill <agent>|kill-all <reason>|pause <agent>|revive <agent>]')
PY
