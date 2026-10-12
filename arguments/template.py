import subprocess
from pathlib import Path


def template() -> None:
    project_dir = Path(__file__).resolve().parents[1]

    config_template = Path(f"{project_dir}/templates/config_template.py").read_text()

    subprocess.run(
        ["tee", f"{project_dir}/variables/config.py"],
        input=config_template,
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )

    slots_file = Path(f"{project_dir}/templates/slots_template.py").read_text()

    subprocess.run(
        ["tee", f"{project_dir}/variables/slots.py"],
        input=slots_file,
        stdout=subprocess.DEVNULL,
        text=True,
        check=False,
    )

    print("Configuration variables needs to be set!")
    print("Please set all configuration variables in variables/config.py")
