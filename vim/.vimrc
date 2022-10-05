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

set scrolloff=3

set relativenumber
set number

let mapleader = ","
let g:camelcasemotion_key = '<leader>'

" <c-_> maps <c-/> functions like other editors
let g:tcomment_mapleader1 = ''
let g:tcomment_mapleader2 = ''
let g:tcomment_mapleader_comment_anyway = ''
let g:tcomment_textobject_inlinecomment = ''
nnoremap <c-_> :TComment<cr>
vnoremap <c-_> :TCommentMaybeInline<cr>

" Copy to system clipboard
if !empty($IS_WSL)
    vnoremap <silent> <C-c> "+y:call system("clip.exe", getreg("+"))<CR>
    vnoremap <silent> <RightMouse> "+y:call system("clip.exe", getreg("+"))<CR>
endif

nnoremap <leader>n :set rnu!<cr>
nnoremap <leader>1 :NERDTreeFocus<cr>

if has('mouse')
    set mouse=a
    if !has('nvim')
        set ttymouse=xterm2
    endif
endif

" Easier window movement
nnoremap <C-H> <C-W>h
nnoremap <C-J> <C-W>j
nnoremap <C-K> <C-W>k
nnoremap <C-L> <C-W>l

nnoremap gb :ls<CR>:b<Space>

" Open current fold and only current fold
nnoremap zB zMzO

nmap <leader>z :call <SID>SynStack()<CR>
function! <SID>SynStack()
    if !exists("*synstack")
        return
    endif
    echo map(synstack(line('.'), col('.')), 'synIDattr(v:val, "name")')
endfunction

" UPPERCASE word
nnoremap U mzviwUe`z
inoremap <c-u> <esc>viwUea

" Add relative line movements to jump list
nnoremap <expr> k (v:count > 5 ? "m'" . v:count : '') . 'k'
nnoremap <expr> j (v:count > 5 ? "m'" . v:count : '') . 'j'

command -range=% Fnl :<line1>,<line2>s/\\n/\r/g
command Fjson :%!jq . -
command -bar PyToJson :silent %s/$\n//eg | silent s/'/"/eg | s/True/true/eg | s/False/false/eg | %!jq . -

" Local overrides
let s:vimrc_local=$HOME . '/.vimrc.local'
if filereadable(s:vimrc_local)
    execute 'source ' . s:vimrc_local
endif

let base16colorspace=256

if has('packages')
    packadd! CamelCaseMotion
    packadd! base16-vim
    packadd! command-t
    packadd! fugitive
    packadd! nerdtree
    packadd! vim-surround
    packadd! vim-tmux-navigator
endif

hi QuickFixLine ctermbg=DarkGray

filetype plugin indent on
syntax on
