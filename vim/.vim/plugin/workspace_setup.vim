let s:filename = expand('~/workspaces')
if !filereadable(s:filename)
    finish
endif

let g:workspaces = {}
for line in readfile(s:filename)
    let s:array = split(line)
    if len(s:array) < 2 | continue | endif
    let g:workspaces[s:array[0]] = s:array[1]
endfor

for workspace in items(g:workspaces)
    execute "command Cd".workspace[0]." :cd ".workspace[1]
endfor
