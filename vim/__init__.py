from setup_tools.installers import install_linux_package


async def install_neovim():
    await install_linux_package('neovim', 'ppa:neovim-ppa/stable')
