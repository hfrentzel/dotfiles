import os
import platform
from argparse import Namespace
from dataclasses import dataclass, field

if platform.system() == "Linux":
    parser_dir = os.path.expanduser("~/.local/share/nvim/site/parser")
else:
    parser_dir = os.path.expanduser("~/Appdata/Local/nvim-data/site/parser")


@dataclass
class Conf:
    args: Namespace = field(default_factory=Namespace)
    dotfiles_home: str = ""
    sources_dir: str = os.path.expanduser("~/.cache/env_setup")
    parser_dir: str = parser_dir
    root_access: bool = False

    def __post_init__(self) -> None:
        os.makedirs(self.sources_dir, exist_ok=True)


def expand(path: str) -> str:
    if path.startswith("DOT"):
        path = path.replace("DOT", conf.dotfiles_home)
    elif path.startswith("CONFL"):
        if platform.system() == "Linux":
            path = path.replace("CONFL", "~/.config")
        else:
            path = path.replace("CONFL", "~/AppData/Local")
    elif path.startswith("CONFR"):
        if platform.system() == "Linux":
            path = path.replace("CONFR", "~/.config")
        else:
            path = path.replace("CONFR", "~/AppData/Roaming")

    path = os.path.expanduser(path)
    return path


conf = Conf()
