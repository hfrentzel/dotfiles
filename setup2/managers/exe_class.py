from dataclasses import dataclass, field
from typing import List, Optional
from setup2.managers.manager import mark_resource


@dataclass
class Exe():
    name: str
    version: str = ''
    installers: List[str] = field(default_factory=list)
    depends_on: Optional[str] = None
    on_demand: bool = False
    override: bool = False
    command_name: str = ''
    extract_path: Optional[str] = None
    url: str = ''
    repo: str = ''
    steps: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        mark_resource(self.name, self.override)
        if self.command_name == '':
            self.command_name = self.name
        desired.append(self)


desired: List[Exe] = []
