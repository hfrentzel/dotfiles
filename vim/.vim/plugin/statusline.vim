function! StandardStatusLine() abort
    set laststatus=2
    set statusline=%F
    set statusline+=\ %y

    set statusline+=%=

    set statusline+=\ (%{get(b:,\"git_branch\",\"\")})\ 
    set statusline+=%{RHS()}
endfunction

function! SetEsStatusLine() abort
    set laststatus=2
    set statusline=%F
    set statusline+=\ %y

    set statusline+=\ %{GetEnv()}

    set statusline+=%=
    set statusline+=%{RHS()}
endfunction

function! RHS() abort
    let l:line=''
    let l:line.=line('.')
    let l:line.='/'
    let l:line.=line('$')
    let l:line.=', '
    let l:line.=virtcol('.')
    return l:line
endfunction


function! GetEnv() abort
    if exists('g:VimKib#currentEnv')
        return '--' . toupper(g:VimKib#currentEnv) . '--'
    endif
    return 'No Cluster Set'
endfunction

augroup gitbranch
    autocmd!
    autocmd BufEnter,FocusGained,BufWritePost * 
                \let b:git_branch = substitute(system("git branch --show-current"), "\n", "", "g")
augroup end

augroup FileTypes
    autocmd!
    autocmd filetype * call StandardStatusLine()
    autocmd filetype elasticsearch call SetEsStatusLine()
augroup END
