import subprocess
from pathlib import Path


def rollback() -> None:
    try:
        if "green" in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
            idle_slot = "blue"
        elif "blue" in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
            idle_slot = "green"
    except FileNotFoundError:
        print("Nothing Deployed!, Exiting rollback.")
        return
    subprocess.run(
        ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
        input=f"root /var/www/{idle_slot}",
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )
