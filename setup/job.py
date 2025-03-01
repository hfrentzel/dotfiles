import asyncio
import logging
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Dict, List, Optional


@dataclass
class Job:
    name: str
    job: Callable[[logging.Logger], Awaitable[bool]]
    description: str
    resources: List[str] = field(default_factory=list)
    depends_on: Optional[str] = None
    on_demand: bool = False
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
        if is_last_item:
            print(f"{front}└──{job.resources}")
        else:
            print(f"{front}├──{job.resources}")

        if len(job.children) != 0:
            print_job_tree(job.children, level + 1, is_last_item)


def build_tree(jobs: Dict[str, Job], complete: List[str]) -> List[Job]:
    root_jobs = []
    for job_name, job in jobs.items():
        if job.on_demand and not any(
            j.depends_on in job.resources for j in jobs.values()
        ):
            continue
        if job.depends_on is None:
            root_jobs.append(job)
        elif job.depends_on in complete:
            root_jobs.append(job)
        else:
            try:
                parent = next(
                    j for j in jobs.values() if job.depends_on in j.resources
                )
            except StopIteration:
                print(
                    f"The dependency '{job.depends_on}' for job '{job_name}' "
                    "is missing"
                )
            parent.children.append(job)

    return root_jobs
