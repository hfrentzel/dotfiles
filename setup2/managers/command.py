import asyncio
import os
from dataclasses import dataclass
from typing import Tuple, Callable, Dict, Coroutine, List, ClassVar, Optional

from setup2.conf import conf
from setup2.job import Job
from setup2.process import async_proc
from setup2.output import print_grid, red, green
from setup2.managers.manager import mark_resource


@dataclass
class Command():
    desired: ClassVar[List['Command']] = []
    name: str
    run_script: str
    check_script: Optional[str] = None
    depends_on: Optional[str] = None
    cwd: Optional[str] = None

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)


check_results: List[Tuple[Command, bool, str]] = []


async def check_job(command: Command) -> Tuple[Command, bool, str]:
    if isinstance(command.cwd, str):
        command.cwd = os.path.expanduser(command.cwd.replace('DOT', conf.dotfiles_home))

    if command.check_script is None:
        return (command, False, 'CANT VERIFY')
    result = await async_proc(command.check_script, cwd=command.cwd)
    if result.returncode == 0:
        return (command, True, green('DONE'))

    return (command, False, red('INCOMPLETE'))


async def get_statuses() -> None:
    tasks = []
    for command in Command.desired:
        tasks.append(check_job(command))
    check_results.extend(await asyncio.gather(*tasks))


def desired_printout() -> str:
    lines = []
    for command in sorted(Command.desired, key=(lambda c: c.name)):
        lines.append((command.name,))
    return print_grid(('SCRIPTS',), lines)


def status_printout(show_all: bool) -> str:
    lines = []
    for command, complete, status in sorted(check_results, key=(lambda c: c[0].name)):
        if not show_all and complete:
            continue
        lines.append((command.name, status))
    return print_grid(('SCRIPT', 'STATUS'), lines)


def create_jobs() -> Tuple[List[str], Dict[str, Job]]:
    no_action_needed = []
    jobs = {}
    for command, complete, status in check_results:
        if complete:
            no_action_needed.append(command.name)
            continue
        jobs[command.name] = Job(
            names=[command.name],
            description=f'Run the {command.name} script',
            depends_on=command.depends_on,
            job=run_script(command.name, command.run_script,
                           command.cwd)
        )

    return no_action_needed, jobs


def run_script(name: str, script: str, cwd: Optional[str]) -> \
        Callable[[], Coroutine[None, None, bool]]:
    async def inner() -> bool:
        print(f'Running the {name} script...')
        result = await async_proc(script, cwd=cwd)
        success = not result.returncode
        if success:
            print(green(f'{name} script ran successfully'))
        else:
            print(red(f'{name} script failed'))
        return success

    return inner
