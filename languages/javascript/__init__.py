from setup2 import Exe, Lib


def install_node():
    Exe('node', version='18.13.0', installers=['Tar'],
        url='https://nodejs.org/dist/v{version}/node-v{version}-linux-x64.tar.xz')


def javascript_editing():
    Lib('typescript', '4.9.4', 'npm')
    Exe('eslint', '8.32.0', installers=['Npm'])
    Exe('typescript-language-server', '3.0.2', installers=['Npm'])
    Exe('vscode-langservers-extracted', '4.5.0', installers=['Npm'],
        command_name='vscode-eslint-language-server')
