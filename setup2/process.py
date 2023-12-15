import asyncio
from dataclasses import dataclass
from os import path
from typing import Optional, List

from .conf import conf


@dataclass
class JobOutput:
    stdout: str
    stderr: str
    returncode: Optional[int]


def ver_greater_than(current: str, target: str) -> bool:
    curr_major, curr_minor, curr_patch = [int(t) for t in current.split(".")]
    tar_major, tar_minor, tar_patch = [int(t) for t in target.split(".")]
    return (
        curr_major > tar_major or
        (curr_major == tar_major and curr_minor > tar_minor) or
        (curr_major == tar_major and curr_minor == tar_minor and curr_patch >= tar_patch))


async def async_proc(cmd: str, stdin: Optional[bytes] = None,
                     cwd: Optional[str] = None) -> JobOutput:
    if isinstance(stdin, str):
        stdin = stdin.encode()
    # TODO Log stdout and stderr if command fails
    process = await asyncio.create_subprocess_shell(
        cmd,
        cwd=cwd,
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
    _, file = path.split(full_url)

    filename = f'{conf.sources_dir}/{file}'
    if not path.exists(filename):
        await async_proc(f'curl -L {full_url} -o {filename}')

    return filename


def filter_assets(asset_list: List[str]) -> Optional[str]:
    # TODO Infer these values from environment and handle other
    # possibilities
    system_os = 'linux'
    hardware = ['x86_64', 'amd64', 'x64']
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

    if len(asset_list) == 1:
        return asset_list[0]
    return None
