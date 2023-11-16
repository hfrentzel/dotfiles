from setup2 import Exe


def install_terraform():
    Exe('terraform', '1.6.4', installers=['Zip'],
        url='https://releases.hashicorp.com/terraform/{version}/terraform_{version}_linux_amd64.zip')
    Exe('terraform-ls', '0.30.1', installers=['Zip'],
        url='https://releases.hashicorp.com/terraform-ls/{version}/terraform-ls_{version}_linux_amd64.zip')
