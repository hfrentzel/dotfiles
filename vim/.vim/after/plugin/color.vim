let g:base16_shell_path=expand('~/.bash/base16-shell/scripts')

function s:setColor()
    if !has('termguicolors')
        let g:base16colorspace=256
    endif

    let s:color_file = expand('~/.base16')

    if filereadable(s:color_file)
        let s:scheme = readfile(s:color_file, '', 1)

        if filereadable(expand('~/.vim/pack/vendor/opt/base16-vim/colors/base16-' . s:scheme[0] . '.vim'))
            execute 'color base16-' . s:scheme[0]
        else
            echoerr 'Bad scheme ' . s:scheme[0]
        endif
    endif
endfunction

augroup TermColor
    autocmd!
    autocmd FocusGained * call s:setColor()
augroup END

call s:setColor()
