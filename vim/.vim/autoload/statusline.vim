function statusline#NumErrors() abort
    if !exists('b:diagnostic_counts')
        return ""
    endif
    if b:diagnostic_counts['error'] > 0
        return "E ".b:diagnostic_counts['error']." "
    endif
    return ""
endfunction

function! statusline#NumWarnings() abort
    if !exists('b:diagnostic_counts')
        return ""
    endif
    if b:diagnostic_counts['warning'] > 0
        return "W ".b:diagnostic_counts['warning']." "
    endif
    return ""
endfunction

"Current Row/TotalRows CurrentCol
function! statusline#rhs() abort
    let l:line=''
    let l:line.=line('.')
    let l:line.='/'
    let l:line.=line('$')
    let l:line.=', '
    let l:line.=virtcol('.')
    return l:line
endfunction
