function! StandardStatusLine() abort
    setlocal laststatus=2
    setlocal statusline=%{get(b:,\"adjusted_path\",\"\")}
    setlocal statusline+=%3*
    setlocal statusline+=%t
    setlocal statusline+=%*
    setlocal statusline+=\ %y

    setlocal statusline+=%=

    setlocal statusline+=%{statusline#NoErrors()}
    setlocal statusline+=%1*
    setlocal statusline+=%{statusline#NumErrors()}
    setlocal statusline+=%2*
    setlocal statusline+=%{statusline#NumWarnings()}
    setlocal statusline+=%*

    setlocal statusline+=\ (%{get(b:,\"git_branch\",\"\")})\ 
    setlocal statusline+=%{statusline#rhs()}
endfunction

function! SetEsStatusLine() abort
    setlocal laststatus=2
    setlocal statusline=%{get(b:,\"adjusted_path\",\"\")}
    setlocal statusline+=\ %y

    setlocal statusline+=\ %{GetEnv()}

    setlocal statusline+=%=
    setlocal statusline+=%{statusline#rhs()}
endfunction

function! GetEnv() abort
    if exists('g:vimKibCurrentEnv')
        return '--' . toupper(g:vimKibCurrentEnv) . '--'
    endif
    return 'No Cluster Set'
endfunction

function! GetGitData() "abort
    let l:git_prefix = 'git -C "'.expand('%:p:h').'"'

    if exists("b:workspace")
        let l:root_path = b:workspace
        let l:root_name = '~' . g:workspaces[b:workspace] . '~'
    endif

    let l:is_git_dir = trim(system(l:git_prefix.' rev-parse --is-inside-work-tree'))
    if l:is_git_dir is# 'true'
        let b:git_branch = substitute(system(l:git_prefix.' branch --show-current'), '\n', '', 'g')

        " Use repo root directory is not in a workspace
        if !exists("l:root_path")
            let l:root_path = substitute(system(l:git_prefix.' rev-parse --show-toplevel'), '\n', '', 'g')
            let l:root_name = '~' . split(l:root_path, '/')[-1] . '~'
        endif
    endif

    if exists("l:root_path")
        let b:adjusted_path = l:root_name . matchstr(expand('%:p:h'), l:root_path . '\zs.*\ze').'/'
    else
        let b:adjusted_path = expand('%:p:h').'/'
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
