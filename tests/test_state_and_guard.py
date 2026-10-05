import os
from pathlib import Path

def test_scoped_and_global_kills(tmp_path, monkeypatch):
    db=tmp_path/'state.db'; monkeypatch.setenv('KILLSWITCH_DB', str(db))
    from src import state
    from src.guard import KilledError, check_kill
    state.DB_PATH=str(db); state.init_db(); state.kill('agent','poster','KILL','test','bad write')
    try: check_kill('poster'); assert False
    except KilledError: pass
    check_kill('muse2')
    state.kill('global',None,'STOP','test','fleet pause')
    try: check_kill('muse2'); assert False
    except KilledError: pass
    assert len(state.list_active_kills()) == 2

def test_revive(tmp_path, monkeypatch):
    db=tmp_path/'state.db'; monkeypatch.setenv('KILLSWITCH_DB', str(db))
    from src import state
    state.DB_PATH=str(db); state.init_db(); state.kill('agent','poster','PAUSE','test','pause'); assert state.revive('agent','poster','test') == 1; assert state.is_killed('poster') is None
