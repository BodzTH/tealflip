import subprocess
from pathlib import Path


def deploy() -> None:
    try:
        if "blue" in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
            active_slot = "green"
            print("\nDeploying on green slot.")
        elif "green" in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
            active_slot = "blue"
            print("\nDeploying on blue slot.")
    except FileNotFoundError:
        print("\nFirst Deploy!, Deploying on blue slot.")
        active_slot = "blue"
    subprocess.run(
        ["sudo", "tee", "/etc/nginx/tealflip/active_slot.conf"],
        input=f"root /var/www/{active_slot}",
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )
