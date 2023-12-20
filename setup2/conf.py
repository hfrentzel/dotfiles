from argparse import Namespace
from dataclasses import dataclass
import os


@dataclass
class Conf:
    args: Namespace = Namespace()
    dotfiles_home: str = ''
    sources_dir: str = os.path.expanduser('~/.cache/env_setup')
    root_access: bool = False

    def __post_init__(self) -> None:
        os.makedirs(self.sources_dir, exist_ok=True)


conf = Conf()
