import os
from dataclasses import dataclass
from typing import ClassVar, List, Tuple, Dict, Coroutine, Callable
from .job import Job
from .conf import conf
from .output import print_grid, red, green


@dataclass
class Sym:
    desired: ClassVar[List['Sym']] = []
    name: str
    source: str
    target: str

    def __post_init__(self) -> None:
        self.desired.append(self)


check_results: List[Tuple[Sym, bool, str]] = []


def check_job(sym: Sym) -> Tuple[bool, str]:
    dest = os.path.expanduser(sym.target)
    if os.path.isfile(dest) or os.path.isdir(dest):
        if os.path.islink(dest):
            return (True, green('LINKED'))
        return (False, red('BLOCKED'))
    return (False, red('MISSING'))


def desired_printout() -> str:
    lines = []
    for sym in sorted(Sym.desired, key=lambda s: s.target):
        lines.append((sym.target,))
    return print_grid(('SYMLINKED FILES',), lines)


async def get_statuses() -> None:
    for sym in Sym.desired:
        check_results.append((sym, *check_job(sym)))


def status_printout(show_all: bool) -> str:
    lines = []
    for sym, complete, status in sorted(check_results, key=(lambda s: s[0].name)):
        if not show_all and complete:
            continue
        lines.append((sym.name, status))
    return print_grid(('SYMLINK', 'STATUS'), lines)


def create_jobs() -> Tuple[List[str], Dict[str, Job]]:
    no_action_needed = []
    jobs = {}
    for sym, complete, status in check_results:
        if complete:
            no_action_needed.append(sym.name)
        elif status == 'BLOCKED':
            # TODO Add unblocking job
            pass
        else:
            jobs[sym.name] = Job(
                names=[sym.name],
                description=f'Generate symlink at {sym.target}',
                job=create_symlink(sym.source, sym.target)
            )

    return no_action_needed, jobs


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
