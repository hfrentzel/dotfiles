import asyncio
import os
from dataclasses import dataclass
from typing import Callable, ClassVar, Coroutine, List, Optional, Tuple

from setup.conf import conf
from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import green, print_grid, red
from setup.process import async_proc


@dataclass
class Command(Manager):
    desired: ClassVar[List["Command"]] = []
    check_results: ClassVar[List[Tuple["Command", bool, str]]] = []
    name: str
    run_script: str
    check_script: Optional[str] = None
    depends_on: Optional[str] = None
    cwd: Optional[str] = None

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def current_status(self) -> Tuple["Command", bool, str]:
        if isinstance(self.cwd, str):
            self.cwd = os.path.expanduser(self.cwd.replace("DOT", conf.dotfiles_home))

        if self.check_script is None:
            return (self, False, "CANT VERIFY")
        result = await async_proc(self.check_script, cwd=self.cwd)
        if result.returncode == 0:
            return (self, True, "DONE")

        return (self, False, "INCOMPLETE")

    @classmethod
    async def get_statuses(cls) -> List[str]:
        complete = []
        tasks = []
        for command in cls.desired:
            tasks.append(command.current_status())
        results = await asyncio.gather(*tasks)
        cls.check_results.extend(results)
        for result in results:
            if result[1]:
                complete.append(result[0].name)
        return complete

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for command in sorted(cls.desired, key=(lambda c: c.name)):
            lines.append((command.name,))
        return print_grid(("SCRIPTS",), lines)

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for command, complete, status in sorted(cls.check_results, key=(lambda c: c[0].name)):
            if not show_all and complete:
                continue
            lines.append((command.name, (status, complete)))
        return print_grid(("SCRIPT", "STATUS"), lines)

    def create_job(self) -> Job:
        return Job(
            names=[self.name],
            description=f"Run the {self.name} script",
            depends_on=self.depends_on,
            job=self.perform_script(self.name, self.run_script, self.cwd),
        )

    @staticmethod
    def perform_script(
        name: str, script: str, cwd: Optional[str]
    ) -> Callable[[], Coroutine[None, None, bool]]:
        async def inner() -> bool:
            print(f"Running the {name} script...")
            result = await async_proc(script, cwd=cwd)
            success = not result.returncode
            if success:
                print(green(f"{name} script ran successfully"))
            else:
                print(red(f"{name} script failed"))
            return success

        return inner
