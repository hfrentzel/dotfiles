from dataclasses import dataclass
from typing import ClassVar, List, Optional


@dataclass
class Exe():
    desired: ClassVar[List['Exe']] = []
    name: str
    version: str = ''
    installers: Optional[List[str]] = None
    command_name: str = ''
    url: str = ''
    repo: str = ''

    def __post_init__(self) -> None:
        if self.command_name == '':
            self.command_name = self.name
        self.desired.append(self)
