from typing import Dict, List, Type

from setup.job import Job

from .command import Command
from .directory import Directory
from .exe import Exe
from .lib import Library
from .manager import Manager
from .package_types.apt import Apt
from .package_types.npm import Npm
from .package_types.pip import Pip
from .parser import Parser
from .sym import Symlink

__all__ = ["Command", "Directory", "Exe", "Library", "Manager", "Parser", "Symlink"]

ALL_MANAGERS: Dict[str, Type[Manager]] = {
    "command": Command,
    "directory": Directory,
    "exe": Exe,
    "library": Library,
    "parser": Parser,
    "symlink": Symlink,
}


def all_desired() -> List[Manager]:
    return [
        *Command.desired,
        *Directory.desired,
        *Exe.desired,
        *Library.desired,
        *Parser.desired,
        *Symlink.desired,
    ]


def create_jobs(selected_types: List[Type[Manager]]) -> Dict[str, Job]:
    jobs = {}
    for t in selected_types:
        for resource in t.desired:
            if resource.state[0]:
                continue
            if resource.state[1] == "BLOCKED":
                # TODO Add unblocking job
                pass
            else:
                job = resource.create_job()
                if job is not None:
                    jobs[resource.name] = job
    jobs.update(create_bonus_jobs())
    return jobs


def create_bonus_jobs() -> Dict[str, Job]:
    jobs = {}
    if len(Apt.all_apts) != 0:
        jobs["apt_install"] = Apt.apt_job()
    if len(Pip.all_pips) != 0:
        jobs["pip_install"] = Pip.pip_job()
    if len(Npm.all_packages) != 0:
        jobs["npm_install"] = Npm.npm_job()
    return jobs
