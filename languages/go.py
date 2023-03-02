from setup_tools.managers import Tar


def install_go():
    Tar(command='go', version='1.20',
        url='https://go.dev/dl/go{version}.linux-amd64.tar.gz',
        version_check="go version | head -1 | grep -o '[0-9\\.]\\+' | head -1")
