from typing import Dict, List, Type

from setup.job import Job

from .command import Command
from .directory import Directory
from .exe import Exe as Exe
from .lib import Library
from .manager import Manager as Manager
from .parser import Parser
from .sym import Symlink

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
        for resource, complete, status in t.check_results:
            if complete:
                continue
            if status == "BLOCKED":
                # TODO Add unblocking job
                pass
            else:
                job = resource.create_job()
                if job is not None:
                    jobs[resource.name] = job
    jobs.update(Exe.create_bonus_jobs())
    return jobs
