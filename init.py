import os
import subprocess
from pathlib import Path

from config import INITIALIZED
from nginx_init import nginx_init
from status import status


def shell_name() -> str:
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


def replace_export_line(path: Path, config_file: Path):
    for text in config_file.read_text().split("\n"):
        if "PATH=" in text:
            splitted_path = text.split()[1]
            add_path = (
                "\n" + splitted_path[:-1] + f':{path}"' + " # added by tealflip" + "\n"
            )

    lines: list[str] = []

    with config_file.open("r") as file:
        lines = file.readlines()

    with config_file.open("w") as file:
        for line in lines:
            if "PATH=" in line:
                file.write(add_path)
            else:
                file.write(line)


def add_path_env(bin_path: Path, shell_config_file: Path) -> None:
    path_value = os.getenv("PATH")

    if (path_value == None) or (
        (str(bin_path) not in path_value)
        and (str(bin_path) not in shell_config_file.read_text())
    ):
        with shell_config_file.open("a") as file:
            file.write(f'\nexport PATH="$PATH:{bin_path}"\n')
            print(f"Run: source {shell_config_file}\n")
            return

    elif str(bin_path) in path_value:
        return

    else:
        replace_export_line(bin_path, shell_config_file)


def init():
    if INITIALIZED:
        print("Already Initialized!")
        return
    # Initializing Variables
    bin_path = Path.home() / ".local" / "bin"  # Absolute path to .local/bin directory
    shell_config_file = Path.home() / ".bashrc"  # Shell Configuration File
    shell = shell_name()  # shell name

    # making a bin directory if does not exist
    try:
        bin_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        subprocess.run(
            ["sudo", "mkdir", "-p", f"{bin_path}"],
            check=False,
            text=True,
            shell=False,
        )

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
    add_path_env(bin_path, shell_config_file)

    """
    ln: link a second file to first file 
    -s: to make symlink instead of hard link
    f"{os.getcwd()}/tealflip": (first file) tealflip absolute path 
    f"{local_bin_path}/tealflip": (second file) the directory path to put the symlink file which is .local/bin
    text=True: Decodes/Encodes Input/Output as str instead of bytes
    check=False: so if a command fails with a non-zero exit code it does not raise CalledProcessError exception
    shell=False: so python does not treat onlythe first item as command and rest as arguments
    """
    if os.path.isfile(
        f"{bin_path}/tealflip"
    ):  # if tealflip symlink exist in bin directory
        print(f"{bin_path}/tealflip Symlink Already Exist.")
    else:
        project_dir = Path(__file__).parent
        subprocess.run(
            ["ln", "-s", f"{project_dir}/tealflip", f"{bin_path}/tealflip"],
            text=True,
            check=False,
            shell=False,
        )

    config_template = Path(f"{project_dir}/config_template.py").read_text()

    subprocess.run(
        ["tee", f"{project_dir}/config.py"],
        input=config_template,
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )

    nginx_init()

    status()
