import json
import shlex
import subprocess
from typing import Optional, List, Tuple, Dict

from setup2.job import Job
from setup2.output import red, green
from setup2.process import async_proc, ver_greater_than
from setup2.managers.manager import Package


class Pip():
    all_pips: List[Tuple[str, str]] = []
    curr_installed: Optional[Dict[str, str]] = None

    @classmethod
    def pip_builder(cls, spec: Package) -> bool:
        cls.all_pips.append((spec.name, spec.version))
        return True

    @classmethod
    def pip_job(cls) -> Job:
        pip_string = " ".join([f'{p[0]}=={p[1]}' for p in cls.all_pips])

        async def inner() -> bool:
            if len(cls.all_pips) == 0:
                return True

            print('Running pip install...')
            result = await async_proc(
                f'/usr/bin/python3.9 -m pip install {pip_string}')
            success = not result.returncode
            if success:
                print(green('The following apps were successfully installed '
                            f'with pip: {",".join(p[0] for p in cls.all_pips)}'))
            else:
                print(red('pip installation failed'))
                # TODO try installing packages one at a time
            return success

        return Job(names=[p[0] for p in cls.all_pips],
                   description=f'Install {pip_string} with pip',
                   depends_on='python3.9',
                   job=inner)

    @classmethod
    def get_version(cls, package: Package) -> Optional[str]:
        if cls.curr_installed is None:
            results = json.loads(
                subprocess.run(shlex.split('/usr/bin/python3.9 -m pip list --format=json'),
                               check=False, capture_output=True).stdout.decode())
            cls.curr_installed = {r['name']: r['version'] for r in results}
        if cls.curr_installed.get(package.name) is None:
            return None
        return cls.curr_installed[package.name]

    @classmethod
    def check_install(cls, package: Package) -> Tuple[bool, str]:
        curr_ver = cls.get_version(package)
        if curr_ver is None:
            return (False, red('MISSING'))

        success = ver_greater_than(curr_ver, package.version)
        color = green if success else red
        return (success, color(curr_ver))
