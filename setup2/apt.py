from typing import List
from .jobs import async_proc
from .job import Job
from .output import red, green


class Apt():
    all_apts: List[str] = []

    @classmethod
    def apt_builder(cls, spec):
        cls.all_apts.append(spec['name'])
        return True

    @classmethod
    def apt_job(cls):
        if len(cls.all_apts) == 0:
            return None

        async def inner():
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
