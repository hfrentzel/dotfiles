from dataclasses import dataclass
from typing import ClassVar, List, Tuple

from setup.managers.manager import Manager, Package, mark_resource
from setup.managers.package_types.npm import Npm
from setup.managers.package_types.pip import Pip
from setup.output import print_grid

JOB_BUILDERS = {"pip": Pip.pip_builder, "npm": Npm.npm_builder}


@dataclass
class Library(Manager, Package):
    desired: ClassVar[List["Library"]] = []
    name: str
    version: str
    manager: str
    state: Tuple[bool, str] = (False, "")

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def _set_status(self) -> None:
        if self.manager == "pip":
            self.state = Pip.check_install(self)
            return
        if self.manager == "npm":
            self.state = Npm.check_install(self)
            return

        self.state = (False, "UNKNOWN")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for lib in sorted(cls.desired, key=lambda b: b.name):
            lines.append((lib.name, lib.version))
        return print_grid(("LIBRARY", "VERSION"), lines)

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for lib in sorted(cls.desired, key=lambda b: b.name):
            if not show_all and lib.state[0]:
                continue
            lines.append((lib.name, lib.version, (lib.state[1], lib.state[0])))
        return print_grid(("LIBRARY", "DESIRED", "CURRENT"), lines)

    def create_job(self) -> None:
        JOB_BUILDERS[self.manager](self)
