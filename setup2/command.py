import asyncio
from operator import itemgetter
import os

from .conf import conf
from .job import Job
from .jobs import async_proc
from .output import print_grid, red, green

desired_commands = []
check_results = []


def Command(name, run_script, check_script=None, depends_on=None, cwd=None):
    desired_commands.append(
        {
            "name": name,
            "run_script": run_script,
            "check_script": check_script,
            "cwd": cwd,
            "depends_on": depends_on
        })


async def check_job(command):
    if isinstance(command['cwd'], str):
        command['cwd'] = os.path.expanduser(command['cwd'].replace('DOT', conf.dotfiles_home))

    if command['check_script'] is None:
        return {**command, 'complete': False, 'status': 'CANT VERIFY'}
    result = await async_proc(command['check_script'], cwd=command['cwd'])
    if result.returncode == 0:
        return {**command, 'complete': True, 'status': green('DONE')}

    return {**command, 'complete': False, 'status': red('INCOMPLETE')}


async def get_statuses():
    tasks = []
    for command in desired_commands:
        tasks.append(check_job(command))
    check_results.extend(await asyncio.gather(*tasks))


def desired_printout():
    lines = []
    for command in sorted(desired_commands, key=itemgetter('name')):
        lines.append((command['name'],))
    return print_grid(('SCRIPTS',), lines)


def status_printout(show_all):
    lines = []
    for command in sorted(check_results, key=itemgetter('name')):
        if not show_all and command['complete']:
            continue
        lines.append((command['name'], command['status']))
    return print_grid(('SCRIPT', 'STATUS'), lines)


def create_jobs():
    no_action_needed = []
    jobs = {}
    for command in check_results:
        if command['complete']:
            no_action_needed.append(command['name'])
            continue
        jobs[command['name']] = Job(
            names=[command['name']],
            description=f'Run the {command["name"]} script',
            depends_on=command['depends_on'],
            job=run_script(command['name'], command['run_script'],
                           command['cwd'])
        )

    return no_action_needed, jobs


def run_script(name, script, cwd):
    async def inner():
        print(f'Running the {name} script...')
        result = await async_proc(script, cwd=cwd)
        success = not result.returncode
        if success:
            print(green(f'{name} script ran successfully'))
        else:
            print(red(f'{name} script failed'))
        return success

    return inner
