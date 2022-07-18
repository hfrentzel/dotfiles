if has('nvim')
    finish
endif
        "             'jedi': {'environment': lsp#utils#find_nearest_parent_file_directory(
        "                 lsp#utils#get_buffer_path(), ['venv/']).'/venv'
        "             }

if executable('pylsp') 
    " let g:lsp_experimental_workspace_folders = 1
    au User lsp_setup call lsp#register_server({
        \ 'name': 'pylsp',
        \ 'cmd': {server_info->['pylsp']},
        \ 'allowlist': ['python'],
        \ 'workspace_config': {
        \     'pylsp': {
        \         'plugins': {
        \             'flake8': {'maxLineLength': 120},
        \             'jedi': {'environment': lsp#utils#find_nearest_parent_file_directory(
        \                 lsp#utils#get_buffer_path(), ['venv/']).'/venv'
        \             }
        \         }
        \     }
        \ }
        \ })
    augroup change_lsp_venv
        au!
        autocmd BufEnter *.py call lsp#update_workspace_config('pylsp', {
            \ 'pylsp': {
            \     'plugins': {
            \         'flake8': {'maxLineLength': 120},
            \         'jedi': {'environment': lsp#utils#find_nearest_parent_file_directory(
            \             lsp#utils#get_buffer_path(), ['venv/']).'/venv'
            \ }}}})
    augroup END
endif

function! s:on_lsp_buffer_enabled() abort
    nmap <buffer> <leader>3 <plug>(lsp-document-diagnostics)
    nmap <buffer> gd <plug>(lsp-definition)
    nmap <buffer> K <plug>(lsp-hover)
endfunction

augroup lsp_install
    au!
    autocmd User lsp_buffer_enabled call s:on_lsp_buffer_enabled()
augroup END

let g:UltiSnipsExpandTrigger='<tab>'
let g:UltiSnipsJumpForwardTrigger='<tab>'
let g:UltiSnipsJumpBackwardTrigger='<S-Tab>'
let g:UltiSnipsSnippetDirectories=["UltiSnips"]
let g:UltiSnipsEditSplit="vertical"
call asyncomplete#register_source(asyncomplete#sources#ultisnips#get_source_options({
    \ 'name': 'ultisnips',
    \ 'allowlist': ['*'],
    \ 'completor': function('asyncomplete#sources#ultisnips#completor'),
    \ }))

let b:did_after_plugin_ultisnips_after = 1

