import argparse
import asyncio
import os
import itertools
from typing import List

from .builder import build_resources
from .managers import create_jobs, all_desired
from .managers import exe
from .job import print_job_tree, build_tree
from .conf import conf
from .output import red, green
from .managers import Manager, Spec, ALL_MANAGERS


async def handle_jobs(selected_types: List[Manager]) -> None:
    if conf.args.stage == 'desired':
        for t in selected_types:
            print(t.desired_printout(), end='')
        return

    all_complete = await asyncio.gather(*[t.get_statuses() for t in ALL_MANAGERS.values()])
    complete = list(itertools.chain.from_iterable(all_complete))
    if conf.args.stage in [None, 'show_all']:
        for t in selected_types:
            print(t.status_printout(bool(conf.args.stage)), end='')
        return

    jobs = create_jobs(selected_types)
    if len(jobs) == 0:
        print('All items are satisfied')
        return

    if conf.args.stage == 'jobs':
        for m in jobs.values():
            print(m.description)
        return

    root_jobs = build_tree(jobs, complete)
    if conf.args.stage == 'tree':
        print_job_tree(root_jobs)
        return

    if all(await asyncio.gather(*[job.run() for job in root_jobs])):
        print(green('All items setup successfully'))
    else:
        print(red('Not all jobs were successful. Check logs for details'))


async def handle_single_resource(resource: Spec, resource_type: str) -> None:
    if resource.name in await ALL_MANAGERS[resource_type].get_statuses():
        print(f'{resource.name} is already set up')
        return

    job = ALL_MANAGERS[resource_type].create_job(resource) or \
        list(exe.create_bonus_jobs().values())[0]

    if job.depends_on is not None:
        if not any(d.name == job.depends_on for d in all_desired()):
            build_resources(job.depends_on)
        all_complete = await asyncio.gather(*[t.get_statuses() for t in ALL_MANAGERS.values()])
        complete = list(itertools.chain.from_iterable(all_complete))

        if remaining := {job.depends_on} - set(complete):
            print(f'Can\'t set up {resource.name} because it has '
                  f'unsatisfied dependencies: {remaining}')
            return

    if conf.args.stage != 'run':
        print(f'{resource.name} can be set up. Rerun with -r to run the job')
        return

    if await job.run():
        print(green(f'{resource.name} set up successfully'))
    else:
        print(red(f'Failed to set up {resource.name}'))


def run() -> None:
    argparser = argparse.ArgumentParser(prog='EnvSetup')
    resources = argparser.add_mutually_exclusive_group()
    resources.add_argument('-t', '--types', choices=ALL_MANAGERS.keys(), nargs='+')
    resources.add_argument('-o', '--only')
    resources.add_argument('--force')
    stages = argparser.add_mutually_exclusive_group()
    stages.add_argument('-s', '--stage', choices=['desired', 'show_all',
                        'jobs', 'tree', 'run'], default=None)
    stages.add_argument('-d', '--desired', action='store_const',
                        const='desired', dest='stage')
    stages.add_argument('-r', '--run', action='store_const',
                        const='run', dest='stage')

    os.environ['NPM_CONFIG_USERCONFIG'] = os.path.expanduser('~/.config/npm/npmrc')

    conf.dotfiles_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf.args = argparser.parse_args()

    resource = build_resources(conf.args.only)
    if resource:
        asyncio.run(handle_single_resource(*resource))
        return

    selected_types = []
    if conf.args.types is None:
        selected_types = list(ALL_MANAGERS.values())
    else:
        for t in conf.args.types:
            selected_types.append(ALL_MANAGERS[t])
    asyncio.run(handle_jobs(selected_types))
