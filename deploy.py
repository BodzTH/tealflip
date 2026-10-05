import subprocess
from pathlib import Path

import slots
from config import FIRST_DEPLOY, PROJECT_PATH


def deploy() -> None:
    if FIRST_DEPLOY:
        print("\nFirst Deploy!, Deploying on Blue slot.")
        subprocess.run(
            ["rsync", "-a", "--delete", f"{PROJECT_PATH}/", f"/var/www/{slots.active}"],
            stdout=subprocess.DEVNULL,
            text=True,
            check=True,
        )
        subprocess.run(
            ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{slots.active}",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        # return
    try:
        active_slot = Path("/etc/nginx/tealflip/active_slot.conf").read_text()
    except FileNotFoundError:
        print("active_slot.conf in /etc/nginx/tealflip/ DOES Not Exist")
    project_dir = Path(__file__).parent
    if "blue" in active_slot:
        slots.idle = "blue"
        slots.active = "green"
        print("\nDeploying on Green slot.")
        print("\nGreen is Active, Blue is Idle.")
    elif "green" in active_slot:
        slots.idle = "green"
        slots.active = "blue"
        print("\nDeploying on Blue slot.")
        print("\nBlue is Active, Green is Idle.")

    subprocess.run(
        ["rsync", "-a", "--delete", f"{PROJECT_PATH}/", f"/var/www/{slots.active}"],
        stdout=subprocess.DEVNULL,
        text=True,
        check=True,
    )

    subprocess.run(
        ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
        input=f"root /var/www/{slots.active}",
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )

    with open(f"{project_dir}/slots.py", "w") as file:
        file.write(f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"')
