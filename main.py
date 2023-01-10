import asyncio
import os
import subprocess

from setup_tools.installers import async_proc, command
from setup_tools.symlink import symlink, execute_symlinks
from setup_tools.linux import linux_package
from setup_tools.utils import run_tasks, add_job
from vim import install_neovim, install_command_t
from languages.python import install_python


async def init_git():
    print('Initializing submodules...')
    await async_proc('git submodule init')

    print('Updating submodules...')
    await async_proc('git submodule update')

    print('Submodules updated')
    return True


async def main():
    subprocess.run(['sudo', 'pwd'], capture_output=True, check=True)

    dotfiles_home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dotfiles_home)

    add_job(init_git())
    command('sudo apt update')

    # Apt packages
    linux_package('dos2unix')
    linux_package('jq')
    linux_package('ripgrep')

    install_neovim()
    install_python()

    # install_command_t()

    symlink('DOTROOT/bash/.bash', '~/.bash')
    symlink('DOTROOT/bash/.bashrc', '~/.bashrc')
    symlink('DOTROOT/bash/.inputrc', '~/.inputrc')
    symlink('DOTROOT/configs/.rgrc', '~/.rgrc')
    symlink('DOTROOT/git/gitconfig', '~/.gitconfig')
    symlink('DOTROOT/tmux/.tmux.conf', '~/.tmux.conf')

    execute_symlinks(dotfiles_home)
    await run_tasks()


if __name__ == '__main__':
    asyncio.run(main())
