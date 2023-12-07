import argparse
import asyncio
import os
from typing import List, Dict

from .builder import build_resources
from .managers import directory
from .managers import exe
from .managers import sym
from .managers import lib
from .managers import command
from .managers import parser
from .job import print_job_tree, Job
from .conf import conf
from .output import red, green

TYPE_MAP = {
    'sym': sym,
    'directory': directory,
    'lib': lib,
    'exe': exe,
    'parser': parser,
    'command': command
}


def show_desired() -> None:
    for t in conf.types:
        print(t.desired_printout(), end='')


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
            parent = next(j for j in jobs.values() if job.depends_on in j.names)
            parent.children.append(job)

    return root_jobs


async def handle_jobs() -> None:
    await asyncio.gather(*[t.get_statuses() for t in conf.types])

    if conf.args.stage in [None, 'show_all']:
        for t in conf.types:
            print(t.status_printout(bool(conf.args.stage)), end='')
        return

    complete = []
    jobs = {}
    for t in conf.types:
        c, j = t.create_jobs()
        complete.extend(c)
        jobs.update(j)

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


def run() -> None:
    argparser = argparse.ArgumentParser(prog='EnvSetup')
    argparser.add_argument('-t', '--types', choices=TYPE_MAP.keys(), nargs='+')
    stages = argparser.add_mutually_exclusive_group()
    stages.add_argument('-s', '--stage', choices=['desired', 'show_all',
                        'jobs', 'tree', 'run'], default=None)
    stages.add_argument('-d', '--desired', action='store_const',
                        const='desired', dest='stage')
    stages.add_argument('-r', '--run', action='store_const',
                        const='run', dest='stage')

    os.environ['NPM_CONFIG_USERCONFIG'] = os.path.expanduser('~/.config/npm/npmrc')
    os.makedirs(os.path.expanduser('~/.cache/env_setup'), exist_ok=True)
    conf.sources_dir = os.path.expanduser('~/.cache/env_setup')

    conf.dotfiles_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf.args = argparser.parse_args()
    if conf.args.types is None:
        conf.types.extend(TYPE_MAP.values())
    else:
        for t in conf.args.types:
            conf.types.append(TYPE_MAP[t])

    build_resources()
    if conf.args.stage == 'desired':
        show_desired()
        return

    asyncio.run(handle_jobs())
