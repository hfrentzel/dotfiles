from setup_tools.installers import install_linux_package
from main import create_action


def rust_editing():
    create_action('rust', install_linux_package('rustc'))
