setlocal foldmethod=syntax
setlocal shiftwidth=2
setlocal tabstop=2

nnoremap <buffer> <leader>f :call vimKib#goToNextRequest()<cr>
nnoremap <buffer> <leader>F :call vimKib#goToPrevRequest()<cr>
