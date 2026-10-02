import subprocess


def watch() -> None:
    remote_status = subprocess.run(
        ["git", "ls-remote"], text=True, shell=False, check=False, capture_output=True
    ).stdout
    print(remote_status)
