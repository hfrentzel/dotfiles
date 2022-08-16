function! StandardStatusLine() abort
    setlocal laststatus=2
    setlocal statusline=%{get(b:,\"adjusted_path\",\"\")}
    setlocal statusline+=\ %y

    setlocal statusline+=%=

    setlocal statusline+=%1*
    setlocal statusline+=%{NumErrors()}
    setlocal statusline+=%2*
    setlocal statusline+=%{NumWarnings()}
    setlocal statusline+=%*

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

function! NumErrors() abort
    if !exists('b:diagnostic_counts')
        return ""
    endif
    if b:diagnostic_counts['error'] > 0
        return "E ".b:diagnostic_counts['error']." "
    endif
    return ""
endfunction

function! NumWarnings() abort
    if !exists('b:diagnostic_counts')
        return ""
    endif
    if b:diagnostic_counts['warning'] > 0
        return "W ".b:diagnostic_counts['warning']." "
    endif
    return ""
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
    if exists('g:vimKibCurrentEnv')
        return '--' . toupper(g:vimKibCurrentEnv) . '--'
    endif
    return 'No Cluster Set'
endfunction

function! GetGitData() abort
    let l:git_prefix = 'git -C "'.expand('%:p:h').'"'

    if exists("b:workspace")
        let l:root_path = b:workspace
        let l:root_name = '~' . g:workspaces[b:workspace] . '~'
    endif

    let l:is_git_dir = trim(system(l:git_prefix.' rev-parse --is-inside-work-tree'))
    if l:is_git_dir is# 'true'
        let b:git_branch = substitute(system(l:git_prefix.' branch --show-current'), '\n', '', 'g')
        if !exists("l:root_path")
            let l:root_path = substitute(system(l:git_prefix.' rev-parse --show-toplevel'), '\n', '', 'g')
            let l:root_name = '~' . split(l:root_path, '/')[-1] . '~'
        endif
    endif

    if exists("l:root_path")
        let b:adjusted_path = l:root_name . matchstr(expand('%:p'), l:root_path . '\zs.*\ze')
    else
        let b:adusted_path = expand('%:p')
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
