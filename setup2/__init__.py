import argparse
import asyncio
import os

from . import exe
from . import sym
from .conf import conf

Exe = exe.Exe
Sym = sym.Sym


def show_desired():
    for t in conf.types:
        print(t.desired_printout(), end="")

async def get_current_status(show_all):
    sym.get_statuses()
    await exe.get_statuses()

    if not conf.args.run:
        for t in conf.types:
            print(t.status_printout(show_all), end="")
        return

    complete, jobs = sym.create_jobs()
    print(complete)
    print(jobs)
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
    parser.add_argument('--show-desired', action='store_true')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--symlinks-only', action='store_true')

    conf.args = parser.parse_args()
    conf.dotfiles_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    conf.types = [sym]
    if not conf.args.symlinks_only:
        conf.types.append(exe)

    if conf.args.show_desired:
        show_desired()
        return

    asyncio.run(get_current_status(conf.args.show_all))
