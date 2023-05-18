import asyncio
import os
import subprocess

from setup_tools.installers import async_proc, command
from setup_tools.managers import all_managers, Apt, Symlink
from setup_tools.config import config
from setup_tools.jobs import run_tasks, add_job, add_dependent_job, successful
from setup_tools.github import github
from vim import install_neovim
from languages.python import install_python, python_editing
from languages.javascript import javascript_editing, install_node
from languages.terraform import install_terraform
from clis.aws import install_aws
from clis.jira import install_jira
from clis.github import install_gh
from clis.fzf import fzf


async def init_git():
    print('Initializing submodules...')
    await async_proc('git submodule init')

    print('Updating submodules...')
    await async_proc('git submodule update')

    print('Submodules updated')
    successful.add('submodules')
    return True


def report():
    missing = False
    for manager in all_managers.values():
        if getattr(manager, 'requires', None):
            continue
        for item in manager.get_missing():
            missing = True
            print(f'{item[0].name} expected: {item[0].version}, current: '
                  f'{item[1]}')

    if not missing:
        print('All packages installed and up to date')


async def main():
    # config.dry_run = True
    # config.check = True
    config.sources_home = os.path.expanduser('~/.pack_sources')
    config.dotfiles_home = os.path.dirname(os.path.abspath(__file__))

    subprocess.run(['sudo', 'pwd'], capture_output=True, check=True)
    os.makedirs(config.sources_home, exist_ok=True)
    os.chdir(config.dotfiles_home)

    # Base tools
    Apt('dos2unix')
    Apt('jq')
    github('dandavison/delta', '0.15.1')
    github('BurntSushi/ripgrep', '13.0.0', name='rg')
    github('sharkdp/bat', 'v0.23.0')
    github('ajeetdsouza/zoxide', 'v0.9.0')
    fzf()
    Symlink('DOTROOT/bash/.bash', '~/.bash')
    Symlink('DOTROOT/bash/.bashrc', '~/.bashrc')
    Symlink('DOTROOT/bash/.inputrc', '~/.inputrc')
    Symlink('DOTROOT/configs/.rgrc', '~/.rgrc')
    Symlink('DOTROOT/configs/batconfig', '~/.config/bat/config')
    Symlink('DOTROOT/git/gitconfig', '~/.gitconfig')
    Symlink('DOTROOT/tmux/.tmux.conf', '~/.tmux.conf')
    Symlink('DOTROOT/tmux/.tmux', '~/.tmux')
    Symlink('DOTROOT/clis/completion/kubectl',
            '~/.local/share/bash-completion/completions/kubectl')

    # Additional components
    install_neovim()
    install_python()
    install_node()
    # javascript_editing()
    # python_editing()
    # install_terraform()

    # install_aws()
    # install_jira()
    # install_gh()

    if not config.check:
        add_job(init_git())

    for manager in all_managers.values():
        if getattr(manager, 'requires', None):
            add_dependent_job(manager.update(), manager.requires,
                    run_on_dry=True)
        else:
            add_job(manager.update(), run_on_dry=True)
    await run_tasks()
    report()
    # if config.check:
    #     await Pip.check()


if __name__ == '__main__':
    asyncio.run(main())
