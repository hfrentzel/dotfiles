import asyncio
import re
import shutil
from operator import itemgetter

from .jobs import async_proc

VERSION_REGEX = re.compile(r'\d+\.\d+\.\d+', re.M)

exes =[]
def Exe(command_name, version=None):
    exes.append(
        {
            "name": command_name,
            "version": version or "ANY",
            "command_name": command_name
        })

def ver_greater_than(current, target):
    curr_major, curr_minor, curr_patch = current.split(".")
    tar_major, tar_minor, tar_patch = target.split(".")
    return (
        curr_major > tar_major or
        (curr_major == tar_major and curr_minor > tar_minor) or 
        (curr_major == tar_major and curr_minor == tar_minor and curr_patch >= tar_patch))


async def exe_check_job(exe):
    command = shutil.which(exe['command_name'])
    if command is None:
        return {
            **exe,
            'complete': False,
            'curr_ver': 'MISSING'
        }
    if exe['version'] == 'ANY':
        return {
            **exe,
            'complete': True,
            'curr_ver': 'ANY'
    }

    subcommands = ["--version", "version", "-V", "-v"]
    for cmd in subcommands:
        version = await async_proc(f"{exe['command_name']} {cmd}")
        if version.returncode == 0:
            break

    if version.returncode != 0:
        return {
            **exe,
            'complete': False,
            'curr_ver': 'UNKNOWN'
        }

    if string := VERSION_REGEX.search(version.stdout):
        curr_ver = string.group(0)
        return {
            **exe,
            'complete': ver_greater_than(curr_ver, exe['version']),
            'curr_ver': curr_ver
        }
    
    else:
        return {
            **exe,
            'complete': False,
            'curr_ver': 'UNKNOWN'
        }

def exe_desired_printout():
    out = ""
    out += '\nCOMMAND       VERSION\n'
    for exe in sorted(exes, key=itemgetter('name')):
        out += f"{exe['name']: <13} {exe['version']}\n"

    return out

async def exe_status_printout(show_all):
    results = []
    tasks = []
    for exe in exes:
        tasks.append(exe_check_job(exe))
    results = await asyncio.gather(*tasks)

    out = ""
    for exe in sorted(results, key=itemgetter('name')):
        if not show_all and exe['complete']:
            continue
        out += f"{exe['name']: <13} {exe['version']: <13} {exe['curr_ver']}\n"

    if out != "":
        return '\nCOMMAND       DESIRED       CURRENT\n' + out
    else:
        return ''
