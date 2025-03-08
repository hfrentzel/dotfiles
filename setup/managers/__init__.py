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

__all__ = [
    "Command",
    "Directory",
    "Exe",
    "Library",
    "Manager",
    "Parser",
    "Symlink",
]

ALL_MANAGERS: dict[str, type[Manager]] = {
    "command": Command,
    "directory": Directory,
    "exe": Exe,
    "library": Library,
    "parser": Parser,
    "symlink": Symlink,
}


def all_desired() -> list[Manager]:
    return [
        *Command.desired,
        *Directory.desired,
        *Exe.desired,
        *Library.desired,
        *Parser.desired,
        *Symlink.desired,
    ]


def create_bonus_jobs() -> dict[str, Job]:
    jobs = {}
    if len(Apt.all_apts) != 0:
        jobs["apt_install"] = Apt.apt_job()
    if len(Pip.all_pips) != 0:
        jobs["pip_install"] = Pip.pip_job()
    if len(Npm.all_packages) != 0:
        jobs["npm_install"] = Npm.npm_job()
    if len(Parser.jobs) != 0:
        jobs["nvim_init"] = Parser.nvim_init_job()
    return jobs
