import os
import subprocess
from pathlib import Path

import slots
from config import INITIALIZED, PROJECT_PATH
from switch import switch


def deploy() -> None:
    project_dir = Path(__file__).parent
    if not INITIALIZED:
        print(f"\nInitializing!, Deploying on {slots.active.capitalize()} slot.")

        try:
            subprocess.run(
                [
                    "rsync",
                    "-a",
                    "--delete",
                    f"{PROJECT_PATH}/",
                    f"/var/www/{slots.active}",
                ],
                stdout=subprocess.DEVNULL,
                text=True,
                check=True,
            )
            if switch(slots.active):
                print(f"\nSwitching to {slots.active} Succeeded.")
            else:
                print(f"\nSwitching to {slots.active} Failed!")
                return
        except subprocess.CalledProcessError as e:
            print("\nDeploy Failed!\n", e.stderr)
            return
        except FileNotFoundError:
            print("\n/etc/nginx/tealflip/ Directory DOES NOT EXIST!")
            return

        service_file = (
            Path(f"{project_dir}/tealflip-git-watcher.service")
            .read_text()
            .replace("{USER}", os.getlogin())
        )

        subprocess.run(
            ["tee", f"{project_dir}/tealflip-git-watcher.service"],
            input=service_file,
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        subprocess.run(
            [
                "sudo",
                "cp",
                f"{project_dir}/tealflip-git-watcher.service",
                f"{project_dir}/tealflip-git-watcher.timer",
                "/etc/systemd/system/",
            ],
            check=False,
            text=True,
            shell=False,
        )

        tealflip_sudoer = f"{os.getlogin()} ALL=(root) NOPASSWD: /usr/bin/nginx -t, /usr/bin/nginx -s reload"

        subprocess.run(
            ["tee", f"{project_dir}/tealflip_sudoer"],
            input=tealflip_sudoer,
            stdout=subprocess.DEVNULL,
            text=True,
            check=False,
        )

        try:
            Path(f"{project_dir}/tealflip_sudoer").is_file()
            subprocess.run(
                ["sudo", "visudo", "-c", f"{project_dir}/tealflip_sudoer"],
                input=tealflip_sudoer,
                stdout=subprocess.DEVNULL,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            print(f"tealflip_sudoer in {project_dir} DOES NOT EXIST!, Quiting.")
            return
        except subprocess.CalledProcessError:
            print("tealflip_sudoer Parsing Failed!, Quiting.")
            return

        try:
            subprocess.run(
                [
                    "sudo",
                    "cp",
                    f"{project_dir}/tealflip_sudoer",
                    "/etc/sudoers.d/",
                ],
                check=True,
                text=True,
                shell=False,
            )

        except subprocess.CalledProcessError:
            print("copying tealflip_sudoer to /etc/sudoers.d/, Quiting.")
            return

        try:
            subprocess.run(
                [
                    "sudo",
                    "systemctl",
                    "enable",
                    "--now",
                    "/etc/systemd/system/tealflip-git-watcher.timer",
                ],
                check=True,
                text=True,
                shell=False,
            )
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            return

        with open(f"{project_dir}/config.py", "r") as file:
            lines = file.readlines()

        with open(f"{project_dir}/config.py", "w") as file:
            for line in lines:
                if "INITIALIZED" in line:
                    file.write("INITIALIZED: bool = True\n")
                else:
                    file.write(line)
        return

    if switch(slots.active):
        print(f"\nSwitching to {slots.active} Succeeded.")
    else:
        print(f"\nSwitching to {slots.active} Failed!")
        return

    subprocess.run(
        ["rsync", "-a", "--delete", f"{PROJECT_PATH}/", f"/var/www/{slots.active}"],
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )
