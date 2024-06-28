from typing import TYPE_CHECKING

from setup.job import Job
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def sequence_builder(spec: "Exe", _: str = "") -> Job:
    async def inner() -> bool:
        print(f"Beginning steps to install {spec.name}")
        for step_template in spec.steps:
            step = step_template.format(version=spec.version)
            result = await async_proc(step)
            if result.returncode != 0:
                print(f"{spec.name} installation failed on step: {step}")
                return False

        return True

    return Job(
        names=[spec.name],
        description=f"Execute {spec.name} installation sequence",
        depends_on=spec.depends_on,
        job=inner,
    )
