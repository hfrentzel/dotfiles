from .jobs import async_proc
from .job import Job
from .output import red, green

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
            print('Running pip install...')
            result = await async_proc(
                f'/usr/bin/python -m pip install {pip_string}')
            success = not result.returncode
            if success:
                print(green('The following apps were successfully installed '
                           f'with pip: {",".join(p[0] for p in cls_all_pips)}'))
            else:
                print(red('pip installation failed'))
                # TODO try installing packages one at a time
            return success

        return Job(names=[p[0] for p in cls.all_pips],
                   description=f'Install {pip_string} with pip',
                   depends_on='python3.9',
                   job=inner)
