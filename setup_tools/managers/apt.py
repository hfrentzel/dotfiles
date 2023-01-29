from __future__ import annotations
import asyncio
from setup_tools.installers import async_proc, add_apt_repo
from setup_tools.utils import successful
from setup_tools.config import config
from setup_tools.managers.manager import Manager


class Apt(Manager):
    def __init__(self, package_name: str, repo: str = ''):
        self.name = package_name
        self.repo = repo
        self._requested.add(self)

    @classmethod
    async def _check_for_installed(cls, package_name, repo_name=None):
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

        cls._missing.add(package_name)
        return True

    @classmethod
    async def update(cls):
        tasks = (cls._check_for_installed(p.name, p.repo) for p in cls._requested)
        await asyncio.gather(*tasks)

        if len(cls._missing) == 0:
            print('No apt installs necessary')
            return True

        if config.dry_run:
            print('Not installing apt because dry run')
            return True

        all_packages = ' '.join(cls._missing)

        install = await async_proc(f'sudo apt install --yes {all_packages}')
        if not install['returncode']:
            print('all apt packages successfully installed')
            successful.update(cls._missing)
            cls._missing.difference_update(cls._missing)

        return True
        # TODO handle failure - check which packages got installed
