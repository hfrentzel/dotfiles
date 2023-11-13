import argparse
import asyncio
import os

from . import dir
from . import exe
from . import sym
from . import command
from .job import print_job_tree
from .conf import conf
from .output import red, green

Dir = dir.Dir
Exe = exe.Exe
Sym = sym.Sym
Command = command.Command


def show_desired():
    for t in conf.types:
        print(t.desired_printout(), end='')

def build_tree(jobs, complete):
    root_jobs = []
    for job_name, job in jobs.items():
        if job.depends_on == None:
            root_jobs.append(job)
        elif job.depends_on in complete:
            root_jobs.append(job)
        else:
            parent = next(j for j in jobs.values() if job.depends_on in j.names)
            parent.children.append(job)

    return root_jobs

async def handle_jobs():
    await asyncio.gather(*[t.get_statuses() for t in conf.types])

    if conf.args.stopping_point in [None, 'all_status']:
        for t in conf.types:
            print(t.status_printout(bool(conf.args.stopping_point)), end='')
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

    if conf.args.stopping_point == 'job_generation':
        [print(j.description) for j in jobs.values()]
        return

    root_jobs = build_tree(jobs, complete)
    if conf.args.stopping_point == 'job_tree':
        print_job_tree(root_jobs)
        return

    runners = []
    for job in root_jobs:
        runners.append(job.run())
    results = await asyncio.gather(*runners)
    if all(results):
        print(green('All items setup successfully'))
    else:
        print(red('Not all jobs were successful. Check logs for details'))


def run():
    parser = argparse.ArgumentParser( prog = 'EnvSetup')
    parser.add_argument('--symlinks-only', action='store_true')
    stages = parser.add_mutually_exclusive_group()
    stages.add_argument('--desired', action='store_true')
    stages.add_argument('--show-all', action='store_const', 
                        const='all_status', dest='stopping_point')
    stages.add_argument('--list-jobs', action='store_const', 
                        const='job_generation', dest='stopping_point')
    stages.add_argument('--job-tree', action='store_const', 
                        const='job_tree', dest='stopping_point')
    stages.add_argument('--run', action='store_const', 
                        const='run_jobs', dest='stopping_point')

    conf.dotfiles_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(os.path.expanduser('~/.cache/env_setup'), exist_ok=True)
    conf.sources_dir = os.path.expanduser('~/.cache/env_setup')
    conf.args = parser.parse_args()

    conf.types = [sym]
    if not conf.args.symlinks_only:
        conf.types.extend([dir, exe, command])

    if conf.args.desired:
        show_desired()
        return

    asyncio.run(handle_jobs())
