hi Folded  term=bold ctermfg=1 ctermbg=242

function! MyFoldText() abort
    return getline(v:foldstart)
endfunction
set foldtext=MyFoldText()
