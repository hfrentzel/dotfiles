from setup_tools.installers import command
from setup_tools.pip import pip_package
from setup_tools.symlink import symlink
from setup_tools.linux import linux_package


def install_python():
    linux_package('python3.9', 'deadsnakes/ppa')
    linux_package('python3-pip')

    command('sudo update-alternatives --install '
            '/usr/bin/python python /usr/bin/python3.9 2',
            depends_on='python3.9')


def python_editing():
    pip_package('flake8', '6.0.0')
    pip_package('pylint', '2.15.4')
    pip_package('pylsp-mypy', '0.6.5')
    pip_package('python-lsp-server', '1.7.1')
    pip_package('debugpy', '1.6.4')

    symlink('DOTROOT/languages/python/.pylintrc', '~/.pylintrc')
