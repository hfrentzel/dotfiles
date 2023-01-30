import asyncio
import shutil

from setup_tools.config import config
from setup_tools.installers import async_proc
from setup_tools.managers.manager import Manager


class Tar(Manager):
    def __init__(self, command: str, url: str, version_check: str,
                 version: str):
        self.command = command
        self.url = url
        self.version_check = version_check
        self.version = version
        self._requested.add(self)

    async def check_for_installed(self):
        if not shutil.which(self.command):
            print(f'{self.command} is not installed')
            self._missing.add(self)
        elif (curr_ver := (await async_proc(self.version_check))['stdout']) \
                != self.version:
            print(f'{self.command} ({curr_ver}) is not up to date. '
                  f'Can be updated to {self.version}')
            self._missing.add(self)
        elif config.verbose:
            print(f'{self.command} is installed and up to '
                  f'date ({self.version})')

    async def install(self):

        full_url = self.url.format(version=self.version)
        filename = f'{config.sources_home}/{self.command}-{self.version}.tar.xz'

        await async_proc(f'curl -L {full_url} -o {filename}')
        await async_proc('sudo tar -C /usr/local --strip-components=1 '
                         f'-xf {filename}')

        return True

    @classmethod
    async def update(cls):
        tasks = (pack.check_for_installed() for pack in cls._requested)
        await asyncio.gather(*tasks)

        if len(cls._missing) == 0:
            print('All tar-installed packages are up to date')
        elif config.dry_run:
            print('Not installing tar-packages because dry run')
            return True
        else:
            install_tasks = (pack.install() for pack in cls._missing)
            await asyncio.gather(*install_tasks)

        return True
