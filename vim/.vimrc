
let &t_SI.="\e[5 q" "SI = INSERT mode
let &t_SR.="\e[4 q" "SR = REPLACE mode
let &t_EI.="\e[1 q" "EI = NORMAL mode (ELSE)

set ttimeout
set ttimeoutlen=1
set ttyfast

autocmd VimLeave * silent !echo -ne "\e[5 q"
autocmd VimEnter * silent !echo -ne "\e[1 q"

set noerrorbells
set visualbell

set tabstop=4
set expandtab
set shiftwidth=4
set autoindent
set splitright
set scrolloff=3

set relativenumber
set number

let mapleader = ","
let g:camelcasemotion_key = '<leader>'

" <c-_> maps <c-/> functions like other editors
let g:tcomment_mapleader1 = '<c-!>'
nnoremap <c-_> :TComment<cr>
vnoremap <c-_> :TCommentMaybeInline<cr>

nmap <leader>n :set rnu!<cr>

" Easier window movement
nnoremap <C-H> <C-W>h
nnoremap <C-L> <C-W>l

" UPPERCASE word
nnoremap <c-u> mzviwUe`z
inoremap <c-u> <esc>viwUea

nnoremap <leader>ev :vs ~/.vimrc<cr>

" Add relative line movements to jump list
nnoremap <expr> k (v:count > 5 ? "m'" . v:count : '') . 'k'
nnoremap <expr> j (v:count > 5 ? "m'" . v:count : '') . 'j'
