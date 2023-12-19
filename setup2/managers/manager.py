from dataclasses import dataclass
from typing import Protocol, List, Dict, Coroutine, Any, Tuple, Optional
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


@dataclass
class Resource(Protocol):
    name: str


class Manager(Protocol):
    check_results: List[Tuple[Any, bool, str]]

    def desired_printout(self) -> str:
        ...

    def status_printout(self, show_all: bool) -> str:
        ...

    def create_job(self, resource: Any) -> Optional[Job]:
        ...

    def get_statuses(self) -> Coroutine[Any, Any, List[str]]:
        ...
