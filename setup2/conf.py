from dataclasses import dataclass
from typing import Optional
from argparse import Namespace


@dataclass
class Conf:
    args: Optional[Namespace] = None
    dotfiles_home: Optional[str] = None
    types: Optional[list] = None
    sources_dir: Optional[str] = None
    root_access: bool = False


conf = Conf()
