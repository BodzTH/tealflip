from pathlib import Path


def status() -> None:
    try:
        active_slot = Path("/etc/nginx/tealflip/active_slot.conf").read_text()
    except FileNotFoundError:
        print("active_slot.conf in /etc/nginx/tealflip/ DOES NOT EXIST!")
        return

    if "blue" in active_slot:
        print("Blue Deployment Active!")
    elif "green" in active_slot:
        print("Green Deployment Active!")
    else:
        print("Nothing Deployed!")
