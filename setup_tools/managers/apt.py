from __future__ import annotations
import asyncio
from setup_tools.installers import async_proc, add_apt_repo, vprint
from setup_tools.jobs import successful
from setup_tools.config import config
from setup_tools.managers.manager import Manager


class Apt(Manager):
    def __init__(self, package_name: str, repo: str = ''):
        self.name = package_name
        self.version = None
        self.repo = repo
        self._requested.add(self)

    @classmethod
    async def _check_for_installed(cls, package):
        package_exists = await async_proc(f'dpkg -s {package.name}')
        if not package_exists['returncode']:
            vprint(f'{package.name} is already installed')
            successful.add(package.name)
            return True

        if package.repo:
            # TODO Change to new function that stores apt repos then
            # installs all at once
            await add_apt_repo(package.repo)

        cls._missing.add((package, None))
        return True

    @classmethod
    async def update(cls):
        tasks = (cls._check_for_installed(p) for p in cls._requested)
        await asyncio.gather(*tasks)

        if len(cls._missing) == 0:
            return True

        if config.dry_run:
            print('Not installing apt because dry run')
            return True

        pack_names = [p[0].name for p in cls._missing]
        all_packages = ' '.join(pack_names)

        print('Running apt update')
        await async_proc('sudo apt update')
        print(f'Installing Apt packages {all_packages}')
        install = await async_proc(f'sudo apt install --yes {all_packages}')
        if not install['returncode']:
            print('all apt packages successfully installed')
            successful.update(pack_names)
            cls._missing.difference_update(cls._missing)
        else:
            print('Apt install failed')
            print(install['stderr'])

        return True
        # TODO handle failure - check which packages got installed
