import asyncio
from setup_tools.installers import async_proc, add_apt_repo
from setup_tools.utils import ready_to_run, successful

_requested_packages = set()
_apt_repos = set()
_apt_packages = set()
_apt_queued = False


def linux_package(package_name, repo_name=None, depends_on=None):
    global _apt_queued
    _requested_packages.add((package_name, repo_name))
    if not _apt_queued:
        ready_to_run.append(install_apt())
        _apt_queued = True


async def _check_for_installed(package_name, repo_name=None):
    package_exists = await async_proc(f'dpkg -s {package_name}')
    if not package_exists['returncode']:
        print(f'{package_name} is already installed')
        successful.add(package_name)
        return True

    if repo_name:
        # TODO Change to new function that stores apt repos then
        # installs all at once
        add_apt_repo(repo_name)

    _apt_packages.add(package_name)
    return True


async def install_apt():
    global _apt_queued
    _apt_queued = False

    tasks = (_check_for_installed(p[0], p[1]) for p in _requested_packages)
    await asyncio.gather(*tasks)

    if len(_apt_packages) == 0:
        print("No installs necessary")
        return True

    all_packages = ' '.join(_apt_packages)

    install = await async_proc(f'sudo apt install --yes {all_packages}')
    if not install['returncode']:
        print('all apt packages successfully installed')
        successful.update(_apt_packages)
        _apt_packages.difference_update(_apt_packages)

    return True
    # TODO handle failure - check which packages got installed
