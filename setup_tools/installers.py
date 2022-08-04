import asyncio


async def async_proc(cmd, input=None):
    process = await asyncio.create_subprocess_shell(cmd,
                                                    stdin=asyncio.subprocess.PIPE if input else None,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate(input)
    return {
        'stdout': stdout,
        'stderr': stderr,
        'returncode': process.returncode
    }


async def add_apt_repo(repo_name):
    repo_list = await async_proc('apt-cache policy')
    grep = await async_proc(f'grep {repo_name.split(":")[-1]}', repo_list['stdout'])

    if not grep['returncode']:
        print(f'{repo_name} is already in the apt cache')
        return

    print(f'Adding {repo_name}')
    await async_proc(f'sudo add-apt-repository --yes {repo_name}')
    print(f'{repo_name} successfully added')

    print('Running apt update')
    await async_proc('sudo apt update')


async def install_linux_package(package_name, repo_name=None):
    print(f'Checking for installed package {package_name}')

    package_exists = await async_proc(f'dpkg -s {package_name}')
    if not package_exists['returncode']:
        print(f'{package_name} is already installed')
        return False

    print(f'{package_name} is not installed')
    if repo_name:
        await add_apt_repo(repo_name)

    print(f'Installing {package_name}...')

    install = await async_proc(f'sudo apt install --yes {package_name}')
    if not install['returncode']:
        print(f'{package_name} successfully installed')
        return True

    print(f'Failed to install {package_name}')
    return False


async def pip_install(package_name):
    freeze_list = await async_proc('python3 -m pip freeze')
    grep = await async_proc(f'grep {package_name}', freeze_list['stdout'])

    if not grep['returncode']:
        print(f'{package_name} is already installed to python')

    print(f'Installing python package {package_name}')
    await async_proc(f'python3 -m pip install {package_name}')
