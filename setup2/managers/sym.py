import os
from dataclasses import dataclass
from typing import ClassVar, List, Tuple, Coroutine, Callable

from setup2.conf import conf
from setup2.job import Job
from setup2.output import print_grid
from setup2.managers.manager import mark_resource


@dataclass
class Sym:
    desired: ClassVar[List['Sym']] = []
    name: str
    source: str
    target: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)


check_results: List[Tuple[Sym, bool, str]] = []


def current_status(sym: Sym) -> Tuple[bool, str]:
    dest = os.path.expanduser(sym.target)
    if os.path.isfile(dest) or os.path.isdir(dest):
        if os.path.islink(dest):
            return (True, 'LINKED')
        return (False, 'BLOCKED')
    return (False, 'MISSING')


def desired_printout() -> str:
    lines = []
    for sym in sorted(Sym.desired, key=lambda s: s.target):
        lines.append((sym.target,))
    return print_grid(('SYMLINKED FILES',), lines)


async def get_statuses() -> List[str]:
    complete = []
    for sym in Sym.desired:
        result = current_status(sym)
        if result[0]:
            complete.append(sym.name)
        check_results.append((sym, *result))
    return complete


def status_printout(show_all: bool) -> str:
    lines = []
    for sym, complete, status in sorted(check_results, key=(lambda s: s[0].name)):
        if not show_all and complete:
            continue
        lines.append((sym.name, (status, complete)))
    return print_grid(('SYMLINK', 'STATUS'), lines)


def create_job(sym: Sym) -> Job:
    return Job(
        names=[sym.name],
        description=f'Generate symlink at {sym.target}',
        job=create_symlink(sym.source, sym.target)
    )


def create_symlink(source: str, target: str) -> Callable[[], Coroutine[None, None, bool]]:
    async def inner() -> bool:
        src = source.replace('DOT', conf.dotfiles_home)
        src = os.path.expanduser(src)
        dest = os.path.expanduser(target)
        print(f'Creating symlink at {dest}...')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        os.symlink(src, dest)

        return True

    return inner
