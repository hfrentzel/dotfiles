from typing import TYPE_CHECKING

from setup.job import Job
from setup.output import green, red
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def go_builder(spec: "Exe", _: str = "") -> Job:
    async def inner() -> bool:
        print(f"Installing {spec.name} with go...")
        result = await async_proc(f"go install {spec.url}@v{spec.version}")
        success = not result.returncode
        if success:
            print(green(f"{spec.name} has been installed successfully"))
        else:
            print(red(f"Failed to install {spec.name} with go"))
        return success

    return Job(
        names=[spec.name],
        description=f"Install {spec.name} with go",
        depends_on="go",
        job=inner,
    )
