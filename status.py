from pathlib import Path

import slots


def status() -> None:
    try:
        Path("/etc/nginx/tealflip/active_slot.conf").exists()
    except FileNotFoundError:
        print("active_slot.conf in /etc/nginx/tealflip/ DOES NOT EXIST!")
        return

    if Path(f"/var/www/{slots.active}/index.html").is_file():
        active_ref = (
            Path(f"/var/www/{slots.active}/.git/refs/heads/main")
            .read_text()
            .strip("\n")
        )
    else:
        print(f"index.html does not exist in {slots.active} slot!")
        return

    print(f"\n{slots.active.capitalize()} Deployment Active!")
    print(f"\nActive Slot Commit Hash: {active_ref}")

    if Path(f"/var/www/{slots.idle}/index.html").is_file():
        idle_ref = (
            Path(f"/var/www/{slots.idle}/.git/refs/heads/main").read_text().strip("\n")
        )
    else:
        print(f"{slots.idle} slot is empty")
        return

    print(f"\nIdle Slot Commit Hash: {idle_ref}")
