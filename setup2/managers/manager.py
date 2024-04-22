from dataclasses import dataclass
from typing import Protocol, List

_all_resources: List[str] = []


def mark_resource(name: str) -> None:
    if name in _all_resources:
        raise ValueError(f"{name} resource is defined more than once")
    _all_resources.append(name)


@dataclass
class Package(Protocol):
    name: str
    version: str
