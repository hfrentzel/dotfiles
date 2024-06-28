import asyncio
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
    check_results: ClassVar[List[Tuple["Library", bool, str]]] = []
    name: str
    version: str
    manager: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def current_status(self) -> Tuple["Library", bool, str]:
        if self.manager == "pip":
            return (self, *Pip.check_install(self))
        if self.manager == "npm":
            return (self, *Npm.check_install(self))

        return (self, False, "UNKNOWN")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for lib in sorted(cls.desired, key=(lambda b: b.name)):
            lines.append((lib.name, lib.version))
        return print_grid(("LIBRARY", "VERSION"), lines)

    @classmethod
    async def get_statuses(cls) -> List[str]:
        complete = []
        tasks = []
        for lib in cls.desired:
            tasks.append(lib.current_status())
        results = await asyncio.gather(*tasks)
        cls.check_results.extend(results)
        for result in results:
            if result[1]:
                complete.append(result[0].name)
        return complete

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for lib, complete, curr_ver in sorted(cls.check_results, key=(lambda b: b[0].name)):
            if not show_all and complete:
                continue
            lines.append((lib.name, lib.version, (curr_ver, complete)))
        return print_grid(("LIBRARY", "DESIRED", "CURRENT"), lines)

    def create_job(self) -> None:
        JOB_BUILDERS[self.manager](self, self.name)
