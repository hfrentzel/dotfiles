let g:base16_shell_path=expand('~/.config/bash/plugins/base16-shell/scripts')

function s:setColor()
    if !has('termguicolors')
        let g:base16colorspace=256
    endif

    let s:color_file = expand('~/.local/share/dotfiles/base16')

    if !filereadable(s:color_file)
        return
    endif

    let s:scheme = readfile(s:color_file, '', 1)

    if !filereadable(expand('~/.config/nvim/pack/vendor/opt/base16-vim/colors/base16-' . s:scheme[0] . '.vim'))
        echoerr 'Bad scheme ' . s:scheme[0]
    endif

    execute 'color base16-' . s:scheme[0]
    doautoall colorscheme
    execute 'highlight Comment ' . pinnacle#italicize('Comment')
    let l:bg = synIDattr(synIDtrans(hlID('StatusLine')), 'bg', 'cterm')

    highlight clear VertSplit
    highlight link VertSplit LineNr
    if has('nvim')
        let l:error = synIDattr(synIDtrans(hlID('DiagnosticError')), 'fg', 'cterm')
        execute 'highlight User1 ' . pinnacle#highlight({'fg': l:error, 'bg': bg})
        let l:warning = synIDattr(synIDtrans(hlID('DiagnosticWarn')), 'fg', 'cterm')
        execute 'highlight User2 ' . pinnacle#highlight({'fg': l:warning, 'bg': bg})
        execute 'highlight User3 ' . pinnacle#embolden('StatusLine')
    endif
endfunction

augroup TermColor
    autocmd!
    autocmd FocusGained * call s:setColor()
augroup END

call s:setColor()
