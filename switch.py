import subprocess
from pathlib import Path

import slots
from nginx_reload import nginx_reload


def switch(input_slot: str) -> bool:

    project_dir = Path(__file__).parent

    last_good_commit: str = slots.last_good_commit
    last_bad_commit: str = slots.last_bad_commit

    try:
        current_slot = (
            Path("/etc/nginx/tealflip/active_slot.conf")
            .read_text()
            .split("/")[3]
            .strip(";")
        )
    except FileNotFoundError:
        print("active_slot.conf in /etc/nginx/tealflip/ DOES NOT EXIST!")
        return False

    if Path(f"/var/www/{input_slot}/index.html").is_file():
        subprocess.run(
            ["tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{input_slot};",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        slots.active = input_slot
        slots.idle = current_slot
    else:
        print(f"index.html does not exist in {input_slot} slot, switching CANCELD!")
        return False

    if nginx_reload():
        print("\nNgnix Reloaded Successfully.")
        last_good_commit = (
            Path(f"/var/www/{input_slot}/.git/refs/heads/main").read_text().strip("\n")
        )
        with open(f"{project_dir}/slots.py", "w") as file:
            file.write(
                f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"\nlast_good_commit: str = "{last_good_commit}"\nlast_bad_commit: str = "{last_bad_commit}"'
            )
    else:
        print(
            f"\nNgnix Failed to Reload!, rolling back to previous {current_slot} slot."
        )
        last_bad_commit = (
            Path(f"/var/www/{input_slot}/.git/refs/heads/main").read_text().strip("\n")
        )

        slots.active = current_slot
        slots.idle = input_slot

        subprocess.run(
            ["tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{current_slot};",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        with open(f"{project_dir}/slots.py", "w") as file:
            file.write(
                f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"\nlast_good_commit: str = "{last_good_commit}"\nlast_bad_commit: str = "{last_bad_commit}"'
            )

        return False

    print(f"\nDeploying on {slots.active.capitalize()} slot.")
    print(
        f"\n{slots.active.capitalize()} is Active, {slots.idle.capitalize()} is Idle."
    )
    return True
