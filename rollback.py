from pathlib import Path

import slots
from config import INITIALIZED
from switch import switch


def rollback() -> None:
    if not INITIALIZED:
        print("\nTealFlip is not Initialized!, Exiting Rollback.")
        return

    idle_ref = (
        Path(f"/var/www/{slots.idle}/.git/refs/heads/main").read_text().strip("\n")
    )

    if slots.last_bad_commit == idle_ref:
        print("Can not rollback to a bad commit!, Quiting.")
        return

    print(f"\nRolling back from {slots.active} slot to {slots.idle}")

    slots.last_bad_commit = (
        Path(f"/var/www/{slots.active}/.git/refs/heads/main").read_text().strip("\n")
    )

    if switch(slots.idle):
        print(f"\nSwitching to {slots.idle} Succeeded.")

    else:
        print(f"\nSwitching to {slots.idle} Failed!")
        return
