from .jobs import async_proc
from .job import Job
from .output import red, green
from .exe_class import Exe


def cargo_builder(spec: Exe) -> Job:
    async def inner() -> bool:
        print(f'Installing {spec.name} with cargo...')
        result = await async_proc(
            f'cargo install --version {spec.version} {spec.name}')
        success = not result.returncode
        if success:
            print(green(f'{spec.name} has been installed successfully'))
        else:
            print(red(f'Failed to install {spec.name} with cargo'))
        return success

    return Job(names=[spec.name],
               description=f'Install {spec.name} with cargo',
               depends_on='cargo',
               job=inner)
