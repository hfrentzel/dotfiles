from argparse import Namespace
from dataclasses import dataclass, field
from typing import List

from .managers.manager import Manager


@dataclass
class Conf:
    args: Namespace = Namespace()
    dotfiles_home: str = ''
    types: List[Manager] = field(default_factory=list)
    sources_dir: str = ''
    root_access: bool = False


conf = Conf()
