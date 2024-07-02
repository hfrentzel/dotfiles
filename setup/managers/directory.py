import os
from dataclasses import dataclass
from typing import Callable, ClassVar, Coroutine, List, Tuple

from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import print_grid


@dataclass
class Directory(Manager):
    desired: ClassVar[List["Directory"]] = []
    name: str
    path: str
    state: Tuple[bool, str] = (False, "")

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def set_status(self) -> None:
        self._set_status()

    def _set_status(self) -> None:
        path = os.path.expanduser(self.path)
        if os.path.isdir(path):
            self.state = (True, "Exists")
            return
        if os.path.exists(path):
            self.state = (False, "BLOCKED")
            return
        self.state = (False, "MISSING")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for directory in sorted(cls.desired, key=(lambda d: d.path)):
            lines.append((directory.path,))
        return print_grid(("SUB-DIRECTORIES",), lines)

    @classmethod
    async def get_statuses(cls) -> List[str]:
        complete = []
        for directory in cls.desired:
            directory._set_status()
            if directory.state[0]:
                complete.append(directory.name)
        return complete

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for directory in sorted(cls.desired, key=(lambda d: d.path)):
            if not show_all and directory.state[0]:
                continue
            lines.append((directory.path, (directory.state[1], directory.state[0])))
        return print_grid(("SUB-DIRECTORIES", "STATUS"), lines)

    def create_job(self) -> Job:
        return Job(
            names=[self.name],
            description=f"Create self at {self.path}",
            job=self.create_directory(self.path),
        )

    @staticmethod
    def create_directory(path: str) -> Callable[[], Coroutine[None, None, bool]]:
        async def inner() -> bool:
            full_path = os.path.expanduser(path)
            print(f"Creating directory at {full_path}...")
            os.makedirs(full_path)

            return True

        return inner
