from pathlib import Path

import slots


def status() -> None:
    try:
        Path("/etc/nginx/tealflip/active_slot.conf").exists()
    except FileNotFoundError:
        print("active_slot.conf in /etc/nginx/tealflip/ DOES NOT EXIST!")
        return

    active_ref = (
        Path(f"/var/www/{slots.active}/.git/refs/heads/main").read_text().strip("\n")
    )
    idle_ref = (
        Path(f"/var/www/{slots.idle}/.git/refs/heads/main").read_text().strip("\n")
    )

    print(f"\n{slots.active.capitalize()} Deployment Active!")
    print(f"\nActive Slot Commit Hash: {active_ref}")
    print(f"\nIdle Slot Commit Hash: {idle_ref}")
