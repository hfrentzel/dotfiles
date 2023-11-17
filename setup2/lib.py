import asyncio
from operator import itemgetter

from .pip import Pip
from .npm import Npm
from .output import print_grid, red

desired_libs = []
check_results = []


def Lib(name, version, l_type):
    desired_libs.append(
        {
            "name": name,
            "version": version,
            "type": l_type
        })


async def check_job(lib):
    if lib['type'] == 'pip':
        return Pip.check_install(lib)
    if lib['type'] == 'npm':
        return Npm.check_install(lib)

    return {**lib, 'complete': False, 'curr_ver': red('UNKNOWN')}


def desired_printout():
    lines = []
    for lib in sorted(desired_libs, key=itemgetter('name')):
        lines.append((lib['name'], lib['version']))
    return print_grid(('LIBRARY', 'VERSION'), lines)


async def get_statuses():
    tasks = []
    for lib in desired_libs:
        tasks.append(check_job(lib))
    check_results.extend(await asyncio.gather(*tasks))


def status_printout(show_all):
    lines = []
    for lib in sorted(check_results, key=itemgetter('name')):
        if not show_all and lib['complete']:
            continue
        lines.append((lib['name'], lib['version'], lib['curr_ver']))
    return print_grid(('LIBRARY', 'DESIRED', 'CURRENT'), lines)


JOB_BUILDERS = {
    'pip': Pip.pip_builder,
    'npm': Npm.npm_builder
}


def create_jobs():
    no_action_needed = []
    jobs = {}
    for lib in check_results:
        if lib['complete']:
            no_action_needed.append(lib['name'])
            continue
        JOB_BUILDERS[lib['type']](lib)
    if len(Pip.all_pips) != 0:
        jobs['pip_install'] = Pip.pip_job()
    if len(Npm.all_packages) != 0:
        jobs['npm_install'] = Npm.npm_job()

    return no_action_needed, jobs
