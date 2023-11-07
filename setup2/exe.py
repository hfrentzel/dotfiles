import asyncio
import re
import shutil
from operator import itemgetter

from .apt import Apt
from .cargo import Cargo
from .pip import Pip
from .npm import Npm
from .job import Job
from .jobs import async_proc
from .output import print_grid, red, green

VERSION_REGEX = re.compile(r'\d+\.\d+\.\d+', re.M)

desired_exes =[]
check_results = []

"""
Installers:
Apt, Deb, Pip, Npm, Tar
#TODO validate elements of installers list are valid
"""
def Exe(name, version=None, installers=None, command_name=None):
    desired_exes.append(
        {
            "name": name,
            "version": version or "ANY",
            "command_name": command_name or name,
            "installers": installers
        })

def ver_greater_than(current, target):
    curr_major, curr_minor, curr_patch = current.split(".")
    tar_major, tar_minor, tar_patch = target.split(".")
    return (
        curr_major > tar_major or
        (curr_major == tar_major and curr_minor > tar_minor) or 
        (curr_major == tar_major and curr_minor == tar_minor and curr_patch >= tar_patch))


async def check_job(exe):
    command = shutil.which(exe['command_name'])
    if command is None:
        return {**exe, 'complete': False, 'curr_ver': red('MISSING')}
    if exe['version'] == 'ANY':
        return {**exe, 'complete': True, 'curr_ver': green('ANY')}

    subcommands = ["--version", "version", "-V", "-v"]
    for cmd in subcommands:
        version = await async_proc(f"{exe['command_name']} {cmd}")
        if version.returncode == 0:
            break

    if version.returncode != 0:
        return {**exe, 'complete': False, 'curr_ver': red('UNKNOWN')}

    if string := VERSION_REGEX.search(version.stdout):
        curr_ver = string.group(0)
        success = ver_greater_than(curr_ver, exe['version'])
        color = green if success else red
        return {**exe, 'complete': success, 'curr_ver': color(curr_ver)}
    return {**exe, 'complete': False, 'curr_ver': red('UNKNOWN')}

def desired_printout():
    lines = []
    for exe in sorted(desired_exes, key=itemgetter('name')):
        lines.append((exe['name'], exe['version']))
    return print_grid(('COMMAND', 'VERSION'), lines)

async def get_statuses():
    tasks = []
    for exe in desired_exes:
        tasks.append(check_job(exe))
    check_results.extend(await asyncio.gather(*tasks))

def status_printout(show_all):
    lines = []
    for exe in sorted(check_results, key=itemgetter('name')):
        if not show_all and exe['complete']:
            continue
        lines.append((exe['name'], exe['version'], exe['curr_ver']))
    return print_grid(('COMMAND', 'DESIRED', 'CURRENT'), lines)

def xxx():
    pass

JOB_BUILDERS = {
    'Apt': Apt.apt_builder,
    'Cargo': Cargo.cargo_builder,
    'Deb': xxx,
    'Pip': Pip.pip_builder,
    'Tar': xxx,
    'Npm': Npm.npm_builder,
}

def create_jobs():
    pass
    """
    Determine which installers are available
        - Apt and Deb require root permissions
        - Pip and Npm require those exes
        - Tar requires gh for github discovery
    """
    no_action_needed = []
    jobs = {}
    for exe in check_results:
        if exe['complete']:
            no_action_needed.append(exe['name'])
            continue
        for t in exe['installers']:
            settled = JOB_BUILDERS[t](exe)
            if isinstance(settled, Job):
                jobs[exe['name']] = settled
            if settled:
                break
    if len(Apt.all_apts) != 0:
        jobs['apt_install'] = Apt.apt_job()
    if len(Pip.all_pips) != 0:
        jobs['pip_install'] = Pip.pip_job()
    if len(Npm.all_packages) != 0:
        jobs['npm_install'] = Npm.npm_job()

    return no_action_needed, jobs
