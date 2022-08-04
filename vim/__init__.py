import os

from setup_tools.installers import install_linux_package, async_proc
from setup_tools.symlink import add_symlink


async def install_neovim(dotfiles_home):
    await install_linux_package('neovim', 'ppa:neovim-ppa/stable')

    add_symlink(f'{dotfiles_home}/vim/.vimrc', '~/.vimrc')
    add_symlink(f'{dotfiles_home}/vim/.vim', '~/.vim')
    add_symlink(f'{dotfiles_home}/vim/.config/nvim/init.vim', '~/.config/nvim/init.vim')


async def install_command_t(dotfiles_home):
    print('Installing neovim gem...')
    await async_proc('sudo gem install neovim')
    os.chdir(f'{dotfiles_home}/vim/.vim/pack/vendor/opt/command-t/ruby/command-t/ext/command-t')
    await async_proc('ruby extconf.rb')
    await async_proc('make')
