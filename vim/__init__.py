from setup_tools.managers import Npm, Deb, Symlink, Pip
from setup_tools.installers import command
from setup_tools.config import config


def install_neovim():
    Symlink('DOTROOT/vim/.vimrc', '~/.vimrc')
    Symlink('DOTROOT/vim/.vim', '~/.vim')
    Symlink('DOTROOT/vim/.config/nvim/init.vim', '~/.config/nvim/init.vim')

    Deb(command="nvim",
        url="https://github.com/neovim/neovim/releases/download/v{version}/nvim-linux64.deb",
        version="0.8.2"
        )
    Pip('pynvim', '0.4.3')
    Npm('vim-language-server', '2.3.0')

    command('make',
            cwd=f'{config.dotfiles_home}/vim/.vim/pack/vendor/opt/command-t/lua/wincent/commandt/lib',
            depends_on='submodules')

