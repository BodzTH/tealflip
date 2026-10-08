import subprocess
from pathlib import Path

from nginx_reload import nginx_reload
from rollback import rollback

# import slots


def switch(slot) -> None:
    # project_dir = Path(__file__).parent
    if Path(f"/var/www/{slot}/index.html").is_file():
        subprocess.run(
            ["tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{slot};",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )
    else:
        print(f"index.html does not exist in {slot} slot, switching CANCELD!")
        return

    if nginx_reload():
        print("\nNgnix Reloaded Successfully.")
    else:
        print("\nNgnix Failed to Reload!, rolling back to previous slot.")
        rollback()
        return

    # with open(f"{project_dir}/slots.py", "w") as file:
    #     file.write(f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"')
