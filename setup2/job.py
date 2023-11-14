import asyncio
from dataclasses import dataclass, field
from typing import List

@dataclass
class Job:
    names: List[str]
    job: callable
    description: str
    depends_on: str = None
    children: List['Job'] = field(default_factory=list)

    async def run(self):
        try:
            result = await self.job()
            if result and len(self.children) != 0:
                runners = [job.run() for job in self.children]
                result = all(await asyncio.gather(*runners))
        except Exception as e:
            print(e)
            result = False
        return result

    def __repr__(self):
        return f"{self.names}, {self.job}"

def print_job_tree(jobs: List[Job], level=0, layers=True):
    for i, job in enumerate(jobs):
        front = ('│  ' if layers else '   ') * level
        if i != len(jobs) - 1:
            print(f'{front}├──{job.names}')
        else:
            print(f'{front}└──{job.names}')

        if len(job.children) != 0:
            print_job_tree(job.children, level+1, i != len(jobs) - 1)

