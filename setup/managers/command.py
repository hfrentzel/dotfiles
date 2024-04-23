import asyncio
import os
from dataclasses import dataclass
from typing import Callable, Coroutine, List, Optional, Tuple

from setup.conf import conf
from setup.job import Job
from setup.managers.manager import mark_resource
from setup.output import green, print_grid, red
from setup.process import async_proc


@dataclass
class Resource:
    name: str
    run_script: str
    check_script: Optional[str] = None
    depends_on: Optional[str] = None
    cwd: Optional[str] = None

    def __post_init__(self) -> None:
        mark_resource(self.name)
        desired.append(self)


desired: List[Resource] = []
check_results: List[Tuple[Resource, bool, str]] = []


async def current_status(command: Resource) -> Tuple[Resource, bool, str]:
    if isinstance(command.cwd, str):
        command.cwd = os.path.expanduser(command.cwd.replace("DOT", conf.dotfiles_home))

    if command.check_script is None:
        return (command, False, "CANT VERIFY")
    result = await async_proc(command.check_script, cwd=command.cwd)
    if result.returncode == 0:
        return (command, True, "DONE")

    return (command, False, "INCOMPLETE")


async def get_statuses() -> List[str]:
    complete = []
    tasks = []
    for command in desired:
        tasks.append(current_status(command))
    results = await asyncio.gather(*tasks)
    check_results.extend(results)
    for result in results:
        if result[1]:
            complete.append(result[0].name)
    return complete


def desired_printout() -> str:
    lines = []
    for command in sorted(desired, key=(lambda c: c.name)):
        lines.append((command.name,))
    return print_grid(("SCRIPTS",), lines)


def status_printout(show_all: bool) -> str:
    lines = []
    for command, complete, status in sorted(check_results, key=(lambda c: c[0].name)):
        if not show_all and complete:
            continue
        lines.append((command.name, (status, complete)))
    return print_grid(("SCRIPT", "STATUS"), lines)


def create_job(command: Resource) -> Job:
    return Job(
        names=[command.name],
        description=f"Run the {command.name} script",
        depends_on=command.depends_on,
        job=run_script(command.name, command.run_script, command.cwd),
    )


def run_script(
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
