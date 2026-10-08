import os
import subprocess
from pathlib import Path

from config import DNS, IP
from nginx_init import nginx_init
from status import status


def check_shell() -> str:
    """
    ps: to check for running process
    -p: to select PID
    os.getppid: to get the parent process id which will be the shell called the script
    -o: to specify the output format
    comm=: sets the header of COMMAND column to nothing so we get the shell name only
    capture_output=True: so we can capture stdout and stderr
    shell=False: so python does not treat onlythe first item as command and rest as arguments
    text=True: Decodes/Encodes Input/Output as str instead of bytes
    check=False: so if a command fails with a non-zero exit code it does not raise CalledProcessError exception
    """

    shell = subprocess.run(
        ["ps", "-p", str(os.getppid()), "-o", "comm="],
        capture_output=True,
        shell=False,
        text=True,
        check=False,
    ).stdout

    return shell.strip("\n")  # remove trailing end line from shell name


def replace_export_line(path: Path, config_file: Path, env_line: str):
    for text in config_file.read_text().split("\n"):
        if env_line in text:
            splitted_path = text.split()[1]
            add_path = (
                "\n" + splitted_path[:-1] + f':{path}"' + " # added by tealflip" + "\n"
            )

    lines: list[str] = []

    with config_file.open("r") as file:
        lines = file.readlines()

    with config_file.open("w") as file:
        for line in lines:
            if env_line in line:
                file.write(add_path)
            else:
                file.write(line)


def add_path_env(path: Path, config_file: Path, env: str, env_line: str) -> None:
    env_value = os.getenv(env)

    if (env_value == None) or (
        (str(path) not in env_value) and (str(path) not in config_file.read_text())
    ):
        with config_file.open("a") as file:
            file.write(f'\nexport {env_line}"${env}:{path}"\n')
            print(f"Run: source {config_file}\n")
            return

    elif str(path) in env_value:
        return

    else:
        replace_export_line(path, config_file, env_line)


def init():
    if Path("/etc/nginx/tealflip/active_slot.conf").exists():
        print("Already Initialized!")
        return
    # Initializing Variables
    local_bin_path = (
        Path.home() / ".local" / "bin"
    )  # Absolute path to .local/bin directory
    shell_config_file = Path.home() / ".bashrc"  # Shell Configuration File
    shell = check_shell()  # shell name

    # making .local/bin directory if does not exist
    local_bin_path.mkdir(parents=True, exist_ok=True)

    # Assiging the shell configuration path for working shell
    if shell == "bash":
        shell_config_file = Path.home() / ".bashrc"
    elif shell == "zsh":
        shell_config_file = Path.home() / ".zshrc"
    elif shell == "fish":
        shell_config_file = Path.home() / ".config/fish/config.fish"
    else:
        print("Unknown Shell, try:\n", "Bash", "Zshell", "Fish")

    # Adding .local/bin directory to PATH if not set
    add_path_env(local_bin_path, shell_config_file, "PATH", "PATH=")

    """
    ln: link a second file to first file 
    -s: to make symlink instead of hard link
    f"{os.getcwd()}/tealflip": (first file) tealflip absolute path 
    f"{local_bin_path}/tealflip": (second file) the directory path to put the symlink file which is .local/bin
    text=True: Decodes/Encodes Input/Output as str instead of bytes
    check=False: so if a command fails with a non-zero exit code it does not raise CalledProcessError exception
    shell=False: so python does not treat onlythe first item as command and rest as arguments
    """
    if not os.path.isfile(
        f"{local_bin_path}/tealflip"
    ):  # if tealflip symlink does not exist in .local/bin
        subprocess.run(
            ["ln", "-s", f"{os.getcwd()}/tealflip", f"{local_bin_path}/tealflip"],
            text=True,
            check=False,
            shell=False,
        )

    nginx_init(IP, DNS)

    status()
