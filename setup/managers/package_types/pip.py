import os
import re
import subprocess
from typing import List, Optional, Tuple

from setup.job import Job
from setup.managers.manager import Package
from setup.managers.package_types.versioning import check_install
from setup.output import green, red
from setup.process import async_proc


class Pip:
    all_pips: List[Tuple[str, str]] = []
    files: str = ""

    @classmethod
    def pip_builder(cls, spec: Package, package: str) -> bool:
        cls.all_pips.append((package, spec.version))
        return True

    @classmethod
    def pip_job(cls) -> Job:
        pip_string = " ".join([f"{p[0]}=={p[1]}" for p in cls.all_pips])

        async def inner() -> bool:
            if len(cls.all_pips) == 0:
                return True

            print("Running pip install...")
            result = await async_proc(f"python -m pip install {pip_string}")
            success = not result.returncode
            if success:
                print(
                    green(
                        'The following apps were successfully installed '
                        f'with pip: {",".join(p[0] for p in cls.all_pips)}'
                    )
                )
            else:
                print(red("pip installation failed"))
                # TODO try installing packages one at a time
            return success

        return Job(
            names=[p[0] for p in cls.all_pips],
            description=f"Install {pip_string} with pip",
            depends_on="python",
            job=inner,
        )

    @classmethod
    def get_version(cls, package: Package) -> Optional[str]:
        if not cls.files:
            pip_dir = (
                subprocess.run(
                    ["python", "-m", "site", "--user-site"], check=False, capture_output=True
                )
                .stdout.decode()
                .strip()
            )
            cls.files = "\n".join([
                s.replace("_", "-") for s in os.listdir(pip_dir) if "dist-info" in s
            ])

        if (m := re.search(f"{package.name}-(.*)\\.dist-info", cls.files)) is not None:
            return m.group(1)
        return None

    @classmethod
    def check_install(cls, package: Package) -> Tuple[bool, str]:
        curr_ver = cls.get_version(package)
        return check_install(curr_ver, package)
