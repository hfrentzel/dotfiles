from dataclasses import dataclass
from typing import Any, Coroutine, Dict, List, Optional, Protocol, Sequence, Tuple, Type

from setup2.job import Job

from . import command, directory, exe, lib, parser, sym
from .exe import create_bonus_jobs


@dataclass
class Spec(Protocol):
    name: str


# https://github.com/python/mypy/issues/7041
class Manager(Protocol):
    @property
    def Resource(self) -> Type[Spec]:  # pylint: disable=invalid-name
        ...

    @property
    def desired(self) -> Sequence[Spec]: ...

    @property
    def check_results(self) -> Sequence[Tuple[Spec, bool, str]]: ...

    def desired_printout(self) -> str: ...

    def status_printout(self, show_all: bool) -> str: ...

    def create_job(self, resource: Any) -> Optional[Job]: ...

    def get_statuses(self) -> Coroutine[None, None, List[str]]: ...


ALL_MANAGERS: Dict[str, Manager] = {
    "command": command,
    "directory": directory,
    "exe": exe,
    "library": lib,
    "parser": parser,
    "symlink": sym,
}


def all_desired() -> List[Spec]:
    return [
        *command.desired,
        *directory.desired,
        *exe.desired,
        *lib.desired,
        *parser.desired,
        *sym.desired,
    ]


def create_jobs(selected_types: List[Manager]) -> Dict[str, Job]:
    jobs = {}
    for t in selected_types:
        for resource, complete, status in t.check_results:
            if complete:
                continue
            if status == "BLOCKED":
                # TODO Add unblocking job
                pass
            else:
                job = t.create_job(resource)
                if job is not None:
                    jobs[resource.name] = job
    jobs.update(create_bonus_jobs())
    return jobs
