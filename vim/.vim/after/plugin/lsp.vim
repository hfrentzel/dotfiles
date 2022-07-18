if has('nvim')
    finish
endif

function! CloseAndExpand() abort
   call asyncomplete#close_popup()
   return "\<C-R>=UltiSnips#ExpandSnippet()\<cr>"
endfunction

inoremap <expr> <silent> <Tab> pumvisible() ? "\<C-n>" : "\<C-R>=UltiSnips#ExpandSnippetOrJump()\<cr>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <expr> <silent> <cr> pumvisible() ? CloseAndExpand() : "\<cr>"
