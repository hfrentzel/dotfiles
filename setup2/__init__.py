import argparse
import asyncio
import os

from . import dir
from . import exe
from . import sym
from .conf import conf

Dir = dir.Dir
Exe = exe.Exe
Sym = sym.Sym


def show_desired():
    for t in conf.types:
        print(t.desired_printout(), end='')

async def get_current_status():
    await asyncio.gather(*[t.get_statuses() for t in conf.types])

    if not conf.args.run and not conf.args.list_jobs:
        for t in conf.types:
            print(t.status_printout(conf.args.show_all), end='')
        return

    complete, jobs = sym.create_jobs()
    comp2, job2 = dir.create_jobs()
    complete.extend(comp2)
    jobs = {**jobs, **job2}

    if conf.args.list_jobs:
        [print(j.description) for j in jobs.values()]
        return

    if len(jobs) == 0:
        return

    runners = []
    for job in jobs.values():
        runners.append(job.run())
    results = await asyncio.gather(*runners)
    print(results)


def run():
    parser = argparse.ArgumentParser( prog = 'EnvSetup')
    parser.add_argument('--show-all', action='store_true')
    parser.add_argument('--desired', action='store_true')
    parser.add_argument('--list-jobs', action='store_true')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--symlinks-only', action='store_true')

    conf.args = parser.parse_args()
    conf.dotfiles_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    conf.types = [sym]
    if not conf.args.symlinks_only:
        conf.types.extend([dir, exe])

    if conf.args.desired:
        show_desired()
        return

    asyncio.run(get_current_status())
