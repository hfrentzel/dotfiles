set nobackup
set nowritebackup
set noswapfile
set backupdir=~/.temp/backups//
set backupdir+=.
set directory=~/.temp/swaps//
set directory+=.
set diffopt+=linematch:60


set backspace=indent,eol,start          " Normal backspacing
set autoindent                          " maintain indent on new line
set textwidth=80
set formatoptions-=t                    " Don't autowrap text
set termguicolors

if has('nvim')
    set fillchars=eob:\ 
    set fillchars+=vert:┃ " U+2503
endif

set switchbuf=usetab

if has('vertsplit')
    set splitright                      " Open splits to the right
endif

if has('windows')
    set splitbelow                      " Open splits below
endif

if has('folding')
    set foldlevelstart=99               " Start unfolded
endif

