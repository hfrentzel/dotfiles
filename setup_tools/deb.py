import shutil

from setup_tools.config import config
from setup_tools.installers import async_proc
from setup_tools.utils import add_job


def deb_package(command, url, version_check, version):
    if not config.check:
        add_job(install_deb(command, url, version, version_check),
                run_on_dry=True)


async def install_deb(command: str, url: str, version: str,
                      version_check: str):
    need_to_install = False
    if not shutil.which(command):
        print(f'{command} is not installed')
        need_to_install = True
    elif (curr_ver := (await async_proc(version_check))['stdout']) != version:
        print(f'{command} ({curr_ver}) is not up to date. Can be updated to '
              f'{version}')
        need_to_install = True
    else:
        print(f'{command} is installed and up to date ({version})')

    if config.dry_run or not need_to_install:
        return True

    full_url = url.format(version=version)
    filename = f'{command}-{version}.deb'

    await async_proc(f'curl -L {full_url} -o {filename}')
    await async_proc(f'sudo apt install {filename}')

    return True
