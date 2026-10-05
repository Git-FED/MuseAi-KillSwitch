.PHONY: test demo clean

test:
python -m pytest -q

demo:
KILLSWITCH_DB=$(CURDIR)/demo-state.db KILLSWITCH_AUDIT=$(CURDIR)/demo-audit.log ./bin/kill.sh status

clean:
rm -f demo-state.db demo-audit.log state.db state.db-*
