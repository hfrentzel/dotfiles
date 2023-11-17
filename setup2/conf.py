from dataclasses import dataclass
from typing import Optional, List
from argparse import Namespace


@dataclass
class Conf:
    args: Optional[Namespace] = None
    dotfiles_home: str = ''
    types: Optional[List[str]] = None
    sources_dir: Optional[str] = None
    root_access: bool = False


conf = Conf()
