from pathlib import Path

import slots
from config import INITIALIZED
from switch import switch


def rollback() -> None:
    if not INITIALIZED:
        print("\nTealFlip is not Initialized!, Exiting Rollback.")
        return

    try:
        idle_ref = (
            Path(f"/var/www/{slots.idle}/.git/refs/heads/main").read_text().strip("\n")
        )
    except FileNotFoundError:
        print("Can not rollback!, Nothing were deployed to idle slot.")
        return

    if slots.last_bad_commit == idle_ref:
        print("Can not rollback to a bad commit!, Quiting.")
        return

    switch(False)
