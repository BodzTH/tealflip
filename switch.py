import subprocess
from pathlib import Path

# import slots


def switch(slot) -> None:
    # project_dir = Path(__file__).parent
    if Path(f"/var/www/{slot}/index.html").is_file():
        subprocess.run(
            ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{slot};",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )
    else:
        print(f"index.html does not exist in {slot} slot, switching CANCELD!")
        return

    # with open(f"{project_dir}/slots.py", "w") as file:
    #     file.write(f'active: str = "{slots.active}"\nidle: str = "{slots.idle}"')
