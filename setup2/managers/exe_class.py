from dataclasses import dataclass, field
from typing import ClassVar, List, Optional
from setup2.managers.manager import mark_resource


@dataclass
class Exe():
    desired: ClassVar[List['Exe']] = []
    name: str
    version: str = ''
    installers: Optional[List[str]] = None
    on_demand: bool = False
    override: bool = False
    command_name: str = ''
    extract_all: bool = False
    url: str = ''
    repo: str = ''
    steps: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        mark_resource(self.name, self.override)
        if self.command_name == '':
            self.command_name = self.name
        self.desired.append(self)
