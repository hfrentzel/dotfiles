from os.path import expanduser
from .jobs import async_proc
from .job import Job
from .output import red, green

class Npm():
    all_packages = []

    @classmethod
    def npm_builder(cls, spec):
        cls.all_packages.append((spec['name'], spec['version']))
        return True

    @classmethod
    def npm_job(cls):
        if len(cls.all_packages) == 0:
            return None

        npm_string = " ".join([p[0] for p in cls.all_packages])
        async def inner():
            print('Running npm install...')
            result = await async_proc(f'npm install -g {npm_string}',
                                      env={"NPM_CONFIG_USERCONFIG": 
                                            expanduser('~/.config/npm/npmrc')})
            success = not result.returncode
            if success:
                print(green('The following apps were successfully installed '
                           f'with npm: {",".join(p[0] for p in cls.all_packages)}'))
            else:
                print(red('npm installation failed'))
                # TODO try installing packages one at a time
            return success

        return Job(names=[p[0] for p in cls.all_packages],
                   description=f'Install {npm_string} with npm',
                   depends_on='node',
                   job=inner)
