function! StandardStatusLine() abort
    setlocal laststatus=2
    setlocal statusline=%{get(b:,\"adjusted_path\",\"\")}
    setlocal statusline+=\ %y

    setlocal statusline+=%=

    setlocal statusline+=\ (%{get(b:,\"git_branch\",\"\")})\ 
    setlocal statusline+=%{RHS()}
endfunction

function! SetEsStatusLine() abort
    setlocal laststatus=2
    setlocal statusline=%{get(b:,\"adjusted_path\",\"\")}
    setlocal statusline+=\ %y

    setlocal statusline+=\ %{GetEnv()}

    setlocal statusline+=%=
    setlocal statusline+=%{RHS()}
endfunction

function! RHS() abort
    let l:line=''
    let l:line.=line('.')
    let l:line.='/'
    let l:line.=line('$')
    let l:line.=', '
    let l:line.=virtcol('.')
    return l:line
endfunction

function! GetEnv() abort
    if exists('g:VimKib#currentEnv')
        return '--' . toupper(g:VimKib#currentEnv) . '--'
    endif
    return 'No Cluster Set'
endfunction

function! GetGitData() abort
    let l:is_git_dir = trim(system('git rev-parse --is-inside-work-tree'))
    if l:is_git_dir is# 'true'
        let b:git_branch = substitute(system('git branch --show-current'), '\n', '', 'g')
        let l:git_root = substitute(system('git rev-parse --show-toplevel'), '\n', '', 'g')
        let l:root_name = '~' . split(l:git_root, '/')[-1] . '~'
        let b:adjusted_path = l:root_name . matchstr(expand('%:p'), l:git_root . '\zs.*\ze')
    endif
endfunction

augroup StatusLineData
    autocmd!
    autocmd BufEnter,FocusGained,BufWritePost * call GetGitData()
augroup end

augroup FileTypes
    autocmd!
    autocmd filetype * call StandardStatusLine()
    autocmd filetype elasticsearch call SetEsStatusLine()
augroup END
