from setup_tools.installers import install_linux_package, pip_install
from setup_tools.symlink import add_symlink
from main import create_action


def install_python(dotfiles_home):
    create_action('pip', install_linux_package('python3-pip'), ['apt_update'])

    create_action('pylsp', pip_install('python-lsp-server'), ['pip'])
    create_action('flake8', pip_install('flake8'), ['pip'])
    create_action('pylint', pip_install('pylint'), ['pip'])
    create_action('mypy', pip_install('pylsp-mypy'), ['pip'])

    add_symlink(f'{dotfiles_home}/languages/python/.pylintrc', '~/.pylintrc')
