from setup_tools.symlink import symlink
from setup_tools.linux import linux_package


def install_neovim():
    linux_package('neovim', 'ppa:neovim-ppa/stable')

    symlink('DOTROOT/vim/.vimrc', '~/.vimrc')
    symlink('DOTROOT/vim/.vim', '~/.vim')
    symlink('DOTROOT/vim/.config/nvim/init.vim', '~/.config/nvim/init.vim')

    # npm install -g vim-language-server


# TODO handle new command-t installation
def install_command_t():
    pass
