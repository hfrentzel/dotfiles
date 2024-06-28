import asyncio
import os
import re
import shutil
from dataclasses import dataclass, field
from typing import Callable, ClassVar, Dict, List, Optional, Tuple, TypedDict, Union

from setup.job import Job
from setup.managers.manager import Manager, Package, mark_resource
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
JOB_BUILDERS: Dict[str, Callable[["Exe", str], Union[bool, Job]]] = {
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


"""
Installers:
Apt, Deb, Pip, Npm, Tar
#TODO validate elements of installers list are valid
"""


@dataclass
class InstallerSpec(TypedDict):
    installer: str
    package_name: Optional[str]
    post_script: Optional[List[str]]


@dataclass
class Exe(Manager, Package):
    desired: ClassVar[List["Exe"]] = []
    check_results: ClassVar[List[Tuple["Exe", bool, str]]] = []
    name: str
    version: str = ""
    installers: List[Union[InstallerSpec, str]] = field(default_factory=list)
    depends_on: Optional[str] = None
    on_demand: bool = False
    command_name: str = ""
    extract_path: Optional[str] = None
    version_cmd: str = ""
    url: str = ""
    repo: str = ""
    steps: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        mark_resource(self.name)
        if not self.command_name:
            self.command_name = self.name
        self.desired.append(self)

    async def current_status(self) -> Tuple["Exe", bool, str]:
        command = shutil.which(self.command_name)
        if command is None:
            return (self, False, "MISSING")
        if not self.version:
            return (self, True, "ANY")

        if self.version_cmd:
            subcommands = [self.version_cmd]
        else:
            subcommands = ["--version", "version", "-V", "-v"]
        for cmd in subcommands:
            version = await async_proc(f"{self.command_name} {cmd}", forward_env=True)
            if version.returncode == 0:
                break

        curr_ver = None
        if version.returncode != 0:
            if self.installers and set(self.installers) & {"Pip", "Npm"}:
                if "Pip" in self.installers:
                    curr_ver = Pip.get_version(self)
                elif "Npm" in self.installers:
                    curr_ver = Npm.get_version(self)
        elif string := VERSION_REGEX.search(version.stdout):
            curr_ver = string.group(0)

        if curr_ver is not None:
            success = ver_greater_than(curr_ver, self.version)
            return (self, success, curr_ver)

        return (self, False, "UNKNOWN")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for exe in sorted(cls.desired, key=(lambda e: e.name)):
            lines.append((exe.name, exe.version))
        return print_grid(("COMMAND", "VERSION"), lines)

    @classmethod
    async def get_statuses(cls) -> List[str]:
        local_bin = os.path.expanduser("~/.local/bin")
        if local_bin not in os.environ["PATH"]:
            os.environ["PATH"] += ":" + local_bin

        complete = []
        tasks = []
        for exe in cls.desired:
            tasks.append(exe.current_status())
        results = await asyncio.gather(*tasks)
        cls.check_results.extend(results)
        for result in results:
            if result[1]:
                complete.append(result[0].name)
        return complete

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for exe, complete, curr_ver in sorted(cls.check_results, key=(lambda e: e[0].name)):
            if not show_all and (complete or exe.on_demand):
                continue
            lines.append((exe.name, exe.version, (curr_ver, complete)))
        return print_grid(("COMMAND", "DESIRED", "CURRENT"), lines)

    def create_job(self) -> Optional[Job]:
        for t in self.installers:
            if isinstance(t, str):
                installer = t
                package = self.name
            else:
                installer = t["installer"]
                package = t.get("package_name") or self.name
            settled = JOB_BUILDERS[installer](self, package)
            if isinstance(settled, Job):
                return settled
            if settled:
                break
        return None

    @staticmethod
    def create_bonus_jobs() -> Dict[str, Job]:
        jobs = {}
        if len(Apt.all_apts) != 0:
            jobs["apt_install"] = Apt.apt_job()
        if len(Pip.all_pips) != 0:
            jobs["pip_install"] = Pip.pip_job()
        if len(Npm.all_packages) != 0:
            jobs["npm_install"] = Npm.npm_job()
        return jobs


Exe(
    "go",
    version="1.20.11",
    on_demand=True,
    installers=["Tar"],
    extract_path="~/.local",
    url="https://go.dev/dl/go{version}.linux-amd64.tar.gz",
)

Exe(
    "node",
    version="18.13.0",
    installers=["Tar"],
    on_demand=True,
    url="https://nodejs.org/dist/v{version}/node-v{version}-linux-x64.tar.xz",
)
