from setup_tools.installers import install_linux_package, pip_install, async_proc
from setup_tools.symlink import symlink
from setup_tools.linux import linux_package


def install_python():
    linux_package('python3.9', 'deadsnakes/ppa')

    # create_action('pyAlt', async_proc('sudo update-alternatives --install '
    #                                   '/usr/bin/python python /usr/bin/python3.9 2'))
    # create_action('pip', install_linux_package('python3-pip'), ['pyAlt'])


# def python_editing():
#     create_action('pylsp', pip_install('python-lsp-server'), ['pip'])
#     create_action('flake8', pip_install('flake8'), ['pip'])
#     create_action('pylint', pip_install('pylint'), ['pip'])
#     create_action('mypy', pip_install('pylsp-mypy'), ['pip'])
#
#     symlink('DOTROOT/languages/python/.pylintrc', '~/.pylintrc')
