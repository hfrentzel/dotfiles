from setup_tools.installers import install_linux_package


def install_neovim():
    install_linux_package('neovim', 'ppa:neovim-ppa/stable')
