import asyncio
from dataclasses import dataclass
from typing import Tuple, ClassVar, List, Dict

from setup2.job import Job
from setup2.output import print_grid, red
from setup2.managers.package_types.pip import Pip
from setup2.managers.package_types.npm import Npm


@dataclass
class Lib:
    desired: ClassVar[List['Lib']] = []
    name: str
    version: str
    manager: str

    def __post_init__(self) -> None:
        self.desired.append(self)


check_results = []


async def check_job(lib: Lib) -> Tuple[Lib, bool, str]:
    if lib.manager == 'pip':
        return (lib, *Pip.check_install(lib))
    if lib.manager == 'npm':
        return (lib, *Npm.check_install(lib))

    return (lib, False, red('UNKNOWN'))


def desired_printout() -> str:
    lines = []
    for lib in sorted(Lib.desired, key=(lambda b: b.name)):
        lines.append((lib.name, lib.version))
    return print_grid(('LIBRARY', 'VERSION'), lines)


async def get_statuses() -> None:
    tasks = []
    for lib in Lib.desired:
        tasks.append(check_job(lib))
    check_results.extend(await asyncio.gather(*tasks))


def status_printout(show_all: bool) -> str:
    lines = []
    for lib, complete, curr_ver in sorted(check_results, key=(lambda b: b[0].name)):
        if not show_all and complete:
            continue
        lines.append((lib.name, lib.version, curr_ver))
    return print_grid(('LIBRARY', 'DESIRED', 'CURRENT'), lines)


JOB_BUILDERS = {
    'pip': Pip.pip_builder,
    'npm': Npm.npm_builder
}


def create_jobs() -> Tuple[List[str], Dict[str, Job]]:
    no_action_needed = []
    jobs = {}
    for lib, complete, curr_ver in check_results:
        if complete:
            no_action_needed.append(lib.name)
            continue
        JOB_BUILDERS[lib.manager](lib)
    if len(Pip.all_pips) != 0:
        jobs['pip_install'] = Pip.pip_job()
    if len(Npm.all_packages) != 0:
        jobs['npm_install'] = Npm.npm_job()

    return no_action_needed, jobs
