import os
from pathlib import Path


def mkdir(path: Path) -> None:
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
