from dataclasses import dataclass
from typing import Dict, List, Protocol, Tuple, Any, Coroutine, Optional, ClassVar
from setup2.job import Job
from .directory import Dir
from .exe_class import Exe
from .exe import create_bonus_jobs
from .sym import Sym
from .lib import Lib
from .command import Command
from .parser import Parser

__all__ = ['Dir', 'Exe', 'Sym', 'Lib', 'Command', 'Parser']


@dataclass
class Spec(Protocol):
    desired: ClassVar[List[Any]]
    name: str


class Manager(Protocol):

    check_results: List[Tuple[Any, bool, str]]

    def desired_printout(self) -> str:
        ...

    def status_printout(self, show_all: bool) -> str:
        ...

    def create_job(self, resource: Any) -> Optional[Job]:
        ...

    def get_statuses(self) -> Coroutine[None, None, List[str]]:
        ...


def all_desired() -> List[Spec]:
    return [*Dir.desired, *Exe.desired, *Sym.desired, *Lib.desired,
            *Command.desired, *Parser.desired]


def create_jobs(selected_types: List[Manager]) -> Dict[str, Job]:
    jobs = {}
    for t in selected_types:
        for resource, complete, status in t.check_results:
            if complete:
                continue
            if status == 'BLOCKED':
                # TODO Add unblocking job
                pass
            else:
                job = t.create_job(resource)
                if job is not None:
                    jobs[resource.name] = job
    jobs.update(create_bonus_jobs())
    return jobs
