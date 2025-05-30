import os
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from logging import Logger
from typing import ClassVar

from setup.conf import expand
from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import print_grid


@dataclass
class Directory(Manager):
    desired: ClassVar[list["Directory"]] = []
    name: str
    path: str
    state: tuple[bool, str] = (False, "")

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def _set_status(self) -> None:
        path = expand(self.path)
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
        for directory in sorted(cls.desired, key=lambda d: d.path):
            lines.append((directory.path,))
        return print_grid(("SUB-DIRECTORIES",), lines)

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for directory in sorted(cls.desired, key=lambda d: d.path):
            if not show_all and directory.state[0]:
                continue
            lines.append((
                directory.path,
                (directory.state[1], directory.state[0]),
            ))
        return print_grid(("SUB-DIRECTORIES", "STATUS"), lines)

    def create_job(self) -> Job:
        return Job(
            name=self.name,
            description=f"Create directory at {self.path}",
            job=self.create_directory(self.path),
        )

    @staticmethod
    def create_directory(
        path: str,
    ) -> Callable[[Logger], Coroutine[None, None, bool]]:
        async def inner(logger: Logger) -> bool:
            full_path = expand(path)
            logger.info(f"Creating directory at {full_path}...")
            os.makedirs(full_path)

            return True

        return inner
