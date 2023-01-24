from dataclasses import dataclass
import asyncio
from typing import Awaitable, Set, List
from setup_tools.config import config


@dataclass(frozen=True)
class DependentJob:
    item: Awaitable
    depends_on: str


def add_dependent_job(job, depends_on, run_on_dry=False):
    if config['dry_run'] and not run_on_dry:
        return
    depends_on_others.add(DependentJob(item=job, depends_on=depends_on))


def add_job(job, run_on_dry=False):
    if config['dry_run'] and not run_on_dry:
        return
    ready_to_run.append(job)


depends_on_others: Set[DependentJob] = set()
ready_to_run: List[Awaitable] = []
successful: Set[str] = set()


async def run_tasks():
    while len(depends_on_others) != 0 or len(ready_to_run) != 0:
        no_longer_dependent = set()
        for item in depends_on_others:
            if item.depends_on in successful:
                ready_to_run.append(item.item)
                no_longer_dependent.add(item)
        depends_on_others.difference_update(no_longer_dependent)
        if len(ready_to_run) != 0:
            results = await asyncio.gather(*ready_to_run)
            for i, result in reversed(list(enumerate(results))):
                if result:
                    ready_to_run.pop(i)
