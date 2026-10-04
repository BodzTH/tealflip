import subprocess
from pathlib import Path


def rollback() -> None:
    if "blue" not in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
        idle_slot = "blue"
    elif "green" not in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
        idle_slot = "green"
    else:
        print("Nothing Deployed!")
        return
    subprocess.run(
        ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
        input=f"root /var/www/{idle_slot}",
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )
