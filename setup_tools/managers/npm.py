from __future__ import annotations
import asyncio
import json
from setup_tools.config import config
from setup_tools.installers import async_proc, vprint
from setup_tools.jobs import successful
from setup_tools.managers.manager import Manager


class Npm(Manager):
    def __init__(self, package_name: str, version: str):
        if not config.check:
            self.name = package_name
            self.version = version
            self._requested.add(self)

    def __str__(self):
        return f'{self.name}@{self.version}'

    @classmethod
    async def _check_for_installed(cls, package: Npm, pack_list):
        if package.name not in pack_list:
            cls._missing.add((package, None))
            return
        if pack_list[package.name] != package.version:
            cls._missing.add((package, pack_list[package.name]))
            return

        vprint(f'{package.name} is installed and up to date ({package.version})')
        successful.add(package.name)
        return

    @classmethod
    async def update(cls):
        install_list = await async_proc('npm --location=global -j list')
        better = json.loads(install_list['stdout'])['dependencies']
        packages = {p[0]: p[1]['version'] for p in better.items()}

        tasks = (cls._check_for_installed(p, packages)
                 for p in cls._requested)
        await asyncio.gather(*tasks)

        if len(cls._missing) == 0:
            return True

        if config.dry_run:
            print('Not installing any node packages because dry run')
            return True

        print(f'Installing npm packages {cls._missing}')
        all_packages = ' '.join(str(p[0]) for p in cls._missing)
        await async_proc(f'npm install -g {all_packages}')

        return True
