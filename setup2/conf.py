from argparse import Namespace
from dataclasses import dataclass, field
from typing import List
import os

from .managers.manager import Manager


@dataclass
class Conf:
    args: Namespace = Namespace()
    dotfiles_home: str = ''
    types: List[Manager] = field(default_factory=list)
    sources_dir: str = os.path.expanduser('~/.cache/env_setup')
    root_access: bool = False

    def __post_init__(self):
        os.makedirs(self.sources_dir, exist_ok=True)


conf = Conf()
