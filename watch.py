import subprocess
from pathlib import Path

from config import PROJECT_PATH, REPO_URL
from deploy import deploy


def watch() -> None:
    try:
        remote_status = subprocess.run(
            [
                "git",
                "ls-remote",
                "-h",
                "--refs",
                f"{REPO_URL}",
            ],
            text=True,
            shell=False,
            check=True,
            capture_output=True,
        ).stdout
    except subprocess.CalledProcessError:
        print(f"fatal: '{REPO_URL}' does not appear to be a git repository")
        return

    last_commit = remote_status.split("\t")[0]
    refs_main = Path(f"{PROJECT_PATH}/.git/refs/heads/main").read_text().strip("\n")
    if last_commit != refs_main:
        try:
            print(
                subprocess.run(
                    [
                        "git",
                        "-C",
                        f"{PROJECT_PATH}",
                        "pull",
                        "origin",
                        "main",
                    ],
                    text=True,
                    shell=False,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                ).stdout
            )
            deploy()
        except subprocess.CalledProcessError:
            return
    else:
        print("Last Commit Already Deployed!")


watch()
