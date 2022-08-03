import os
import subprocess

from setup_tools.symlink import add_symlink
from setup_tools.installers import install_linux_package, pip_install
from vim import install_neovim


if __name__ == '__main__':
    dotfiles_home = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dotfiles_home)

    print('Initializing submodules...')
    subprocess.run(['git', 'submodule', 'init'], capture_output=True)
    print('Updating submodules...')
    subprocess.run(['git', 'submodule', 'update'], capture_output=True)

    install_neovim()

    add_symlink(f'{dotfiles_home}/vim/.vimrc', '~/.vimrc')
    add_symlink(f'{dotfiles_home}/vim/.vim', '~/.vim')
    add_symlink(f'{dotfiles_home}/vim/.config/nvim/init.vim', '~/.config/nvim/init.vim')

    # pylsp setup
    install_linux_package('python3-pip')
    pip_install('python-lsp-server')

    # command-t
    install_linux_package('ruby')
    install_linux_package('ruby-dev')
    print('Installing neovim gem...')
    subprocess.run(['sudo', 'gem', 'install', 'neovim'], capture_output=True)
    os.chdir(f'{dotfiles_home}/vim/.vim/pack/vendor/opt/command-t/ruby/command-t/ext/command-t')
    subprocess.run(['ruby', 'extconf.rb'], capture_output=True)
    subprocess.run(['make'], capture_output=True)
