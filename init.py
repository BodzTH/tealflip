import os
import subprocess
from fnmatch import fnmatch
from pathlib import Path


def check_shell() -> str:
    shell = subprocess.run(
        ["ps", "-p", str(os.getppid()), "-o", "comm="],
        capture_output=True,
        shell=False,
        text=True,
        check=False,
    ).stdout
    return shell.strip("\n")


def mkdir(path: Path) -> None:

    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def replace_export_line(path: Path, shell_conf: Path, env: str, env_line: str):
    for text in shell_conf.read_text().split("\n"):
        if env in text:
            splitted_path = text.split()[1]
            add_path = "\n" + splitted_path[:-1] + f':{path}"' + "\n"

    lines: list[str] = []
    with shell_conf.open("r") as file:
        lines = file.readlines()
    with shell_conf.open("w") as file:
        for line in lines:
            if env_line in line:
                file.write(add_path)
            else:
                file.write(line)


def add_path_env(path: Path, shell_conf: Path, env: str, env_line: str) -> None:
    env_value = os.getenv(env)
    shell_conf_file = shell_conf.read_text()

    if env_value == None:
        if env_line in shell_conf_file and (str(path) not in shell_conf_file):
            with shell_conf.open("a") as file:
                file.write(f'\nexport {env_line}"${env}:{path}"\n')
                print("Restart Shell!")
                return
    elif str(path) in env_value:
        return
    else:
        if env_line in shell_conf_file and (str(path) not in shell_conf_file):
            replace_export_line(path, shell_conf, env, env_line)
        else:
            pass


def init():
    path = Path.home() / ".local" / "bin"
    mkdir(path)

    shell_conf = Path.home() / ".bashrc"
    shell = check_shell()
    if fnmatch(shell, "fish"):
        shell_conf = Path.home() / ".config/fish/config.fish"
    if fnmatch(shell, "zsh"):
        shell_conf = Path.home() / ".zshrc"
    if fnmatch(shell, "bash"):
        shell_conf = Path.home() / ".bashrc"

    add_path_env(path, shell_conf, "PATH", "PATH=")
