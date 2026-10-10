import subprocess


def nginx_reload() -> bool:
    try:
        subprocess.run(
            [
                "sudo",
                "nginx",
                "-t",
            ],
            check=True,
            text=True,
            shell=False,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return False
    try:
        subprocess.run(
            [
                "sudo",
                "nginx",
                "-s",
                "reload",
            ],
            check=True,
            text=True,
            shell=False,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return False

    return True
