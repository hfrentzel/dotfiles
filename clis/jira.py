from setup_tools.managers import Tar


def install_jira():
    Tar(command='jira', version='1.3.0',
        url='https://github.com/ankitpokhrel/jira-cli/releases/download/v{version}/jira_{version}_linux_x86_64.tar.gz',
        version_check="jira version | head -1 | grep -o '[0-9\\.]\\+' | head -1")
