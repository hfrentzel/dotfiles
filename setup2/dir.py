import os
from dataclasses import dataclass
from typing import Tuple, List, ClassVar, Callable, Dict, Coroutine
from .job import Job
from .output import print_grid, red, green


@dataclass
class Dir():
    desired: ClassVar[List['Dir']] = []
    name: str
    path: str

    def __post_init__(self) -> None:
        self.desired.append(self)


check_results: List[Tuple[Dir, bool, str]] = []


def check_job(directory: Dir) -> Tuple[bool, str]:
    path = os.path.expanduser(directory.path)
    if os.path.isdir(path):
        return (True, green('Exists'))
    if os.path.exists(path):
        return (False, red('BLOCKED'))
    return (False, red('MISSING'))


def desired_printout() -> str:
    lines = []
    for directory in sorted(Dir.desired, key=(lambda d: d.path)):
        lines.append((directory.path,))
    return print_grid(('SUB-DIRECTORIES',), lines)


async def get_statuses() -> None:
    for directory in Dir.desired:
        check_results.append((directory, *check_job(directory)))


def status_printout(show_all: bool) -> str:
    lines = []
    for directory, complete, status in sorted(check_results, key=(lambda d: d[0].path)):
        if not show_all and complete:
            continue
        lines.append((directory.path, status))
    return print_grid(('SUB-DIRECTORIES', 'STATUS'), lines)


def create_jobs() -> Tuple[List[str], Dict[str, Job]]:
    no_action_needed = []
    jobs = {}
    for directory, complete, status in check_results:
        if complete:
            no_action_needed.append(directory.name)
        elif status == 'BLOCKED':
            # TODO Add unblocking job
            pass
        else:
            jobs[directory.name] = Job(
                names=[directory.name],
                description=f'Create directory at {directory.path}',
                job=create_directory(directory.path)
            )

    return no_action_needed, jobs


def create_directory(path: str) -> Callable[[], Coroutine[None, None, bool]]:
    async def inner() -> bool:
        full_path = os.path.expanduser(path)
        print(f'Creating directory at {full_path}...')
        os.makedirs(full_path)

        return True

    return inner
