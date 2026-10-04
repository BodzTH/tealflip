from pathlib import Path


def status() -> None:
    if "blue" in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
        print("Blue Deployment Active!")

    elif "green" in Path("/etc/nginx/tealflip/active_slot.conf").read_text():
        print("Green Deployment Active!")
    else:
        print("Nothing Deployed!")
