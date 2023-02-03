from setup_tools.managers import Npm, Deb, Symlink


def install_neovim():
    Symlink('DOTROOT/vim/.vimrc', '~/.vimrc')
    Symlink('DOTROOT/vim/.vim', '~/.vim')
    Symlink('DOTROOT/vim/.config/nvim/init.vim', '~/.config/nvim/init.vim')

    Deb(command="nvim",
        url="https://github.com/neovim/neovim/releases/download/v{version}/nvim-linux64.deb",
        version="0.8.2"
        )
    Npm('vim-language-server', '2.3.0')


# TODO handle new command-t installation
def install_command_t():
    pass
