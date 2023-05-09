from setup_tools.managers import Npm, Symlink, Pip
from setup_tools.installers import command
from setup_tools.config import config
from setup_tools.github import github


def install_neovim():
    Symlink('DOTROOT/vim/.vimrc', '~/.vimrc')
    Symlink('DOTROOT/vim/.vim', '~/.vim')
    Symlink('DOTROOT/vim/.config/nvim/init.vim', '~/.config/nvim/init.vim')

    github('neovim/neovim', 'v0.8.2', name='nvim')
    Pip('pynvim', '0.4.3')
    Npm('vim-language-server', '2.3.0')

    command('make',
            cwd=f'{config.dotfiles_home}/vim/.vim/pack/vendor/opt/command-t/lua/wincent/commandt/lib',
            depends_on='submodules')

