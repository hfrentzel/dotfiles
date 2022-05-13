let g:NERDTreeMinimalUI=1

let g:NERDTreeCreatePrefix='silent keepalt keepjumps'

nnoremap <silent> - :silent edit <C-R>=empty(expand('%')) ? '.' : expand('%:p:h')<CR><CR>

if has('autocmd')
    augroup vinegarOpen
        autocmd!
        autocmd User NERDTreeInit call autocmds#get_last_file()
    augroup END
endif
