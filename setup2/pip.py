from .jobs import async_proc
from .job import Job

class Pip():
    all_pips = []

    @classmethod
    def pip_builder(cls, spec):
        cls.all_pips.append(spec['name'])
        return True

    @classmethod
    def pip_job(cls):
        if len(cls.all_pips) == 0:
            return None

        async def inner():
            #TODO add output and proper error handling
            result = await async_proc(
                f'/usr/bin/python -m pip install {" ".join(cls.all_pips)}')
            return not result['returncode']

        return Job(names=cls.all_pips,
                   description=f'Install {", ".join(cls.all_pips)} with pip',
                   job=inner)
