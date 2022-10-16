import asyncio
import os
import subprocess

from setup_tools.installers import install_linux_package, async_proc
from setup_tools.symlink import symlink, execute_symlinks
from vim import install_neovim, install_command_t
from languages.python import install_python

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
    create_action('ripgrep', install_linux_package('ruby-dev'), ['apt_update'])
    create_action('ruby', install_linux_package('ruby'), ['apt_update'])
    create_action('ruby-dev', install_linux_package('ruby-dev'), ['apt_update'])

    create_action('neovim', install_neovim(dotfiles_home))
    create_action('python', install_python())

    create_action('command_t', install_command_t(dotfiles_home),
                  ['ruby', 'ruby-dev', 'submodules'])

    symlink('DOTROOT/bash/.bash', '~/.bash')
    symlink('DOTROOT/bash/.bashrc', '~/.bashrc')
    symlink('DOTROOT/bash/.inputrc', '~/.inputrc')
    symlink('DOTROOT/configs/.rgrc', '~/.rgrc')
    symlink('DOTROOT/git/gitconfig', '~/.gitconfig')
    symlink('DOTROOT/tmux/.tmux.conf', '~/.tmux.conf')

    execute_symlinks(dotfiles_home)
    for a in all_actions.values():
        await a


if __name__ == '__main__':
    asyncio.run(main())
