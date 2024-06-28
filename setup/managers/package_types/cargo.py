from typing import TYPE_CHECKING

from setup.job import Job
from setup.output import green, red
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def cargo_builder(spec: "Exe", package: str) -> Job:
    async def inner() -> bool:
        print(f"Installing {spec.name} with cargo...")
        result = await async_proc(f"cargo install --version {spec.version} {package}")
        success = not result.returncode
        if success:
            print(green(f"{spec.name} has been installed successfully"))
        else:
            print(red(f"Failed to install {spec.name} with cargo"))
        return success

    return Job(
        names=[spec.name],
        description=f"Install {spec.name} with cargo",
        depends_on="cargo",
        job=inner,
    )
