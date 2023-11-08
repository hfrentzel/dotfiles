from dataclasses import dataclass

@dataclass
class Conf:
    args: str=None
    dotfiles_home: str=None
    types: list=None
    sources_dir: str=None

conf = Conf()

