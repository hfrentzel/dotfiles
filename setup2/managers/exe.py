import asyncio
import re
import shutil
from typing import List, Tuple, Dict, Callable, Union

from setup2.job import Job
from setup2.process import async_proc, ver_greater_than
from setup2.output import print_grid, red, green, yellow
from setup2.managers.exe_class import Exe
from setup2.managers.package_types.apt import Apt
from setup2.managers.package_types.cargo import cargo_builder
from setup2.managers.package_types.go import go_builder
from setup2.managers.package_types.deb import deb_builder
from setup2.managers.package_types.github import Github
from setup2.managers.package_types.gitlab import Gitlab
from setup2.managers.package_types.pip import Pip
from setup2.managers.package_types.sequence import sequence_builder
from setup2.managers.package_types.npm import Npm
from setup2.managers.package_types.tar import tar_builder
from setup2.managers.package_types.zip import zip_builder

VERSION_REGEX = re.compile(r'\d+\.\d+\.\d+', re.M)


"""
Installers:
Apt, Deb, Pip, Npm, Tar
#TODO validate elements of installers list are valid
"""


check_results: List[Tuple[Exe, bool, str]] = []


async def check_job(exe: Exe) -> Tuple[Exe, bool, str]:
    fail_color = yellow if exe.on_demand else red
    command = shutil.which(exe.command_name)
    if command is None:
        return (exe, False, fail_color('MISSING'))
    if exe.version == '':
        return (exe, True, green('ANY'))

    subcommands = ["--version", "version", "-V", "-v"]
    for cmd in subcommands:
        version = await async_proc(f'{exe.command_name} {cmd}')
        if version.returncode == 0:
            break

    curr_ver = None
    if version.returncode != 0:
        if exe.installers and set(exe.installers) & {'Pip', 'Npm'}:
            if 'Pip' in exe.installers:
                curr_ver = Pip.get_version(exe)
            elif 'Npm' in exe.installers:
                curr_ver = Npm.get_version(exe)
    elif string := VERSION_REGEX.search(version.stdout):
        curr_ver = string.group(0)

    if curr_ver is not None:
        success = ver_greater_than(curr_ver, exe.version)
        color = green if success else fail_color
        return (exe, success, color(curr_ver))

    return (exe, False, fail_color('UNKNOWN'))


def desired_printout() -> str:
    lines = []
    for exe in sorted(Exe.desired, key=(lambda e: e.name)):
        lines.append((exe.name, exe.version))
    return print_grid(('COMMAND', 'VERSION'), lines)


async def get_statuses() -> None:
    tasks = []
    for exe in Exe.desired:
        tasks.append(check_job(exe))
    check_results.extend(await asyncio.gather(*tasks))


def status_printout(show_all: bool) -> str:
    lines = []
    for exe, complete, curr_ver in sorted(check_results, key=(lambda e: e[0].name)):
        if not show_all and (complete or exe.on_demand):
            continue
        lines.append((exe.name, exe.version, curr_ver))
    return print_grid(('COMMAND', 'DESIRED', 'CURRENT'), lines)


JOB_BUILDERS: Dict[str, Callable[[Exe], Union[bool, Job]]] = {
    'Apt': Apt.apt_builder,
    'Cargo': cargo_builder,
    'Deb': deb_builder,
    'Github': Github.github_builder,
    'Gitlab': Gitlab.gitlab_builder,
    'Go': go_builder,
    'Npm': Npm.npm_builder,
    'Pip': Pip.pip_builder,
    'Sequence': sequence_builder,
    'Tar': tar_builder,
    'Zip': zip_builder,
}


def create_jobs() -> Tuple[List[str], Dict[str, Job]]:
    """
    Determine which installers are available
        - Apt and Deb require root permissions
        - Pip and Npm require those exes
        - Tar requires gh for github discovery
    """
    no_action_needed = []
    jobs = {}
    for exe, complete, curr_verr in check_results:
        if complete:
            no_action_needed.append(exe.name)
            continue
        if exe.installers is None:
            break
        for t in exe.installers:
            settled = JOB_BUILDERS[t](exe)
            if isinstance(settled, Job):
                jobs[exe.name] = settled
            if settled:
                break
    if len(Apt.all_apts) != 0:
        jobs['apt_install'] = Apt.apt_job()
    if len(Pip.all_pips) != 0:
        jobs['pip_install'] = Pip.pip_job()
    if len(Npm.all_packages) != 0:
        jobs['npm_install'] = Npm.npm_job()

    return no_action_needed, jobs
