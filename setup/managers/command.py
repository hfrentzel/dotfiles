import os
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from logging import Logger
from typing import ClassVar, Optional, Union

from setup.conf import expand
from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import green, print_grid, red
from setup.process import async_proc


@dataclass
class Command(Manager):
    desired: ClassVar[list["Command"]] = []
    name: str
    run_script: Union[str, list[str]]
    state: tuple[bool, str] = (False, "")
    check_script: Optional[str] = None
    depends_on: list[str] = field(default_factory=list)
    cwd: Optional[str] = None

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def _set_status(self) -> None:
        if isinstance(self.cwd, str):
            self.cwd = expand(self.cwd)

        if self.check_script is None:
            self.state = (False, "CANT VERIFY")
            return

        if self.cwd and not os.path.exists(self.cwd):
            self.state = (False, "INCOMPLETE")
            return

        result = await async_proc(self.check_script, cwd=self.cwd)
        if result.returncode == 0:
            self.state = (True, "DONE")
            return

        self.state = (False, "INCOMPLETE")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for command in sorted(cls.desired, key=lambda c: c.name):
            lines.append((command.name,))
        return print_grid(("SCRIPTS",), lines)

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for command in sorted(cls.desired, key=lambda c: c.name):
            if not show_all and command.state[0]:
                continue
            lines.append((command.name, (command.state[1], command.state[0])))
        return print_grid(("SCRIPT", "STATUS"), lines)

    def create_job(self) -> Job:
        return Job(
            name=self.name,
            description=f"Run the {self.name} script",
            depends_on=self.depends_on,
            job=self.perform_script(self.name, self.run_script, self.cwd),
        )

    @staticmethod
    def perform_script(
        name: str, script: Union[str, list[str]], cwd: Optional[str]
    ) -> Callable[[Logger], Coroutine[None, None, bool]]:
        async def inner(logger: Logger) -> bool:
            logger.info(f"Running the {name} script...")

            if cwd and not os.path.exists(cwd):
                logger.error(red(f"{name} script failed"))
                return False

            if isinstance(script, str):
                result = await async_proc(script, cwd=cwd, logger=logger)
                success = not result.returncode
            else:
                for step in script:
                    result = await async_proc(step, cwd=cwd, logger=logger)
                    success = not result.returncode
                    if not success:
                        break
            if success:
                logger.info(green(f"{name} script ran successfully"))
            else:
                logger.error(red(f"{name} script failed"))
            return success

        return inner
