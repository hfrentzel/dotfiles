import json
import platform
from typing import TYPE_CHECKING

from setup.job import Job
from setup.managers.package_types.tar import tar_builder
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def build_hole_builder(spec: "Exe", _: str = "") -> Job:
    async def inner() -> bool:
        hole = await get_hole()

        hardware = platform.uname().machine.lower()
        if hardware == "x86_64":
            env = "x86_64-linux-20.04"
        else:
            env = "aarch64-linux-22.04"
        spec.url = hole[spec.name][spec.version][env]

        await tar_builder(spec).run()
        return True

    return Job(
        names=[spec.name],
        description=f"Install {spec.name} from build-hole",
        job=inner,
    )


async def get_hole():
    url = "https://raw.githubusercontent.com/hfrentzel/build-hole/master/hole.json"
    result = await async_proc(f"curl -L {url}")
    hole = json.loads(result.stdout)
    return hole
