import json
import subprocess
import shlex

from os.path import expanduser
from .jobs import async_proc, ver_greater_than
from .job import Job
from .output import red, green

class Npm():
    all_packages = []
    curr_installed = None

    @classmethod
    def npm_builder(cls, spec):
        cls.all_packages.append((spec['name'], spec['version']))
        return True

    @classmethod
    def npm_job(cls):
        if len(cls.all_packages) == 0:
            return None

        npm_string = " ".join([f'{p[0]}@{p[1]}' for p in cls.all_packages])
        async def inner():
            print('Running npm install...')
            result = await async_proc(f'npm install -g {npm_string}')
            success = not result.returncode
            if success:
                print(green('The following apps were successfully installed '
                           f'with npm: {",".join(p[0] for p in cls.all_packages)}'))
            else:
                print(red('npm installation failed'))
                # TODO try installing packages one at a time
            return success

        return Job(names=[p[0] for p in cls.all_packages],
                   description=f'Install {",".join(p[0] for p in cls.all_packages)} with npm',
                   depends_on='node',
                   job=inner)

    @classmethod
    def get_version(cls, package):
        if cls.curr_installed is None:
            results = json.loads(
                subprocess.run(shlex.split('npm -g -j list'), 
                               capture_output=True).stdout.decode())
            cls.curr_installed = {k: v['version'] for (k, v) in results['dependencies'].items()}
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
