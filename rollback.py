from pathlib import Path

import slots
from config import INITIALIZED
from switch import switch


def rollback() -> None:
    if not INITIALIZED:
        print("\nTealFlip is not Initialized!, Exiting Rollback.")
        return

    project_dir = Path(__file__).parent

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

    print(f"\nDeploying on {slots.idle.capitalize()} slot.")
    print(f"\n{slots.idle.capitalize()} is Active, {slots.idle.capitalize()} is Idle.")

    with open(f"{project_dir}/slots.py", "w") as file:
        file.write(
            f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"\nlast_good_commit: str = "{slots.last_good_commit}"\nlast_bad_commit: str = "{slots.last_bad_commit}"'
        )
