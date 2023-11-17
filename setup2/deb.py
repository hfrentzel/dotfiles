from .jobs import async_proc, fetch_file
from .job import Job
from .output import red, green


class Deb():

    @classmethod
    def deb_builder(cls, spec):
        async def inner():
            print(f'Installing {spec["name"]} from debian archive...')
            archive_file = await fetch_file(spec['url'], spec['version'])
            result = await async_proc(f'sudo apt install {archive_file}')
            success = not result.returncode
            if success:
                print(green(f'{spec["name"]} has been installed successfully'))
            else:
                print(red(f'Failed to install {spec["name"]} from debian archive'))
            return success

        return Job(names=[spec['name']],
                   description=f'Install {spec["name"]} from debian archive',
                   job=inner)
