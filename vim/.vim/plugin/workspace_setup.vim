let s:filename = expand('~/workspaces')
if !filereadable(s:filename)
    finish
endif

let g:workspaces = {}
for line in readfile(s:filename)
    let s:array = split(line)
    if len(s:array) < 2 | continue | endif
    let g:workspaces[s:array[1]] = s:array[0]
endfor

for workspace in items(g:workspaces)
    execute "command Cd".workspace[1]." :cd ".workspace[0]
endfor

function s:set_workspace() abort
    let filename = expand('%:p')
    let g:workspace_regex = join(keys(g:workspaces), '|')
    for directory in (keys(g:workspaces)->sort({i1, i2 -> len(i2) - len(i1)}))
        if stridx(filename, directory) > -1
            let b:workspace = directory
            break
        endif
    endfor
endfunction

augroup workspaces
    autocmd BufReadPre * call s:set_workspace()
augroup END
