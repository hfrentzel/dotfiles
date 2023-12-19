import argparse
import asyncio
import os
import itertools
from typing import Dict

from .builder import build_resources
from .managers import create_jobs
from .managers import directory
from .managers import exe
from .managers import sym
from .managers import lib
from .managers import command
from .managers import parser
from .job import print_job_tree, build_tree
from .conf import conf
from .output import red, green
from .managers.manager import Manager

TYPE_MAP: Dict[str, Manager] = {
    'sym': sym,
    'directory': directory,
    'lib': lib,
    'exe': exe,
    'parser': parser,
    'command': command
}


async def handle_jobs() -> None:
    if conf.args.stage == 'desired':
        for t in conf.types:
            print(t.desired_printout(), end='')
        return

    all_complete = await asyncio.gather(*[t.get_statuses() for t in TYPE_MAP.values()])
    complete = list(itertools.chain.from_iterable(all_complete))
    if conf.args.stage in [None, 'show_all']:
        for t in conf.types:
            print(t.status_printout(bool(conf.args.stage)), end='')
        return

    jobs = create_jobs()

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
    resources = argparser.add_mutually_exclusive_group()
    resources.add_argument('-t', '--types', choices=TYPE_MAP.keys(), nargs='+')
    resources.add_argument('-o', '--only')
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
    if conf.args.types is None:
        conf.types.extend(TYPE_MAP.values())
    else:
        for t in conf.args.types:
            conf.types.append(TYPE_MAP[t])

    build_resources()
    asyncio.run(handle_jobs())
