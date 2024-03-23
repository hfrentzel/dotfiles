import asyncio
from dataclasses import dataclass
from itertools import zip_longest
import platform
import os
from typing import Optional, List, Literal, overload

from .conf import conf


@dataclass
class JobOutput:
    stdout: str
    stderr: str
    returncode: Optional[int]


def ver_greater_than(current: str, target: str) -> bool:
    curr_segments = [int(t) for t in current.split(".")]
    tar_segments = [int(t) for t in target.split(".")]
    for curr, tar in zip_longest(curr_segments, tar_segments, fillvalue=0):
        if curr > tar:
            return True
        if curr < tar:
            return False
    return True


async def async_proc(cmd: str,
                     cwd: Optional[str] = None,
                     stdin: Optional[bytes] = None,
                     forward_env: bool = False) -> JobOutput:
    if isinstance(stdin, str):
        stdin = stdin.encode()
    # TODO Log stdout and stderr if command fails
    process = await asyncio.create_subprocess_shell(
        cmd,
        cwd=cwd,
        env=os.environ if forward_env else None,
        stdin=asyncio.subprocess.PIPE if stdin else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate(stdin)
    return JobOutput(
        stdout=stdout.decode().strip('\n'),
        stderr=stderr.decode().strip('\n'),
        returncode=process.returncode
    )


async def fetch_file(url: str, version: Optional[str]) -> str:
    full_url = url
    if version is not None:
        full_url = url.format(version=version)
    _, file = os.path.split(full_url)

    filename = f'{conf.sources_dir}/{file}'
    if not os.path.exists(filename):
        await async_proc(f'curl -L {full_url} -o {filename}')

    return filename


@overload
def filter_assets(asset_list: List[str], return_all: Literal[True]) -> List[str]:
    ...


@overload
def filter_assets(asset_list: List[str]) -> Optional[str]:
    ...


def filter_assets(asset_list, return_all=False):
    system = platform.uname()
    system_os = system.system.lower()
    hardware = set_hardware(system.machine.lower())
    if False and any(a.endwiths('.deb') for a in asset_list):
        # TODO handle deb files when sudo permissions are available
        pass

    asset_list = [a for a in asset_list if a.endswith('.zip') or '.tar.' in a]

    if any(system_os in a for a in asset_list):
        asset_list = [a for a in asset_list if system_os in a]
    if any(any(h in a for a in asset_list) for h in hardware):
        asset_list = [a for a in asset_list if any(h in a for h in hardware)]

    if system_os == 'linux' and 'x86_64' in hardware and len(asset_list) == 2:
        asset_list = [a for a in asset_list if 'musl' not in a] or asset_list

    if return_all:
        return asset_list
    if len(asset_list) == 1:
        return asset_list[0]
    return None


def set_hardware(machine: str) -> List[str]:
    if machine in ['amd64', 'x86_64']:
        return ['amd64', 'x86_64', 'x64']
    if machine == 'aarch64' and platform.architecture()[0] == '64bit':
        return ['aarch64', 'arm64']
    if machine == 'aarch64' and platform.architecture()[0] == '32bit':
        return ['armv7', 'arm-']
    return ['']
