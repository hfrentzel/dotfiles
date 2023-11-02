from .jobs import async_proc
from .job import Job

class Pip():
    all_pips = []

    @classmethod
    def pip_builder(cls, spec):
        cls.all_pips.append((spec['name'], spec['version']))
        return True

    @classmethod
    def pip_job(cls):
        if len(cls.all_pips) == 0:
            return None

        pip_string = " ".join([f'{p[0]}=={p[1]}' for p in cls.all_pips])
        async def inner():
            #TODO add output and proper error handling
            result = await async_proc(
                f'/usr/bin/python -m pip install {pip_string}')
            return not result['returncode']

        return Job(names=[p[0] for p in cls.all_pips],
                   description=f'Install {pip_string} with pip',
                   depends_on='python3.9',
                   job=inner)
