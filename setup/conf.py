import os
from argparse import Namespace
from dataclasses import dataclass


@dataclass
class Conf:
    args: Namespace = Namespace()
    dotfiles_home: str = ""
    sources_dir: str = os.path.expanduser("~/.cache/env_setup")
    parser_dir: str = os.path.expanduser("~/.local/share/nvim/site/parser")
    root_access: bool = False

    def __post_init__(self) -> None:
        os.makedirs(self.sources_dir, exist_ok=True)


conf = Conf()
