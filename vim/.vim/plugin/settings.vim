set nobackup
set nowritebackup
set noswapfile
set backupdir=~/.temp/backups//
set backupdir+=.
set directory=~/.temp/swaps//
set directory+=.


set backspace=indent,eol,start          " Normal backspacing
set expandtab                           " Always uses spaces over tabs
set shiftwidth=4                        " Spaces per tab
set tabstop=4                           " Spaces per tab
set autoindent                          " maintain indent on new line

if has('vertsplit')
    set splitright                      " Open splits to the right
endif
if has('windows')
    set splitbelow                      " Open splits below
endif

if has('folding')
    set foldlevelstart=99               " Start unfolded
endif

