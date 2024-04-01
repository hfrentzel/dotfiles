from setup2.job import Job
from setup2.output import red, green
from setup2.process import async_proc
from setup2.managers.exe_class import Exe

Exe('go',
    version='1.20.11',
    on_demand=True,
    installers=['Tar'],
    extract_path='~/.local',
    url='https://go.dev/dl/go{version}.linux-amd64.tar.gz')


def go_builder(spec: Exe, _: str = "") -> Job:
    async def inner() -> bool:
        print(f'Installing {spec.name} with go...')
        result = await async_proc(
            f'go install {spec.url}@v{spec.version}')
        success = not result.returncode
        if success:
            print(green(f'{spec.name} has been installed successfully'))
        else:
            print(red(f'Failed to install {spec.name} with go'))
        return success

    return Job(names=[spec.name],
               description=f'Install {spec.name} with go',
               depends_on='go',
               job=inner)
