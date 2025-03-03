import asyncio
from typing import Dict, List, Optional

from .builder import get_resource
from .job import Job
from .managers import create_bonus_jobs


async def build_tree(jobs: Dict[str, Job], complete: List[str]) -> List[Job]:
    async def inner() -> Optional[List[Job]]:
        root_jobs = []
        for job in jobs.values():
            job.children = []
        for job in jobs.values():
            if job.depends_on is None:
                root_jobs.append(job)
            elif job.depends_on in complete:
                root_jobs.append(job)
            else:
                try:
                    parent = next(
                        j
                        for j in jobs.values()
                        if job.depends_on in j.resources
                    )
                    parent.children.append(job)
                except StopIteration:
                    resource = get_resource(job.depends_on)
                    if await resource.get_status():
                        root_jobs.append(job)
                        complete.append(resource.name)
                    else:
                        new_job = resource.create_job()
                        if new_job:
                            jobs[resource.name] = new_job
                            return None
                        jobs.update(create_bonus_jobs())
                        return None
        return root_jobs

    root_jobs = None
    while root_jobs is None:
        root_jobs = await inner()

    return root_jobs
