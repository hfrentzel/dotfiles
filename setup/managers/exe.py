import re
import shutil
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import (
    ClassVar,
    Optional,
    TypedDict,
    Union,
)

from setup.job import Job
from setup.managers.manager import Manager, Package, mark_resource
from setup.managers.package_types.apt import Apt
from setup.managers.package_types.build_hole import build_hole_builder
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
JOB_BUILDERS: dict[str, Callable[["Exe"], Union[bool, Job]]] = {
    "Apt": Apt.apt_builder,
    "bh": build_hole_builder,
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


class InstallerSpec(TypedDict):
    installer: str
    package_name: Optional[Union[str, list[str]]]
    apt_repo: Optional[str]
    post_script: Optional[list[str]]
    urls: Optional[dict[str, str]]


@dataclass
class Exe(Manager, Package):
    desired: ClassVar[list["Exe"]] = []
    name: str
    state: tuple[bool, str] = (False, "")
    version: str = ""
    installers: list[Union[InstallerSpec, str]] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    command_name: str = ""
    extract_path: Optional[str] = None
    version_cmd: str = ""
    url: str = ""
    repo: str = ""
    steps: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        mark_resource(self.name)
        if not self.command_name:
            self.command_name = self.name
        self.desired.append(self)

    async def _set_status(self) -> None:
        command = shutil.which(self.command_name)
        if command is None:
            self.state = False, "MISSING"
            return
        if not self.version:
            self.state = (True, "ANY")
            return

        # TODO This is a hack, make this better
        if self.version_cmd == "NPM":
            curr_ver = Npm.get_version(self)
        else:
            if self.version_cmd:
                subcommands = [self.version_cmd]
            else:
                subcommands = ["--version", "version", "-V", "-v"]
            for cmd in subcommands:
                version = await async_proc(
                    f"{self.command_name} {cmd}", forward_env=True
                )
                if version.returncode == 0:
                    break

            curr_ver = None
            if version.returncode != 0:
                if self.installers and set(self.installers) & {"Pip", "Npm"}:
                    if "Pip" in self.installers:
                        curr_ver = await Pip.get_version(self)
                    elif "Npm" in self.installers:
                        curr_ver = Npm.get_version(self)
            elif string := VERSION_REGEX.search(version.stdout):
                curr_ver = string.group(0)

        if curr_ver is not None:
            success = ver_greater_than(curr_ver, self.version)
            self.state = (success, curr_ver)
            return

        self.state = (False, "UNKNOWN")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for exe in sorted(cls.desired, key=lambda e: e.name):
            lines.append((exe.name, exe.version))
        return print_grid(("COMMAND", "VERSION"), lines)

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for exe in sorted(cls.desired, key=lambda e: e.name):
            if not show_all and exe.state[0]:
                continue
            lines.append((exe.name, exe.version, (exe.state[1], exe.state[0])))
        return print_grid(("COMMAND", "DESIRED", "CURRENT"), lines)

    def create_job(self) -> Optional[Job]:
        for t in self.installers:
            if isinstance(t, str):
                installer = t
            else:
                installer = t["installer"]
            settled = JOB_BUILDERS[installer](self)
            if isinstance(settled, Job):
                return settled
            if settled:
                break
        return None
