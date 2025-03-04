import asyncio
from typing import List, Set

from .builder import get_resource
from .job import Job
from .managers import create_bonus_jobs
from .managers.manager import Manager


async def create_jobs(
    resources: List[Manager], complete: Set[str]
) -> List[Job]:
    jobs = {}
    all_dependencies = set()
    all_job_resources = set()
    for r in resources:
        if r.state[0]:
            continue

        job = r.create_job()
        if job is None:
            continue
        jobs[r.name] = job
        all_dependencies.update(job.depends_on)
        all_job_resources.update(job.resources)

    bonus_jobs = create_bonus_jobs()
    for bonus_job in bonus_jobs.values():
        all_dependencies.update(bonus_job.depends_on)
        all_job_resources.update(bonus_job.resources)
    jobs.update(bonus_jobs)

    while missing_dependencies := (
        all_dependencies - complete.union(all_job_resources)
    ):
        for dep in missing_dependencies:
            r = get_resource(dep)
            if await r.get_status():
                complete.add(r.name)
            elif new_job := r.create_job():
                jobs[r.name] = new_job
                all_dependencies.update(new_job.depends_on)
                all_job_resources.update(new_job.resources)
            else:
                bonus_jobs = create_bonus_jobs()
                for bonus_job in bonus_jobs.values():
                    all_dependencies.update(bonus_job.depends_on)
                    all_job_resources.update(bonus_job.resources)
                jobs.update(bonus_jobs)

    return list(jobs.values())


async def build_tree(jobs: List[Job]) -> List[Job]:
    for job in jobs:
        if parents := [
            j
            for j in jobs
            if set(job.depends_on).intersection(set(j.resources))
        ]:
            loop = asyncio.get_event_loop()
            for p in parents:
                fut = loop.create_future()
                p.children.append(fut)
                job.parents.append(fut)
    return jobs


def print_job_tree(jobs: List[Job]) -> None:
    for j in jobs:
        print(
            f"{j.name}: Parents: {len(j.parents)} Children: {len(j.children)}"
        )
