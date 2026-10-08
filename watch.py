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
                f"{REPO_URL}",
                "main",
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
    project_commit = (
        Path(f"{PROJECT_PATH}/.git/refs/heads/main").read_text().strip("\n")
    )
    if last_commit != project_commit:
        try:
            git_pull = subprocess.run(
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
                check=True,
                capture_output=True,
            )

            print(git_pull.stdout)

            deploy()

        except subprocess.CalledProcessError as e:
            print(e.stderr)
            return
    else:
        print("Last Commit Already Deployed!")
