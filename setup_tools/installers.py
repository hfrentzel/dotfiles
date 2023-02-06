import asyncio
import shutil
from typing import Union, Optional
from os import path
from setup_tools.jobs import add_dependent_job, add_job
from setup_tools.config import config


def vprint(msg: str):
    if config.verbose:
        print(msg)


def command(cmd, depends_on=None, run_on_dry=False):
    if config.dry_run and not run_on_dry:
        return
    if depends_on is not None:
        add_dependent_job(async_proc(cmd), depends_on)
    else:
        add_job(async_proc(cmd))


async def async_proc(cmd, stdin=None, cwd=None):
    process = await asyncio.create_subprocess_shell(
        cmd,
        cwd=cwd,
        stdin=asyncio.subprocess.PIPE if stdin else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate(stdin)
    return {
        'stdout': stdout.decode().strip('\n'),
        'stderr': stderr.decode().strip('\n'),
        'returncode': process.returncode
    }


async def add_apt_repo(repo_name):
    repo_list = await async_proc('apt-cache policy')
    grep = await async_proc(f'grep {repo_name.split(":")[-1]}', repo_list['stdout'])

    if not grep['returncode']:
        print(f'{repo_name} is already in the apt cache')
        return

    print(f'Adding {repo_name}')
    await async_proc(f'sudo add-apt-repository --yes {repo_name}')
    print(f'{repo_name} successfully added')

    print('Running apt update')
    await async_proc('sudo apt update')


async def check_version(cmd, desired_version, check_cmd=None) -> \
        Optional[Union[bool, str]]:
    if check_cmd is None:
        check_cmd = f"{cmd} --version | head -1 | grep -o '[0-9\\.]\\+' | head -1"
    if not shutil.which(cmd):
        print(f'{cmd} is not installed')
        return None

    curr_ver = (await async_proc(check_cmd))['stdout']
    if curr_ver != desired_version:
        print(f'{cmd} ({curr_ver}) is not up to date. '
              f'Can be updated to {desired_version}')
        return curr_ver

    vprint(f'{cmd} is installed and up to date ({curr_ver})')
    return True


async def fetch_file(version, url):
    full_url = url.format(version=version)
    _, file = path.split(full_url)

    filename = f'{config.sources_home}/{file}'

    await async_proc(f'curl -L {full_url} -o {filename}')

    return filename
