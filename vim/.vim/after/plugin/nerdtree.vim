let g:NERDTreeMinimalUI=1

let g:NERDTreeCreatePrefix='silent keepalt keepjumps'

nnoremap <silent> - :let g:currFile=expand('%')<CR>:silent edit <C-R>=empty(expand('%')) ? '.' : expand('%:p:h')<CR><CR>:let b:currFile = g:currFile<CR>

if has('autocmd')
    augroup vinegarOpen
        autocmd!
        autocmd User NERDTreeInit call autocmds#get_last_file()
    augroup END
endif

