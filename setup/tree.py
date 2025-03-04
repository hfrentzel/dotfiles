import asyncio
from logging import Logger
from typing import Dict, List, Tuple

from .builder import get_resource
from .job import Job
from .managers import create_bonus_jobs
from .managers.manager import Manager


async def create_jobs(
    resources: List[Manager], complete: List[str]
) -> Tuple[Dict[str, Job], List[str]]:
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
        all_dependencies - set(complete).union(all_job_resources)
    ):
        for dep in missing_dependencies:
            r = get_resource(dep)
            if await r.get_status():
                complete.append(r.name)
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

    return jobs, complete


def make_future_job(name: str, fut: asyncio.Future):
    async def inner(_: Logger):
        fut.set_result("done")
        return True

    return Job(name=name, description="", job=inner)


def child_wrapper(child_job: Job, futs: List[asyncio.Future]):
    async def inner(_):
        await asyncio.gather(*futs)
        return await child_job.run()

    return Job(
        name=child_job.name,
        resources=child_job.resources,
        description=child_job.description,
        job=inner,
        children=child_job.children,
    )


async def build_tree(
    jobs: Dict[str, Job], complete: List[str]
) -> Tuple[List[Job], bool]:
    need_root_access = False

    root_jobs = []
    job_list = list(jobs.values())
    for i in range(len(job_list)):
        job = job_list[i]
        if job.needs_root_access:
            need_root_access = True
        if len(job.depends_on) == 0:
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
            for j, parent in enumerate(parents[1:]):
                fut = loop.create_future()
                name = f"{job.name}__{j}"
                parent.children.append(make_future_job(name, fut))
                futs.append(fut)
            wrapper_job = child_wrapper(job, futs)
            parents[0].children.append(wrapper_job)
            job.children = []
            job_list[i] = wrapper_job

    return root_jobs, need_root_access
