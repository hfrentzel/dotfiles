import asyncio
from setup_tools.installers import async_proc, add_apt_repo

_requested_packages = set()
_apt_repos = set()
_apt_packages = set()
_successes = set()


def linux_package(package_name, repo_name=None):
    _requested_packages.add((package_name, repo_name))


async def install_package(package_name, repo_name=None):
    package_exists = await async_proc(f'dpkg -s {package_name}')
    if not package_exists['returncode']:
        print(f'{package_name} is already installed')
        _successes.add(package_name)
        return

    if repo_name:
        # TODO Change to new function that stores apt repos then
        # installs all at once
        add_apt_repo(repo_name)

    _apt_packages.add(package_name)


async def install_all_packages():
    # Sequential equivalent
    # for p in _requested_packages:
    #     await install_package(p[0], p[1])
    tasks = (install_package(p[0], p[1]) for p in _requested_packages)
    await asyncio.gather(*tasks)


async def install_apt():
    all_packages = ' '.join(_apt_packages)

    install = await async_proc(f'sudo apt install --yes {all_packages}')
    if not install['returncode']:
        print('all apt packages successfully installed')
        _successes.update(_apt_packages)
        return

    # TODO handle failure - check which packages got installed
