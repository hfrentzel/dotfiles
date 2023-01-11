import asyncio
from setup_tools.utils import add_dependent_job, ready_to_run, successful


def command(cmd, depends_on=None):
    if depends_on is not None:
        add_dependent_job(async_proc(cmd), depends_on)
    else:
        ready_to_run.append(async_proc(cmd))


async def async_proc(cmd, stdin=None):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdin=asyncio.subprocess.PIPE if stdin else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate(stdin)
    return {
        'stdout': stdout,
        'stderr': stderr,
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


_requested_packages = set()
_pip_packages = set()
_pip_queued = False


def pip_package(package_name, depends_on=None):
    global _pip_queued
    _requested_packages.add(package_name)
    if not _pip_queued:
        ready_to_run.append(install_pip_packages())
        _pip_queued = True


async def _check_for_installed(package_name, pack_list):
    grep = await async_proc(f'grep {package_name}', pack_list)
    if not grep['returncode']:
        print(f'{package_name} is already installed to python')
        successful.add(package_name)
        return

    _pip_packages.add(package_name)


async def install_pip_packages():
    global _pip_queued
    _pip_queued = False

    freeze_list = await async_proc('/usr/bin/python -m pip freeze')
    tasks = (_check_for_installed(p, freeze_list['stdout'])
             for p in _requested_packages)
    await asyncio.gather(*tasks)

    if len(_pip_packages) == 0:
        print('No pip packages to install')
        return True

    print(f'Installing python packages {_pip_packages}')
    all_packages = ' '.join(_pip_packages)
    await async_proc(f'/usr/bin/python -m pip install {all_packages}')

    return True
