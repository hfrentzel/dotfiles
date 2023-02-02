from setup_tools.config import config
from setup_tools.utils import add_job
from setup_tools.installers import async_proc


def install_aws():
    async def aws():
        installed = await async_proc('aws --version')
        if not installed['returncode']:
            print('aws cli is installed')
            return True

        print('aws cli not installed')
        if config.dry_run:
            return True

        print('Installing aws cli')
        url = "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
        filename = f'{config.sources_home}/awscli.zip'
        await async_proc(f'curl -L "{url}" -o {filename}')
        await async_proc(f'unzip {filename}', cwd=config.sources_home)
        await async_proc('sudo ./aws/install', cwd=config.sources_home)

    add_job(aws(), run_on_dry=True)
