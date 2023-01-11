from setup_tools.installers import pip_package, command
from setup_tools.symlink import symlink
from setup_tools.linux import linux_package


def install_python():
    linux_package('python3.9', 'deadsnakes/ppa')
    linux_package('python3-pip')

    command('sudo update-alternatives --install '
            '/usr/bin/python python /usr/bin/python3.9 2',
            depends_on='python3.9')


def python_editing():
    pip_package('flake8')
    pip_package('pylint')
    pip_package('pylsp-mypy')
    pip_package('python-lsp-server')
    pip_package('debugpy')

    symlink('DOTROOT/languages/python/.pylintrc', '~/.pylintrc')
