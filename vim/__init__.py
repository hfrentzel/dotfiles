from setup_tools.symlink import symlink
from setup_tools.deb import deb_package


def install_neovim():
    symlink('DOTROOT/vim/.vimrc', '~/.vimrc')
    symlink('DOTROOT/vim/.vim', '~/.vim')
    symlink('DOTROOT/vim/.config/nvim/init.vim', '~/.config/nvim/init.vim')

    # npm install -g vim-language-server
    src = {
        "command": "nvim",
        "url": "https://github.com/neovim/neovim/releases/download/v{version}/nvim-linux64.deb",
        "version_check": "nvim --version | head -1 | grep -o '[0-9\\.]\\+'",
        "version": "0.8.2"
    }
    deb_package(**src)


# TODO handle new command-t installation
def install_command_t():
    pass
