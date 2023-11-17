from setup2 import Exe, Sym, Lib, Dir


def install_python():
    Exe('python3.9', installers=['Apt'])
    # Exe('python3-pip', installers=['Apt'])

    # command('sudo update-alternatives --install '
    #         '/usr/bin/python python /usr/bin/python3.9 2',
    #         depends_on='python3.9', name='python')


def python_editing():
    Exe('flake8', '6.0.0', installers=['Pip'])
    Exe('pylint', '2.15.4', installers=['Pip'])
    Exe('python-lsp-server', '1.7.1', command_name='pylsp', installers=['Pip'])
    Lib('pylsp-mypy', '0.6.5', 'pip')
    Lib('debugpy', '1.6.4', 'pip')

    Dir('python_data', '~/.local/share/python')  # for .python_history
    Sym('startup.py', 'DOT/languages/python/gen_startup.py', '~/.config/python/startup.py')
    Sym('pylintrc', 'DOT/languages/python/pylintrc', '~/.config/pylint/pylintrc')
