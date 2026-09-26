import os
import subprocess
from fnmatch import fnmatch
from pathlib import Path


def check_shell() -> str:
    shell = subprocess.getoutput("echo $SHELL").split("/")
    return shell[-1]


def mkdir(path: Path) -> None:

    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def init():
    path = Path.home() / ".local" / "bin"
    mkdir(path)
    shell_conf = Path.home() / ".bashrc"
    if fnmatch(check_shell(), "fish"):
        shell_conf = Path.home() / ".conf/fish/config.fish"
        print(".conf/fish")
    if fnmatch(check_shell(), "zsh"):
        shell_conf = Path.home() / ".bashrc"
        print(".zshrc")
    if fnmatch(check_shell(), "bash"):
        shell_conf = Path.home() / ".bashrc"
        print(".bashrc")

    print(shell_conf)
    env = "PATH"
    export_line = f"export {env}"

    path_env = ""
    try:
        os.environ[env]
    except KeyError:
        if export_line in shell_conf.read_text():
            for text in shell_conf.read_text().split("\n"):
                if "PATH" in text:
                    path_env = "\n" + text + "\n"
        if export_line not in shell_conf.read_text():
            with shell_conf.open("a") as file:
                file.write(path_env)
        with shell_conf.open("a") as file:
            file.write(path_env)


init()
