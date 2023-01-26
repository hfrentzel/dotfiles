import asyncio
from setup_tools.installers import async_proc, add_apt_repo
from setup_tools.utils import ready_to_run, successful
from setup_tools.config import config

apt_status = {
    'requested': set(),
    'repos': set(),
    'missing': set(),
    'queued': False
}


def linux_package(package_name, repo_name=None, depends_on=None):
    apt_status['requested'].add((package_name, repo_name))
    if not apt_status['queued']:
        ready_to_run.append(install_apt())
        apt_status['queued'] = True


async def _check_for_installed(package_name, repo_name=None):
    package_exists = await async_proc(f'dpkg -s {package_name}')
    if not package_exists['returncode']:
        if config.verbose:
            print(f'{package_name} is already installed')
        successful.add(package_name)
        return True

    if repo_name:
        # TODO Change to new function that stores apt repos then
        # installs all at once
        add_apt_repo(repo_name)

    apt_status['missing'].add(package_name)
    return True


async def install_apt():
    apt_status['queued'] = False

    tasks = (_check_for_installed(p[0], p[1]) for p in apt_status['requested'])
    await asyncio.gather(*tasks)

    if len(apt_status['missing']) == 0:
        print('No apt installs necessary')
        return True

    if config.dry_run:
        print('Not installing apt because dry run')
        return True

    all_packages = ' '.join(apt_status['missing'])

    install = await async_proc(f'sudo apt install --yes {all_packages}')
    if not install['returncode']:
        print('all apt packages successfully installed')
        successful.update(apt_status['missing'])
        apt_status['missing'].difference_update(apt_status['missing'])

    return True
    # TODO handle failure - check which packages got installed
