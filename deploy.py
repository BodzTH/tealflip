import subprocess
from pathlib import Path

import slots
from config import FIRST_DEPLOY, PROJECT_PATH


def deploy() -> None:
    project_dir = Path(__file__).parent
    if FIRST_DEPLOY:
        print(f"\nFirst Deploy!, Deploying on {slots.active.capitalize()} slot.")

        try:
            subprocess.run(
                [
                    "rsync",
                    "-a",
                    "--delete",
                    f"{PROJECT_PATH}/",
                    f"/var/www/{slots.active}",
                ],
                stdout=subprocess.DEVNULL,
                text=True,
                check=True,
            )
            subprocess.run(
                ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
                input=f"root /var/www/{slots.active};",
                stdout=subprocess.DEVNULL,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            print("\nDeploy Function Failed!")
            return
        except FileNotFoundError:
            print("/etc/nginx/tealflip/ Directory DOES NOT EXIST!")
            return

        with open(f"{project_dir}/config.py", "r") as file:
            lines = file.readlines()

        with open(f"{project_dir}/config.py", "w") as file:
            for line in lines:
                if "FIRST_DEPLOY" in line:
                    file.write("FIRST_DEPLOY: bool = False\n")
                else:
                    file.write(line)
        return

    try:
        active_slot = Path("/etc/nginx/tealflip/active_slot.conf").read_text()
    except FileNotFoundError:
        print("active_slot.conf in /etc/nginx/tealflip/ DOES NOT EXIST!")
        return

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
    else:
        print("active_slot.conf in /etc/nginx/tealflip/ IS EMPTY!, Quiting.")
        return

    subprocess.run(
        ["rsync", "-a", "--delete", f"{PROJECT_PATH}/", f"/var/www/{slots.active}"],
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )

    subprocess.run(
        ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
        input=f"root /var/www/{slots.active};",
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )

    with open(f"{project_dir}/slots.py", "w") as file:
        file.write(f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"')
