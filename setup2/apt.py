from .jobs import async_proc
from .job import Job

class Apt():
    all_apts = []

    @classmethod
    def apt_builder(cls, spec):
        cls.all_apts.append(spec['name'])
        return True

    @classmethod
    def apt_job(cls):
        if len(cls.all_apts) == 0:
            return None

        async def inner():
            #TODO add output and proper error handling
            await async_proc('sudo apt update')
            result = await async_proc(f'sudo apt install --yes {" ".join(cls.all_apts)}')
            return not result['returncode']

        return Job(names=cls.all_apts,
                   description=f'Install {", ".join(cls.all_apts)} with Apt',
                   job=inner)
