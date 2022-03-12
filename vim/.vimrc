
let &t_SI.="\e[5 q" "SI = INSERT mode
let &t_SR.="\e[4 q" "SR = REPLACE mode
let &t_EI.="\e[1 q" "EI = NORMAL mode (ELSE)

set ttimeout
set ttimeoutlen=1
set ttyfast

autocmd VimLeave * silent !echo -ne "\e[5 q"
autocmd VimEnter * silent !echo -ne "\e[1 q"

set tabstop=4
set expandtab
set shiftwidth=4
set autoindent

set rnu
set number

set noerrorbells
set visualbell

let mapleader = ","
let g:camelcasemotion_key = '<leader>'

set scrolloff=3
nmap <leader>n :set rnu!<cr>

nnoremap <C-H> <C-W>h
nnoremap <C-L> <C-W>l
