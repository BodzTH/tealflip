import subprocess
from pathlib import Path


def deploy() -> None:
    if "blue" not in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
        active_slot = "blue"
    elif "green" not in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
        active_slot = "green"
    else:
        print("Deploying!")
    subprocess.run(
        ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
        input=f"root /var/www/{active_slot}",
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )
