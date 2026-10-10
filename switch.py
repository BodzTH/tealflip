import subprocess
from pathlib import Path

import slots
from config import INITIALIZED, PROJECT_PATH
from nginx_reload import nginx_reload


def switch(is_deployment: bool) -> None:

    if not INITIALIZED:
        subprocess.run(
            ["tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{slots.active};",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        return

    project_dir = Path(__file__).parent

    last_good_commit: str = slots.last_good_commit
    last_bad_commit: str = slots.last_bad_commit

    try:
        active_slot = (
            Path("/etc/nginx/tealflip/active_slot.conf")
            .read_text()
            .split("/")[3]
            .strip(";")
        )
    except FileNotFoundError:
        print("active_slot.conf in /etc/nginx/tealflip/ DOES NOT EXIST!")
        return

    if is_deployment:
        active_commit = (
            Path(f"/var/www/{slots.active}/.git/refs/heads/main")
            .read_text()
            .strip("\n")
        )
        project_commit = (
            Path(f"{PROJECT_PATH}/.git/refs/heads/main").read_text().strip("\n")
        )
        if project_commit == active_commit:
            print("Active Deployment already has latest commit!")
            return

        if Path(f"{PROJECT_PATH}/index.html").is_file():
            if "blue" == active_slot:
                slots.idle = "blue"
                slots.active = "green"
            elif "green" == active_slot:
                slots.idle = "green"
                slots.active = "blue"
            else:
                print("active_slot.conf in /etc/nginx/tealflip/ IS EMPTY!, Quiting.")
                return

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
                check=False,
            )

            print(f"\nDeploying on {slots.active.capitalize()} slot.")

            subprocess.run(
                ["tee", "/etc/nginx/tealflip/active_slot.conf"],
                input=f"root /var/www/{slots.active};",
                stdout=subprocess.DEVNULL,
                text=True,
                check=False,
            )

        else:
            print(f"index.html does not exist in {PROJECT_PATH}, switching CANCELD!")
            return
    else:
        print(
            f"\nRolling back from {slots.active.capitalize()} slot to {slots.idle.capitalize()}"
        )

        last_bad_commit = (
            Path(f"/var/www/{slots.active}/.git/refs/heads/main")
            .read_text()
            .strip("\n")
        )

        if "blue" == active_slot:
            slots.idle = "blue"
            slots.active = "green"
        elif "green" == active_slot:
            slots.idle = "green"
            slots.active = "blue"
        else:
            print("active_slot.conf in /etc/nginx/tealflip/ IS EMPTY!, Quiting.")
            return

        subprocess.run(
            ["tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{slots.active};",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )

    if nginx_reload():
        print(f"\nSwitching to {slots.active.capitalize()} Succeeded.")
        print(
            f"\n{slots.active.capitalize()} is Active, {slots.idle.capitalize()} is Idle."
        )

        last_good_commit = (
            Path(f"/var/www/{slots.active}/.git/refs/heads/main")
            .read_text()
            .strip("\n")
        )

        with open(f"{project_dir}/slots.py", "w") as file:
            file.write(
                f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"\nlast_good_commit: str = "{last_good_commit}"\nlast_bad_commit: str = "{last_bad_commit}"'
            )
    else:
        print(f"\nSwitching to {slots.active.capitalize()} Failed!")
        print(f"\nNgnix Failed to Reload!, rolling back to previous {slots.idle} slot.")

        last_bad_commit = (
            Path(f"/var/www/{slots.active}/.git/refs/heads/main")
            .read_text()
            .strip("\n")
        )

        subprocess.run(
            ["tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{slots.idle};",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )

        print(
            f"\n{slots.idle.capitalize()} is Active, {slots.active.capitalize()} is Idle."
        )
        with open(f"{project_dir}/slots.py", "w") as file:
            file.write(
                f'active: str = "{slots.idle}"\nidle: str = "{slots.active}"\nlast_good_commit: str = "{last_good_commit}"\nlast_bad_commit: str = "{last_bad_commit}"'
            )

        return

    return
