import json
import shlex
import subprocess

from .jobs import async_proc, ver_greater_than
from .job import Job
from .output import red, green

class Pip():
    all_pips = []
    curr_installed = None

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
    def get_version(cls, package):
        if cls.curr_installed is None:
            results = json.loads(
                subprocess.run(shlex.split('/usr/bin/python3.9 -m pip list --format=json'), 
                               capture_output=True).stdout.decode())
            cls.curr_installed = {r['name']: r['version'] for r in results}
        if cls.curr_installed.get(package['name']) is None:
            return None
        return cls.curr_installed[package['name']]


    @classmethod
    def check_install(cls, package):
        curr_ver = cls.get_version(package)
        if curr_ver is None:
            return {**package, 'complete': False, 'curr_ver': red('MISSING')}

        success = ver_greater_than(curr_ver, package['version'])
        color = green if success else red
        return {**package, 'complete': success, 'curr_ver': color(curr_ver)}
