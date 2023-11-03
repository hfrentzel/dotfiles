from dataclasses import dataclass
import asyncio

@dataclass
class JobOutput:
    stdout: str
    stderr: str
    returncode: int

async def async_proc(cmd, stdin=None, cwd=None):
    if isinstance(stdin, str):
        stdin = stdin.encode()
    #TODO Log stdout and stderr if command fails
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

