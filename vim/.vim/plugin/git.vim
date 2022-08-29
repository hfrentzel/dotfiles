" https://github.com/tpope/vim-fugitive/issues/1474
function! s:BlameToggle() abort
    let found = 0
    for winnr in range(1, winnr('$'))
        if getbufvar(winbufnr(winnr), '&filetype') ==# 'fugitiveblame'
            exe winnr . 'close'
            let found = 1
        endif
    endfor
    if !found
        Git blame
    endif
endfunction

nmap <silent> <c-b> :call <SID>BlameToggle()<CR>
