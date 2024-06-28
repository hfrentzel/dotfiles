import os
from dataclasses import dataclass
from typing import Callable, ClassVar, Coroutine, List, Tuple

from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import print_grid


@dataclass
class Directory(Manager):
    desired: ClassVar[List["Directory"]] = []
    check_results: ClassVar[List[Tuple["Directory", bool, str]]] = []
    name: str
    path: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    def current_status(self) -> Tuple[bool, str]:
        path = os.path.expanduser(self.path)
        if os.path.isdir(path):
            return (True, "Exists")
        if os.path.exists(path):
            return (False, "BLOCKED")
        return (False, "MISSING")

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
            result = directory.current_status()
            if result[0]:
                complete.append(directory.name)
            cls.check_results.append((directory, *result))
        return complete

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for directory, complete, status in sorted(cls.check_results, key=(lambda d: d[0].path)):
            if not show_all and complete:
                continue
            lines.append((directory.path, (status, complete)))
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
