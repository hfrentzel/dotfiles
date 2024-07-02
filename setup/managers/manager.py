from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, List, Optional, Sequence, Tuple

from setup.job import Job

_all_resources: List[str] = []


def mark_resource(name: str) -> None:
    if name in _all_resources:
        raise ValueError(f"{name} resource is defined more than once")
    _all_resources.append(name)


@dataclass
class Package(ABC):
    name: str
    version: str


# https://github.com/python/mypy/issues/7041
class Manager(ABC):
    name: str
    state: Tuple[bool, str]
    desired: ClassVar[Sequence["Manager"]]

    @abstractmethod
    async def set_status(self) -> None:
        pass

    @classmethod
    @abstractmethod
    def desired_printout(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def status_printout(cls, show_all: bool) -> str:
        pass

    @abstractmethod
    def create_job(self) -> Optional[Job]:
        pass

    @classmethod
    @abstractmethod
    async def get_statuses(cls) -> List[str]:
        pass
