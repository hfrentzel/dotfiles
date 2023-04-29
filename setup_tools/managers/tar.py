import asyncio
from typing import Optional

from setup_tools.config import config
from setup_tools.installers import async_proc, check_version, \
    fetch_file
from setup_tools.jobs import successful
from setup_tools.managers.manager import Manager


class Tar(Manager):
    def __init__(self, command: str, url: str, version: str,
                 includes: str = 'bundle',
                 version_check: Optional[str] = None):
        self.name = command
        self.url = url
        self.version_check = version_check
        self.version = version
        self.tarball_type = includes
        self._requested.add(self)

    async def check_for_installed(self):
        version = await check_version(self.name, self.version,
                                      self.version_check)
        if version is None or isinstance(version, str):
            self._missing.add((self, version))
        else:
            successful.add(self.name)

    async def install(self):

        filename = await fetch_file(self.version, self.url)
        flags = 'zxf' if filename.endswith('gz') else 'xf'
        if self.tarball_type == 'bin':
            dest = '/usr/local/bin'
        elif self.tarball_type == 'bundle':
            dest = '/usr/local --strip-components=1'

        result = await async_proc(f'sudo tar -C {dest} '
                                  f'-{flags} {filename}')
        if result['returncode'] != 0:
            print(f'Tar {self.name} failed to install')
            return True
        print(f'Tar {self.name} installed successfully')
        successful.add(self.name)
        return True

    @classmethod
    async def update(cls):
        tasks = (pack.check_for_installed() for pack in cls._requested)
        await asyncio.gather(*tasks)

        if len(cls._missing) == 0:
            return True
        if config.dry_run:
            print('Not installing tar-packages because dry run')
            return True

        install_tasks = (pack[0].install() for pack in cls._missing)
        await asyncio.gather(*install_tasks)

        return True
