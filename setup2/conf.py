from dataclasses import dataclass

@dataclass
class Conf:
    args: str=None
    dotfiles_home: str=None
    types: list=None

conf = Conf()

