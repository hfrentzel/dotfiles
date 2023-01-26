import asyncio
import os
import subprocess

from setup_tools.installers import async_proc, command
from setup_tools.pip import check_up_to_date
from setup_tools.symlink import symlink, execute_symlinks
from setup_tools.config import config
from setup_tools.linux import linux_package
from setup_tools.deb import deb_package
from setup_tools.utils import run_tasks, add_job
from vim import install_neovim
from languages.python import install_python, python_editing


async def init_git():
    print('Initializing submodules...')
    await async_proc('git submodule init')

    print('Updating submodules...')
    await async_proc('git submodule update')

    print('Submodules updated')
    return True


async def main():
    config.dry_run = True
    # config.check = True
    subprocess.run(['sudo', 'pwd'], capture_output=True, check=True)

    dotfiles_home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dotfiles_home)

    # Apt packages
    linux_package('dos2unix')
    linux_package('jq')
    linux_package('ripgrep')
    deb_package(command='rg',
                url='https://github.com/BurntSushi/ripgrep/releases/download/'
                    '{version}/ripgrep_{version}_amd64.deb',
                version_check="rg --version | head -1 | grep -o '[0-9\\.]\\+'",
                version='13.0.0'
                )

    install_neovim()
    install_python()

    python_editing()

    symlink('DOTROOT/bash/.bash', '~/.bash')
    symlink('DOTROOT/bash/.bashrc', '~/.bashrc')
    symlink('DOTROOT/bash/.inputrc', '~/.inputrc')
    symlink('DOTROOT/configs/.rgrc', '~/.rgrc')
    symlink('DOTROOT/git/gitconfig', '~/.gitconfig')
    symlink('DOTROOT/tmux/.tmux.conf', '~/.tmux.conf')

    if not config.check:
        execute_symlinks(dotfiles_home)
        add_job(init_git())
        command('sudo apt update')

    await run_tasks()
    if config.check:
        await check_up_to_date()


if __name__ == '__main__':
    asyncio.run(main())
