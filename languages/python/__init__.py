from setup_tools.installers import command
from setup_tools.managers import Pip, Apt, Symlink


def install_python():
    Apt('python3.9', 'deadsnakes/ppa')
    Apt('python3-pip')

    command('sudo update-alternatives --install '
            '/usr/bin/python python /usr/bin/python3.9 2',
            depends_on='python3.9', name='python')


def python_editing():
    Pip('flake8', '6.0.0')
    Pip('pylint', '2.15.4')
    Pip('pylsp-mypy', '0.6.5')
    Pip('python-lsp-server', '1.7.1')
    Pip('debugpy', '1.6.4')

    Symlink('DOTROOT/languages/python/.pylintrc', '~/.pylintrc')
