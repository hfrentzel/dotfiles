
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
    nmap <buffer> K <plug>(lsp-hover)
    inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
    inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
    inoremap <expr> <cr> pumvisible() ? asyncomplete#close_popup() : "\<cr>"
endfunction

" let g:lsp_settings = {
" \    'pylsp': {
" \        'workspace_config': {
" \            'pylsp': {
" \                'configurationSources': ['flake8'],
" \                'plugins': {
" \                    'flake8': {'maxLineLength': 120}
" \                }
" \            }
" \        }
" \     }
" \}

augroup lsp_install
    au!
    autocmd User lsp_buffer_enabled call s:on_lsp_buffer_enabled()
augroup END

