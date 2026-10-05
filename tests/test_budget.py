def test_budget_only_pauses(tmp_path, monkeypatch):
    db=tmp_path/'state.db'; monkeypatch.setenv('KILLSWITCH_DB', str(db))
    from src import state, budget
    state.DB_PATH=str(db); state.init_db(); budget.reset(); actions=budget.check_and_act(8.0)
    assert {a['action'] for a in actions} == {'notify','pause_non_essential'}
    assert state.is_killed('poster').level == 'PAUSE'
