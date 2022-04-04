
if executable('pylsp') 
    au User lsp_setup call lsp#register_server({
        \ 'name': 'pylsp',
        \ 'cmd': {server_info->['pylsp']},
        \ 'allowlist': ['python'],
        \ })
endif

function! s:on_lsp_buffer_enabled() abort
    nmap <buffer> K <plug>(lsp-hover)
endfunction

let g:lsp_settings = {
\    'pylsp': {
\        'workspace_config': {
\            'pylsp': {
\                'configurationSources': ['flake8']
\            }
\        }
\     }
\}

augroup lsp_install
    au!
    autocmd User lsp_buffer_enabled call s:on_lsp_buffer_enabled()
augroup END

set foldmethod=expr
            \ foldexpr=lsp#ui#vim#folding#foldexpr()
            \ foldtext=lsp#ui#vim#folding#foldtext()

hi link LspWarningHighlight Underlined
hi link LspErrorHighlight Underlined

