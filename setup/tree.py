import asyncio
from logging import Logger
from typing import Dict, List, Tuple

from .builder import get_resource
from .job import Job
from .managers import create_bonus_jobs


async def check_all_dependencies(
    jobs: Dict[str, Job], complete: List[str]
) -> Tuple[Dict[str, Job], List[str]]:
    all_dependencies = set()
    all_job_resources = set()

    run_dependency_check = True
    while run_dependency_check:
        for job in jobs.values():
            if job.depends_on:
                all_dependencies.update(job.depends_on)
            all_job_resources.update(job.resources)
        missing_dependencies = all_dependencies - set(complete).union(
            all_job_resources
        )
        run_dependency_check = False
        for dep in missing_dependencies:
            resource = get_resource(dep)
            if await resource.get_status():
                complete.append(resource.name)
            else:
                run_dependency_check = True
                if new_job := resource.create_job():
                    jobs[resource.name] = new_job
                else:
                    jobs.update(create_bonus_jobs())
    return jobs, complete


def make_future_job(name: str, fut: asyncio.Future):
    async def inner(_: Logger):
        fut.set_result("done")

    return Job(name=name, description="", job=inner)


def child_wrapper(child_job: Job, futs: List[asyncio.Future]):
    async def inner(_):
        await asyncio.gather(*futs)
        await child_job.run()

    return Job(
        name=child_job.name,
        resources=child_job.resources,
        description=child_job.description,
        job=inner,
        children=child_job.children,
    )


async def build_tree(jobs: Dict[str, Job], complete: List[str]) -> List[Job]:
    jobs, complete = await check_all_dependencies(jobs, complete)

    root_jobs = []
    for job in jobs.values():
        if job.depends_on is None:
            root_jobs.append(job)
        elif set(job.depends_on).issubset(set(complete)):
            root_jobs.append(job)
        else:
            parents = [
                j
                for j in jobs.values()
                if set(job.depends_on).intersection(set(j.resources))
            ]
            if len(parents) == 1:
                parents[0].children.append(job)
                continue
            loop = asyncio.get_event_loop()
            futs = []
            for i, parent in enumerate(parents[1:]):
                fut = loop.create_future()
                name = f"{job.name}__{i}"
                parent.children.append(make_future_job(name, fut))
                futs.append(fut)
            parents[0].children.append(child_wrapper(job, futs))

    return root_jobs
