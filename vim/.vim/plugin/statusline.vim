function! StandardStatusLine() abort
    set laststatus=2
    set statusline=%F
    set statusline+=\ %y

    set statusline+=%=
    set statusline+=%l
    set statusline+=/
    set statusline+=%L
    set statusline+=,
    set statusline+=\ %c
endfunction

function! SetEsStatusLine() abort
        
    set laststatus=2
    set statusline=%F
    set statusline+=\ %y

    set statusline+=\ %{GetEnv()}

    set statusline+=%=
    set statusline+=%l
    set statusline+=/
    set statusline+=%L
    set statusline+=,
    set statusline+=\ %c

endfunction

function! GetEnv() abort
    if exists('g:VimKib#currentEnv')
        return '--' . toupper(g:VimKib#currentEnv) . '--'
    endif
    return 'No Cluster Set'
endfunction

call StandardStatusLine()
augroup FileTypes
    autocmd!
    autocmd filetype * call StandardStatusLine()
    autocmd filetype elasticsearch call SetEsStatusLine()
augroup END
