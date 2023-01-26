import asyncio
import dataclasses
import json
from setup_tools.utils import ready_to_run, successful
from setup_tools.installers import async_proc
from setup_tools.config import config


@dataclasses.dataclass(frozen=True)
class PipPackage:
    name: str
    version: str

    def __str__(self):
        return f'{self.name}=={self.version}'


@dataclasses.dataclass
class PipStatus:
    requested: set = dataclasses.field(default_factory=set)
    missing: set = dataclasses.field(default_factory=set)
    queued: bool = False


pip_status = PipStatus()


def pip_package(package_name: str, version: str):
    pip_status.requested.add(PipPackage(package_name, version))
    if not pip_status.queued and not config.check:
        ready_to_run.append(install_pip_packages())
        pip_status.queued = True


async def _check_for_installed(package: PipPackage, pack_list):
    if package.name not in pack_list:
        pip_status.missing.add(package)
        return
    if pack_list[package.name] != package.version:
        print(f'{package.name} is not at correct version. Expected {package.version}. '
              f'Installed: {pack_list[package.name]}')
        pip_status.missing.add(package)
        return

    if config.verbose:
        print(f'{package.name} is installed and up to date ({package.version})')
    successful.add(package.name)
    return


async def install_pip_packages():
    pip_status.queued = False

    freeze_list = await async_proc('/usr/bin/python -m pip list --format=json')
    freeze_packs = {p['name']: p['version'] for p in
                    json.loads(freeze_list['stdout'])}
    tasks = (_check_for_installed(p, freeze_packs)
             for p in pip_status.requested)
    await asyncio.gather(*tasks)

    if len(pip_status.missing) == 0:
        print('All pip packages up to date')
        return True

    if config.dry_run:
        print('Not installing anything because dry run')
        return True

    print(f'Installing python packages {pip_status.missing}')
    all_packages = ' '.join(str(p) for p in pip_status.missing)
    await async_proc(f'/usr/bin/python -m pip install {all_packages}')

    return True


async def check_up_to_date():
    outdated_list, uptodate_list = await asyncio.gather(
        async_proc('/usr/bin/python -m pip list -o --format=json'),
        async_proc('/usr/bin/python -m pip list -u --format=json'))

    outdated = {p['name']: {'curr': p['version'], 'avail': p['latest_version']}
                for p in json.loads(outdated_list['stdout'])}
    uptodate = {p['name']: p['version'] for p in
                json.loads(uptodate_list['stdout'])}
    name_length = max(len(p.name) for p in pip_status.requested)
    print(f'{"name": <{name_length}} Current  Available')

    for pack in pip_status.requested:
        if pack.name in outdated:
            print(f'{pack.name: <{name_length}} {outdated[pack.name]["curr"]: <8} '
                  f'{outdated[pack.name]["avail"]}')
        elif pack.name in uptodate:
            print(f'{pack.name: <{name_length}} {uptodate[pack.name]: <8} '
                  f'Up To Date')
