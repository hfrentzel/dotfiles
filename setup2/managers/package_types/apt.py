from typing import List

from setup2.job import Job
from setup2.output import red, green
from setup2.process import async_proc
from setup2.managers.exe_class import Exe


class Apt():
    all_apts: List[str] = []

    @classmethod
    def apt_builder(cls, spec: Exe) -> bool:
        cls.all_apts.append(spec.name)
        return True

    @classmethod
    def apt_job(cls) -> Job:

        async def inner() -> bool:
            if len(cls.all_apts) == 0:
                return True
            print('Running apt install...')
            await async_proc('sudo apt update')
            result = await async_proc(f'sudo apt install --yes {" ".join(cls.all_apts)}')
            success = not result.returncode
            if success:
                print(green('The following apps were successfully installed '
                            f'with apt: {",".join(p[0] for p in cls.all_apts)}'))
            else:
                print(red('apt installation failed'))
                # TODO try installing packages one at a time
            return success

        return Job(names=cls.all_apts,
                   description=f'Install {", ".join(cls.all_apts)} with Apt',
                   job=inner)
