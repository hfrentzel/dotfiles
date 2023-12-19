import asyncio
from dataclasses import dataclass, field
from typing import List, Callable, Optional, Awaitable, Dict


@dataclass
class Job:
    names: List[str]
    job: Callable[[], Awaitable[bool]]
    description: str
    depends_on: Optional[str] = None
    on_demand: bool = False
    children: List['Job'] = field(default_factory=list)

    async def run(self) -> bool:
        try:
            result = await self.job()
            if result and len(self.children) != 0:
                runners = [job.run() for job in self.children]
                result = all(await asyncio.gather(*runners))
        except Exception as e:
            print(e)
            result = False
        return result

    def __repr__(self) -> str:
        return f"{self.names}, {self.job}"


def print_job_tree(jobs: List[Job], level: int = 0,
                   parent_is_last: bool = True) -> None:
    for i, job in enumerate(jobs):
        is_last_item = i == len(jobs) - 1

        front = ('   ' if parent_is_last else '│  ') * level
        if is_last_item:
            print(f'{front}└──{job.names}')
        else:
            print(f'{front}├──{job.names}')

        if len(job.children) != 0:
            print_job_tree(job.children, level+1, is_last_item)


def build_tree(jobs: Dict[str, Job], complete: List[str]) -> List[Job]:
    root_jobs = []
    for job_name, job in jobs.items():
        if job.on_demand and not any(j.depends_on in job.names for j in jobs.values()):
            continue
        if job.depends_on is None:
            root_jobs.append(job)
        elif job.depends_on in complete:
            root_jobs.append(job)
        else:
            try:
                parent = next(j for j in jobs.values() if job.depends_on in j.names)
            except StopIteration:
                print(f"The dependency '{job.depends_on}' for job '{job_name}' is missing")
            parent.children.append(job)

    return root_jobs
