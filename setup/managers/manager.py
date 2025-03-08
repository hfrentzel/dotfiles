from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar, Optional

from setup.job import Job

_all_resources: list[str] = []


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
    state: tuple[bool, str]
    desired: ClassVar[Sequence["Manager"]]

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

    @abstractmethod
    async def _set_status(self) -> None:
        pass

    async def get_status(self) -> bool:
        await self._set_status()
        return self.state[0]
