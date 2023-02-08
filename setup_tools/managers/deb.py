import asyncio
from typing import Optional

from setup_tools.config import config
from setup_tools.installers import async_proc, check_version, \
    fetch_file
from setup_tools.managers.manager import Manager


class Deb(Manager):
    def __init__(self, command: str, url: str, version: str,
                 version_check: Optional[str] = None):
        self.name = command
        self.url = url
        self.version_check = version_check
        self.version = version
        self._requested.add(self)

    async def check_for_installed(self):
        version = await check_version(self.name, self.version,
                                      self.version_check)
        if version is None or isinstance(version, str):
            self._missing.add((self, version))

    async def install(self):

        print(f'Installing {self.name}...')
        filename = await fetch_file(self.version, self.url)
        await async_proc(f'sudo apt install {filename}')

        return True

    @classmethod
    async def update(cls):
        tasks = (pack.check_for_installed() for pack in cls._requested)
        await asyncio.gather(*tasks)

        if len(cls._missing) == 0:
            return True
        if config.dry_run:
            print('Not installing Debian because dry run')
            return True

        install_tasks = (pack[0].install() for pack in cls._missing)
        await asyncio.gather(*install_tasks)

        return True