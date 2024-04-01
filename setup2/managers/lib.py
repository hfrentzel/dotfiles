import asyncio
from dataclasses import dataclass
from typing import Tuple, List

from setup2.output import print_grid
from setup2.managers.manager import mark_resource
from setup2.managers.package_types.pip import Pip
from setup2.managers.package_types.npm import Npm


@dataclass
class Resource:
    name: str
    version: str
    manager: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        desired.append(self)


desired: List[Resource] = []
check_results = []


async def current_status(lib: Resource) -> Tuple[Resource, bool, str]:
    if lib.manager == 'pip':
        return (lib, *Pip.check_install(lib))
    if lib.manager == 'npm':
        return (lib, *Npm.check_install(lib))

    return (lib, False, 'UNKNOWN')


def desired_printout() -> str:
    lines = []
    for lib in sorted(desired, key=(lambda b: b.name)):
        lines.append((lib.name, lib.version))
    return print_grid(('LIBRARY', 'VERSION'), lines)


async def get_statuses() -> List[str]:
    complete = []
    tasks = []
    for lib in desired:
        tasks.append(current_status(lib))
    results = await asyncio.gather(*tasks)
    check_results.extend(results)
    for result in results:
        if result[1]:
            complete.append(result[0].name)
    return complete


def status_printout(show_all: bool) -> str:
    lines = []
    for lib, complete, curr_ver in sorted(check_results, key=(lambda b: b[0].name)):
        if not show_all and complete:
            continue
        lines.append((lib.name, lib.version, (curr_ver, complete)))
    return print_grid(('LIBRARY', 'DESIRED', 'CURRENT'), lines)


JOB_BUILDERS = {
    'pip': Pip.pip_builder,
    'npm': Npm.npm_builder
}


def create_job(lib: Resource) -> None:
    JOB_BUILDERS[lib.manager](lib, lib.name)
