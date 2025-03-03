import asyncio
import logging
from dataclasses import dataclass, field
from typing import Awaitable, Callable, List, Optional


@dataclass
class Job:
    name: str
    job: Callable[[logging.Logger], Awaitable[bool]]
    description: str
    resources: List[str] = field(default_factory=list)
    depends_on: Optional[List[str]] = None
    children: List["Job"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.resources) == 0:
            self.resources = [self.name]

    async def run(self) -> bool:
        try:
            logger = logging.getLogger(self.name)
            result = await self.job(logger)
            if result and len(self.children) != 0:
                runners = [job.run() for job in self.children]
                result = all(await asyncio.gather(*runners))
        except Exception as e:
            logger.error(e)
            result = False
        return result

    def __repr__(self) -> str:
        return f"{self.resources}, {self.job}"


def print_job_tree(
    jobs: List[Job], level: int = 0, parent_is_last: bool = True
) -> None:
    for i, job in enumerate(jobs):
        is_last_item = i == len(jobs) - 1

        front = ("   " if parent_is_last else "│  ") * level
        if len(job.resources) == 1 and job.resources[0] == job.name:
            output = job.name
        else:
            output = f"{job.name}({','.join(job.resources)})"
        if is_last_item:
            print(f"{front}└──{output}")
        else:
            print(f"{front}├──{output}")

        if len(job.children) != 0:
            print_job_tree(job.children, level + 1, is_last_item)
