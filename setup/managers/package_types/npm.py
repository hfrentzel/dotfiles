import json
import os
from typing import List, Optional, Tuple

from setup.job import Job
from setup.managers.manager import Package
from setup.managers.package_types.versioning import check_install
from setup.output import green, red
from setup.process import async_proc


class Npm:
    all_packages: List[Tuple[str, str]] = []

    @classmethod
    def npm_builder(cls, spec: Package, package: str) -> bool:
        cls.all_packages.append((package, spec.version))
        return True

    @classmethod
    def npm_job(cls) -> Job:
        npm_string = " ".join([f"{p[0]}@{p[1]}" for p in cls.all_packages])

        async def inner() -> bool:
            if len(cls.all_packages) == 0:
                return True

            print("Running npm install...")
            result = await async_proc(f"npm install -g {npm_string}")
            success = not result.returncode
            if success:
                print(
                    green(
                        'The following apps were successfully installed '
                        f'with npm: {",".join(p[0] for p in cls.all_packages)}'
                    )
                )
            else:
                print(red("npm installation failed"))
                # TODO try installing packages one at a time
            return success

        return Job(
            names=[p[0] for p in cls.all_packages],
            description=f'Install {",".join(p[0] for p in cls.all_packages)} with npm',
            depends_on="node",
            job=inner,
        )

    @classmethod
    def get_version(cls, package: Package) -> Optional[str]:
        path = os.path.join(
            os.path.expanduser("~/.local/lib/node_modules"),
            package.name,
            "package.json",
        )
        if not os.path.exists(path):
            return None
        with open(path) as f:
            if isinstance(version := json.loads(f.read()).get("version"), str):
                return version
        return None

    @classmethod
    def check_install(cls, package: Package) -> Tuple[bool, str]:
        curr_ver = cls.get_version(package)
        return check_install(curr_ver, package)
