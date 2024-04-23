from dataclasses import dataclass, field
from typing import List, Optional, TypedDict, Union

from setup.managers.manager import mark_resource


@dataclass
class InstallerSpec(TypedDict):
    installer: str
    package_name: Optional[str]
    post_script: Optional[List[str]]


@dataclass
class Exe:
    name: str
    version: str = ""
    installers: List[Union[InstallerSpec, str]] = field(default_factory=list)
    depends_on: Optional[str] = None
    on_demand: bool = False
    command_name: str = ""
    extract_path: Optional[str] = None
    version_cmd: str = ""
    url: str = ""
    repo: str = ""
    steps: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        mark_resource(self.name)
        if not self.command_name:
            self.command_name = self.name
        desired.append(self)


desired: List[Exe] = []
