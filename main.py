import asyncio
import os
import subprocess

from setup_tools.installers import install_linux_package, pip_install, \
    async_proc
from vim import install_neovim, install_command_t

all_actions: dict = {}


def create_action(name, action, dependencies=None):
    async def task(job):
        if dependencies is not None:
            for d in dependencies:
                await all_actions[d]

        await job

    all_actions[name] = asyncio.create_task(task(action))


async def init_git():
    print('Initializing submodules...')
    await async_proc('git submodule init')

    print('Updating submodules...')
    await async_proc('git submodule update')

    print('Submodules updated')


async def main():
    subprocess.run(['sudo', 'pwd'], capture_output=True, check=True)

    dotfiles_home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dotfiles_home)

    create_action('submodules', init_git())
    create_action('apt_update', async_proc('sudo apt update'))

    # Apt packages
    create_action('dos2unix', install_linux_package('dos2unix'), ['apt_update'])
    create_action('neovim', install_neovim(dotfiles_home))
    create_action('pip', install_linux_package('python3-pip'), ['apt_update'])
    create_action('ruby', install_linux_package('ruby'), ['apt_update'])
    create_action('ruby-dev', install_linux_package('ruby-dev'), ['apt_update'])

    create_action('pylsp', pip_install('python-lsp-server'), ['pip'])
    create_action('flake8', pip_install('flake8'), ['pip'])
    create_action('pylint', pip_install('flake8'), ['pip'])
    create_action('mypy', pip_install('pylsp-mypy'), ['pip'])

    create_action('command_t', install_command_t(dotfiles_home), ['ruby', 'ruby-dev', 'submodules'])

    for a in all_actions.values():
        await a


if __name__ == '__main__':
    asyncio.run(main())
