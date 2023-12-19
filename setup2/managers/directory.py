import os
from dataclasses import dataclass
from typing import Tuple, List, ClassVar, Callable, Coroutine

from setup2.job import Job
from setup2.output import print_grid
from setup2.managers.manager import mark_resource


@dataclass
class Dir():
    desired: ClassVar[List['Dir']] = []
    name: str
    path: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)


check_results: List[Tuple[Dir, bool, str]] = []


def current_status(directory: Dir) -> Tuple[bool, str]:
    path = os.path.expanduser(directory.path)
    if os.path.isdir(path):
        return (True, 'Exists')
    if os.path.exists(path):
        return (False, 'BLOCKED')
    return (False, 'MISSING')


def desired_printout() -> str:
    lines = []
    for directory in sorted(Dir.desired, key=(lambda d: d.path)):
        lines.append((directory.path,))
    return print_grid(('SUB-DIRECTORIES',), lines)


async def get_statuses() -> List[str]:
    complete = []
    for directory in Dir.desired:
        result = current_status(directory)
        if result[0]:
            complete.append(directory.name)
        check_results.append((directory, *result))
    return complete


def status_printout(show_all: bool) -> str:
    lines = []
    for directory, complete, status in sorted(check_results, key=(lambda d: d[0].path)):
        if not show_all and complete:
            continue
        lines.append((directory.path, (status, complete)))
    return print_grid(('SUB-DIRECTORIES', 'STATUS'), lines)


def create_job(directory: Dir) -> Job:
    return Job(
        names=[directory.name],
        description=f'Create directory at {directory.path}',
        job=create_directory(directory.path)
    )


def create_directory(path: str) -> Callable[[], Coroutine[None, None, bool]]:
    async def inner() -> bool:
        full_path = os.path.expanduser(path)
        print(f'Creating directory at {full_path}...')
        os.makedirs(full_path)

        return True

    return inner
