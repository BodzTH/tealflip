import subprocess
from pathlib import Path

from config import PROJECT_PATH, REPO_URL


def watch() -> None:
    remote_status = subprocess.run(
        [
            "git",
            "ls-remote",
            "-h",
            "--refs",
            REPO_URL,
        ],
        text=True,
        shell=False,
        check=False,
        capture_output=True,
    ).stdout
    last_commit = remote_status.split("\t")[0]
    refs_main = Path(f"{PROJECT_PATH}/.git/refs/heads/main").read_text().strip("\n")
    if last_commit != refs_main:
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
                capture_output=True,
            ).stdout
        )
    else:
        pass


watch()
