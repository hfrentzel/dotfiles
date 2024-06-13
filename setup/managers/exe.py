import asyncio
import os
import re
import shutil
from typing import Callable, Dict, List, Optional, Tuple, Union

from setup.job import Job
from setup.managers.exe_class import Exe
from setup.managers.exe_class import desired as desired
from setup.managers.package_types.apt import Apt
from setup.managers.package_types.cargo import cargo_builder
from setup.managers.package_types.deb import deb_builder
from setup.managers.package_types.github import Github
from setup.managers.package_types.gitlab import Gitlab
from setup.managers.package_types.go import go_builder
from setup.managers.package_types.npm import Npm
from setup.managers.package_types.pip import Pip
from setup.managers.package_types.sequence import sequence_builder
from setup.managers.package_types.tar import tar_builder
from setup.managers.package_types.zip import zip_builder
from setup.output import print_grid
from setup.process import async_proc, ver_greater_than

VERSION_REGEX = re.compile(r"\d+\.\d+(\.\d+)?", re.M)


"""
Installers:
Apt, Deb, Pip, Npm, Tar
#TODO validate elements of installers list are valid
"""

Resource = Exe

check_results: List[Tuple[Exe, bool, str]] = []


async def current_status(exe: Exe) -> Tuple[Exe, bool, str]:
    command = shutil.which(exe.command_name)
    if command is None:
        return (exe, False, "MISSING")
    if not exe.version:
        return (exe, True, "ANY")

    if exe.version_cmd:
        subcommands = [exe.version_cmd]
    else:
        subcommands = ["--version", "version", "-V", "-v"]
    for cmd in subcommands:
        version = await async_proc(f"{exe.command_name} {cmd}", forward_env=True)
        if version.returncode == 0:
            break

    curr_ver = None
    if version.returncode != 0:
        if exe.installers and set(exe.installers) & {"Pip", "Npm"}:
            if "Pip" in exe.installers:
                curr_ver = Pip.get_version(exe)
            elif "Npm" in exe.installers:
                curr_ver = Npm.get_version(exe)
    elif string := VERSION_REGEX.search(version.stdout):
        curr_ver = string.group(0)

    if curr_ver is not None:
        success = ver_greater_than(curr_ver, exe.version)
        return (exe, success, curr_ver)

    return (exe, False, "UNKNOWN")


def desired_printout() -> str:
    lines = []
    for exe in sorted(desired, key=(lambda e: e.name)):
        lines.append((exe.name, exe.version))
    return print_grid(("COMMAND", "VERSION"), lines)


async def get_statuses() -> List[str]:
    local_bin = os.path.expanduser("~/.local/bin")
    if local_bin not in os.environ["PATH"]:
        os.environ["PATH"] += ":" + local_bin

    complete = []
    tasks = []
    for exe in desired:
        tasks.append(current_status(exe))
    results = await asyncio.gather(*tasks)
    check_results.extend(results)
    for result in results:
        if result[1]:
            complete.append(result[0].name)
    return complete


def status_printout(show_all: bool) -> str:
    lines = []
    for exe, complete, curr_ver in sorted(check_results, key=(lambda e: e[0].name)):
        if not show_all and (complete or exe.on_demand):
            continue
        lines.append((exe.name, exe.version, (curr_ver, complete)))
    return print_grid(("COMMAND", "DESIRED", "CURRENT"), lines)


JOB_BUILDERS: Dict[str, Callable[[Exe, str], Union[bool, Job]]] = {
    "Apt": Apt.apt_builder,
    "Cargo": cargo_builder,
    "Deb": deb_builder,
    "Github": Github.github_builder,
    "Gitlab": Gitlab.gitlab_builder,
    "Go": go_builder,
    "Npm": Npm.npm_builder,
    "Pip": Pip.pip_builder,
    "Sequence": sequence_builder,
    "Tar": tar_builder,
    "Zip": zip_builder,
}


def create_job(exe: Exe) -> Optional[Job]:
    for t in exe.installers:
        if isinstance(t, str):
            installer = t
            package = exe.name
        else:
            installer = t["installer"]
            package = t.get("package_name") or exe.name
        settled = JOB_BUILDERS[installer](exe, package)
        if isinstance(settled, Job):
            return settled
        if settled:
            break
    return None


def create_bonus_jobs() -> Dict[str, Job]:
    jobs = {}
    if len(Apt.all_apts) != 0:
        jobs["apt_install"] = Apt.apt_job()
    if len(Pip.all_pips) != 0:
        jobs["pip_install"] = Pip.pip_job()
    if len(Npm.all_packages) != 0:
        jobs["npm_install"] = Npm.npm_job()
    return jobs