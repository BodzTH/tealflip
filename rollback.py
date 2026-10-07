import subprocess
from pathlib import Path

import slots
from config import FIRST_DEPLOY


def rollback() -> None:
    if FIRST_DEPLOY:
        print("\nNothin Deployed!, Exiting Rollback.")
        return

    if slots.active == slots.rolled_back:
        print(f"\n Already rolled back to {slots.active}!")
        return

    print(f"\nRolling back to {slots.idle} slot")

    subprocess.run(
        ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
        input=f"root /var/www/{slots.idle};",
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    slots.rolled_back = slots.idle

    project_dir = Path(__file__).parent

    if "blue" == slots.rolled_back:
        slots.idle = "green"
        slots.active = "blue"
        print("\nDeploying on Blue slot.")
        print("\nBlue is Active, Green is Idle.")
    elif "green" in slots.rolled_back:
        slots.idle = "blue"
        slots.active = "green"
        print("\nDeploying on Green slot.")
        print("\nGreen is Active, Blue is Idle.")
    else:
        print("active_slot.conf in /etc/nginx/tealflip/ IS EMPTY!, Quiting.")
        return

    with open(f"{project_dir}/slots.py", "w") as file:
        file.write(
            f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"\nrolled_back: str = "{slots.rolled_back}"'
        )
