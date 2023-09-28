" Cursor settings for vanilla vim
if !has('nvim')
    let &t_SI.="\e[5 q" "SI = INSERT mode
    let &t_SR.="\e[4 q" "SR = REPLACE mode
    let &t_EI.="\e[1 q" "EI = NORMAL mode (ELSE)
    autocmd VimLeave * silent !echo -ne "\e[5 q"
    autocmd VimEnter * silent !echo -ne "\e[1 q"

    set ttyfast
    set ttymouse=xterm2
    set viminfofile=~/.local/state/vim/viminfo
endif

if has('mouse')
    set mouse=a
endif

set noerrorbells
set number
set relativenumber
set scrolloff=3
set ttimeout
set ttimeoutlen=1
set visualbell

let base16colorspace=256
let mapleader = ","

let g:slime_no_mappings = 1
let g:slime_paste_file = tempname()
xmap <leader><enter> <Plug>SlimeRegionSend
nmap <leader><enter> <Plug>SlimeParagraphSend
let g:slime_target = 'tmux'
let g:slime_default_config = {'socket_name': 'default',
                            \ 'target_pane': '{right-of}' }

" <c-_> maps <c-/> functions like other editors
let g:tcomment_mapleader1 = ''
let g:tcomment_mapleader2 = ''
let g:tcomment_mapleader_comment_anyway = ''
let g:tcomment_textobject_inlinecomment = ''
nnoremap <silent> <c-_> :TComment<cr>
vnoremap <silent> <c-_> :TCommentMaybeInline<cr>

" Copy to system clipboard
if !empty($IS_WSL)
    vnoremap <silent> <C-c> "+y:call system("clip.exe", getreg("+"))<CR>
    vnoremap <silent> <RightMouse> "+y:call system("clip.exe", getreg("+"))<CR>
endif

nnoremap <leader>n :set rnu!<cr>

" Open current fold and only current fold
nnoremap zB zMzO

" Navigate while in insert mode
inoremap <c-h> <left>
inoremap <c-j> <down>
inoremap <c-k> <up>
inoremap <c-l> <right>

" Easier window movement
nnoremap <C-H> <C-W>h
nnoremap <C-J> <C-W>j
nnoremap <C-K> <C-W>k
nnoremap <C-L> <C-W>l

" Quicker buffer selection. This gets mapped to CommandTBuffer in nvim
nnoremap <leader>b :ls<CR>:b<Space>

" UPPERCASE word
nnoremap U mzviwUe`z
inoremap <c-u> <esc>viwUea

" Entire File text object
onoremap <silent> ae :<C-U>normal! ggVG<CR>
xnoremap <silent> ae :<C-U>normal! ggVG<CR>

" Add relative line movements to jump list
nnoremap <expr> k (v:count > 5 ? "m'" . v:count : '') . 'k'
nnoremap <expr> j (v:count > 5 ? "m'" . v:count : '') . 'j'

" Debug Syntax highlighting
nmap <leader>z :call <SID>SynStack()<CR>
function! <SID>SynStack()
    if !exists("*synstack")
        return
    endif
    echo map(synstack(line('.'), col('.')), 'synIDattr(v:val, "name")')
endfunction

" Commands for formatting Json and tracebacks
command -range=% Fnl :<line1>,<line2>s/\\n/\r/g
command Fjson :%!jq . -
command -bar PyToJson :silent %s/$\n//eg | silent s/'/"/eg | s/True/true/eg | s/False/false/eg | s/None/null/eg | %!jq . -

" Local overrides
let s:vimrc_local=expand('~/.vimrc.local')
if filereadable(s:vimrc_local)
    execute 'source ' . s:vimrc_local
endif

if has('packages')
    packadd! CamelCaseMotion
    packadd! base16-vim
    packadd! fugitive
    packadd! eunuch
    packadd! vim-slime
    packadd! vim-surround
    packadd! vim-visual-multi
    if !has('nvim')
        packadd! vim-tmux-navigator
    endif
endif

omap <silent> <leader>iw <Plug>CamelCaseMotion_iw
xmap <silent> <leader>iw <Plug>CamelCaseMotion_iw

filetype plugin indent on
syntax on
