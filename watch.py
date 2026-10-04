import subprocess

from config import REPO_URL


def watch() -> None:
    remote_status = subprocess.run(
        [
            "git",
            "ls-remote",
            REPO_URL,
        ],
        text=True,
        shell=False,
        check=False,
        capture_output=True,
    ).stdout
    print(remote_status)
