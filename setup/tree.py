import asyncio
from dataclasses import dataclass, field

from .builder import get_resource
from .job import Job
from .managers import create_bonus_jobs
from .managers.manager import Manager


async def create_jobs(
    resources: list[Manager], complete: set[str]
) -> list[Job]:
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


@dataclass
class TreeNode:
    name: str
    resources: list[str] = field(default_factory=list)
    children: list["TreeNode"] = field(default_factory=list)


async def build_tree(jobs: list[Job]) -> tuple[list[Job], list[TreeNode]]:
    tree_d = {j.name: TreeNode(j.name, j.resources, []) for j in jobs}
    tree = []
    for job in jobs:
        if parents := [
            j for j in jobs if set(job.depends_on) & set(j.resources)
        ]:
            loop = asyncio.get_event_loop()
            for i, p in enumerate(parents):
                fut = loop.create_future()
                p.children.append(fut)
                job.parents.append(fut)
                if i == 0:
                    tree_d[p.name].children.append(tree_d[job.name])
                else:
                    tree_d[p.name].children.append(TreeNode(f"{job.name}__{i}"))
        else:
            tree.append(tree_d[job.name])

    return jobs, tree


def print_job_tree(
    jobs: list[TreeNode], level: int = 0, parent_is_last: bool = True
) -> None:
    for i, job in enumerate(jobs):
        is_last_item = i == len(jobs) - 1

        front = ("   " if parent_is_last else "│  ") * level
        if len(job.resources) == 0 or (
            len(job.resources) == 1 and job.resources[0] == job.name
        ):
            output = job.name
        else:
            output = f"{job.name}({','.join(job.resources)})"
        if is_last_item:
            print(f"{front}└──{output}")
        else:
            print(f"{front}├──{output}")

        if len(job.children) != 0:
            print_job_tree(job.children, level + 1, is_last_item)
