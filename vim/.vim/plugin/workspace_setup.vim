let s:filename = expand('~/workspaces')
if !filereadable(s:filename)
    finish
endif

for line in readfile(s:filename)
    let s:array = split(line)
    if len(s:array) < 2 | continue | endif
    execute "command Cd".s:array[0]." :cd ".s:array[1]
endfor
