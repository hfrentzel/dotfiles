from setup_tools.managers import Tar


def install_gh():
    Tar(command='gh', version='2.23.0',
        url='https://github.com/cli/cli/releases/download/v{version}/gh_{version}_linux_amd64.tar.gz',
        version_check="gh version | head -1 | grep -o '[0-9\\.]\\+' | head -1")
