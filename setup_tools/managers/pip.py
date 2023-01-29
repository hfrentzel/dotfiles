from __future__ import annotations
import asyncio
import json
from setup_tools.utils import successful
from setup_tools.installers import async_proc
from setup_tools.config import config
from setup_tools.managers.manager import Manager


class Pip(Manager):
    def __init__(self, package_name: str, version: str):
        self.name = package_name
        self.version = version
        self._requested.add(self)

    def __str__(self):
        return f'{self.name}=={self.version}'

    @classmethod
    async def _check_for_installed(cls, package: Pip, pack_list):
        if package.name not in pack_list:
            cls._missing.add(package)
            return
        if pack_list[package.name] != package.version:
            print(f'{package.name} is not at correct version. Expected {package.version}. '
                  f'Installed: {pack_list[package.name]}')
            cls._missing.add(package)
            return

        if config.verbose:
            print(f'{package.name} is installed and up to date ({package.version})')
        successful.add(package.name)
        return

    @classmethod
    async def update(cls):
        freeze_list = await async_proc('/usr/bin/python -m pip list --format=json')
        freeze_packs = {p['name']: p['version'] for p in
                        json.loads(freeze_list['stdout'])}
        tasks = (cls._check_for_installed(p, freeze_packs)
                 for p in cls._requested)
        await asyncio.gather(*tasks)

        if len(cls._missing) == 0:
            print('All pip packages up to date')
            return True

        if config.dry_run:
            print('Not installing anything because dry run')
            return True

        print(f'Installing python packages {cls._missing}')
        all_packages = ' '.join(str(p) for p in cls._missing)
        await async_proc(f'/usr/bin/python -m pip install {all_packages}')

        return True

    @classmethod
    async def check(cls):
        outdated_list, uptodate_list = await asyncio.gather(
            async_proc('/usr/bin/python -m pip list -o --format=json'),
            async_proc('/usr/bin/python -m pip list -u --format=json'))

        outdated = {p['name']: {'curr': p['version'], 'avail': p['latest_version']}
                    for p in json.loads(outdated_list['stdout'])}
        uptodate = {p['name']: p['version'] for p in
                    json.loads(uptodate_list['stdout'])}
        name_length = max(len(p.name) for p in cls._requested)
        print(f'{"name": <{name_length}} Current  Available')

        for pack in cls._requested:
            if pack.name in outdated:
                print(f'{pack.name: <{name_length}} {outdated[pack.name]["curr"]: <8} '
                      f'{outdated[pack.name]["avail"]}')
            elif pack.name in uptodate:
                print(f'{pack.name: <{name_length}} {uptodate[pack.name]: <8} '
                      f'Up To Date')
