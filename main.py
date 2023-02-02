import asyncio
import os
import subprocess

from setup_tools.installers import async_proc, command
from setup_tools.managers import all_managers, Apt, Deb, Symlink
from setup_tools.config import config
from setup_tools.utils import run_tasks, add_job
from vim import install_neovim
from languages.python import install_python, python_editing
from languages.javascript import install_javascript
from clis.aws import install_aws


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
    config.sources_home = '~/.pack_sources'
    subprocess.run(['sudo', 'pwd'], capture_output=True, check=True)

    config.dotfiles_home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(config.dotfiles_home)

    # Base tools
    Apt('dos2unix')
    Apt('jq')
    Deb(command='delta', version='0.15.1',
        url='https://github.com/dandavison/delta/releases/download/'
            '{version}/git-delta-musl_{version}_amd64.deb',
        version_check=" delta --version | head -1 | grep -o '[0-9\\.]\\+' | tail -1"
        )
    Deb(command='rg', version='13.0.0',
        url='https://github.com/BurntSushi/ripgrep/releases/download/'
            '{version}/ripgrep_{version}_amd64.deb',
        version_check="rg --version | head -1 | grep -o '[0-9\\.]\\+' | head -1"
        )
    Symlink('DOTROOT/bash/.bash', '~/.bash')
    Symlink('DOTROOT/bash/.bashrc', '~/.bashrc')
    Symlink('DOTROOT/bash/.inputrc', '~/.inputrc')
    Symlink('DOTROOT/configs/.rgrc', '~/.rgrc')
    Symlink('DOTROOT/git/gitconfig', '~/.gitconfig')
    Symlink('DOTROOT/tmux/.tmux.conf', '~/.tmux.conf')

    # Additional components
    install_neovim()
    install_python()
    install_javascript()
    python_editing()
    install_aws()

    if not config.check:
        add_job(init_git())
        command('sudo apt update')

    for manager in all_managers.values():
        add_job(manager.update(), run_on_dry=True)
    await run_tasks()
    # if config.check:
    #     await Pip.check()


if __name__ == '__main__':
    asyncio.run(main())
