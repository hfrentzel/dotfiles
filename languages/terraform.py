from setup_tools.config import config
from setup_tools.installers import async_proc, check_version, fetch_file
from setup_tools.utils import add_job


def install_terraform():
    async def terraform():
        version = '1.3.7'
        url = 'https://releases.hashicorp.com/terraform/{version}/terraform_{version}_linux_amd64.zip'

        async def install():
            print('Installing terraform')
            filename = await fetch_file(version, url)
            await async_proc(f'unzip {filename}', cwd=config.sources_home)
            await async_proc('mv terraform ~/.local/bin/terraform', cwd=config.sources_home)

        is_setup = await check_version('terraform', version)

        if is_setup or config.dry_run:
            return True

        await install()
        return True

    async def terraform_ls():
        version = '0.30.1'
        url = 'https://releases.hashicorp.com/terraform-ls/{version}/terraform-ls_{version}_linux_amd64.zip'

        async def install():
            print('Installing terraform-ls')
            filename = await fetch_file(version, url)
            await async_proc(f'unzip {filename}', cwd=config.sources_home)
            await async_proc('mv terraform-ls ~/.local/bin/terraform-ls', cwd=config.sources_home)

        is_setup = await check_version('terraform-ls', version)

        if is_setup or config.dry_run:
            return True

        await install()
        return True

    add_job(terraform(), run_on_dry=True)
    add_job(terraform_ls(), run_on_dry=True)
