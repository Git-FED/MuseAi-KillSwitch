"""Minimal integration pattern: place check_kill at the top of every loop."""
import time
from src.guard import KilledError, check_kill

def run(agent_name: str):
    while True:
        try: check_kill(agent_name)
        except KilledError as stop:
            print(f"clean exit: {stop}"); return
        print(f"{agent_name}: safe iteration")
        time.sleep(1)

if __name__ == '__main__': run('poster')
