from dataclasses import dataclass
from os import path
import asyncio
from typing import Optional

from .conf import conf


@dataclass
class JobOutput:
    stdout: str
    stderr: str
    returncode: Optional[int]


def ver_greater_than(current: str, target: str) -> bool:
    curr_major, curr_minor, curr_patch = current.split(".")
    tar_major, tar_minor, tar_patch = target.split(".")
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


async def fetch_file(url: str, version: str) -> str:
    full_url = url.format(version=version)
    _, file = path.split(full_url)

    filename = f'{conf.sources_dir}/{file}'
    await async_proc(f'curl -L {full_url} -o {filename}')

    return filename
