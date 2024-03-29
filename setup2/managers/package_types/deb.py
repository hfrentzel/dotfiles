from setup2.job import Job
from setup2.output import red, green
from setup2.process import async_proc, fetch_file
from setup2.managers.exe_class import Exe


def deb_builder(spec: Exe) -> Job:
    async def inner() -> bool:
        print(f'Installing {spec.name} from debian archive...')
        archive_file = await fetch_file(spec.url, spec.version)
        result = await async_proc(f'sudo apt install {archive_file}')
        success = not result.returncode
        if success:
            print(green(f'{spec.name} has been installed successfully'))
        else:
            print(red(f'Failed to install {spec.name} from debian archive'))
        return success

    return Job(names=[spec.name],
               description=f'Install {spec.name} from debian archive',
               job=inner)
