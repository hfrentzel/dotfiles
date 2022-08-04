import os
import subprocess
import asyncio

from setup_tools.symlink import add_symlink
from setup_tools.installers import install_linux_package, pip_install, \
    async_proc
from vim import install_neovim


async def init_git():
    print('Initializing submodules...')
    await async_proc('git submodule init')

    print('Updating submodules...')
    await async_proc('git submodule update')

    print('Submodules updated')


async def install_command_t(dotfiles_home):
    print('Installing neovim gem...')
    await async_proc('sudo gem install neovim')
    os.chdir(f'{dotfiles_home}/vim/.vim/pack/vendor/opt/command-t/ruby/command-t/ext/command-t')
    await async_proc('ruby extconf.rb')
    await async_proc('make')


async def main():
    subprocess.run(['sudo', 'pwd'], capture_output=True)

    dotfiles_home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dotfiles_home)

    submods = asyncio.create_task(init_git())

    await async_proc('sudo apt update')
    pytho = asyncio.create_task(install_linux_package('python3-pip'))
    ruby = asyncio.create_task(install_linux_package('ruby'))
    ruby_dev = asyncio.create_task(install_linux_package('ruby-dev'))
    dos2unix = asyncio.create_task(install_linux_package('dos2unix'))
    neovim = asyncio.create_task(install_neovim())

    await pytho
    pylsp = asyncio.create_task(pip_install('python-lsp-server'))

    add_symlink(f'{dotfiles_home}/vim/.vimrc', '~/.vimrc')
    add_symlink(f'{dotfiles_home}/vim/.vim', '~/.vim')
    add_symlink(f'{dotfiles_home}/vim/.config/nvim/init.vim', '~/.config/nvim/init.vim')

    await ruby
    await ruby_dev
    await submods

    await install_command_t(dotfiles_home)

    await neovim
    await dos2unix
    await pylsp


if __name__ == '__main__':
    asyncio.run(main())
