from dataclasses import dataclass
from os import path
import asyncio

from .conf import conf

@dataclass
class JobOutput:
    stdout: str
    stderr: str
    returncode: int

async def async_proc(cmd, stdin=None, cwd=None, env=None):
    if '|' in cmd:
        parts = cmd.split('|')
        for part in parts:
            intermediate = await async_proc(part.strip(), stdin=stdin, cwd=cwd,
                                            env=env)
            if intermediate.returncode != 0:
                return intermediate
            stdin = intermediate.stdout
        return intermediate

    if isinstance(stdin, str):
        stdin = stdin.encode()
    #TODO Log stdout and stderr if command fails
    process = await asyncio.create_subprocess_shell(
        cmd,
        cwd=cwd,
        env=env,
        stdin=asyncio.subprocess.PIPE if stdin else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate(stdin)
    return JobOutput(
        stdout=stdout.decode().strip('\n'),
        stderr=stderr.decode().strip('\n'),
        returncode=process.returncode
    )


async def fetch_file(url, version):
    full_url = url.format(version=version)
    _, file = path.split(full_url)

    filename = f'{conf.sources_dir}/{file}'
    await async_proc(f'curl -L {full_url} -o {filename}')

    return filename
