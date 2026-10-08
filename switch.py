import subprocess
from pathlib import Path

from nginx_reload import nginx_reload


def switch(slot) -> bool:
    current_slot = (
        Path("/etc/nginx/tealflip/active_slot.conf")
        .read_text()
        .split("/")[3]
        .strip(";")
    )
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
        return False

    if nginx_reload():
        print("\nNgnix Reloaded Successfully.")
    else:
        print(
            f"\nNgnix Failed to Reload!, rolling back to previous {current_slot} slot."
        )
        subprocess.run(
            ["tee", "/etc/nginx/tealflip/active_slot.conf"],
            input=f"root /var/www/{current_slot};",
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        return False

    return True
