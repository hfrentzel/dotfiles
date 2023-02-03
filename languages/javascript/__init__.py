from setup_tools.managers import Npm, Tar


def install_javascript():
    Tar(command='node', version='18.13.0',
        url='https://nodejs.org/dist/v{version}/node-v{version}-linux-x64.tar.xz')

    Npm('eslint', '8.32.0')
    Npm('typescript', '4.9.4')
    Npm('typescript-language-server', '3.0.2')
    Npm('vscode-langservers-extracted', '4.5.0')
