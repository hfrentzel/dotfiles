from dataclasses import dataclass
from typing import Protocol, Tuple, List, Dict, Coroutine, Any
from setup2.job import Job

_all_resources: List[str] = []


def mark_resource(name: str, override: bool = False) -> None:
    if name in _all_resources:
        if override:
            return
        raise ValueError(f'{name} resource is defined more than once')
    _all_resources.append(name)


@dataclass
class Package(Protocol):
    name: str
    version: str


class Manager(Protocol):
    def desired_printout(self) -> str:
        ...

    def status_printout(self, show_all: bool) -> str:
        ...

    def create_jobs(self) -> Tuple[List[str], Dict[str, Job]]:
        ...

    def get_statuses(self) -> Coroutine[Any, Any, None]:
        ...
