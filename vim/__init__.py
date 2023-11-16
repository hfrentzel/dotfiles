from setup2 import Sym, Exe, Command, Lib

def install_neovim():
    Sym('vimrc', 'DOT/vim/vimrc', '~/.config/vim/vimrc')
    Sym('nvimconfig', 'DOT/vim/nvim', '~/.config/nvim')

    Exe('neovim', '0.8.2', installers=['Github'], repo='neovim/neovim', 
        command_name='nvim')

    Exe('vim-language-server', '2.3.0', installers=['Npm'])
    Lib('pynvim', '0.4.3', 'pip')
    Command('command-t', 'make',
            check_script='test -f commandt.so',
            cwd=f'DOT/vim/nvim/pack/vendor/opt/command-t/lua/wincent/commandt/lib',
            depends_on='submodules')

