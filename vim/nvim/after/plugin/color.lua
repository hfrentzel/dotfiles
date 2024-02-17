local function setColor()
    local pinnacle = require('wincent.pinnacle')

    local color_file = vim.fn.expand('~/.local/share/dotfiles/base16')
    if vim.fn.filereadable(color_file) == 0 then
        return
    end

    local scheme = vim.fn.readfile(color_file, '', 1)
    local scheme_file = vim.fn.expand('~/.config/nvim/pack/vendor/opt/base16-vim/colors/base16-'..scheme[1]..'.vim')
    if vim.fn.filereadable(scheme_file) == 0 then
        vim.api.nvim_err_writeln('Bad scheme ' .. scheme[1])
    end

    vim.cmd.colorscheme('base16-'..scheme[1])
    vim.cmd.doautoall('colorscheme')
    pinnacle.merge('Comment', {italic = true})

    vim.cmd.highlight('clear VertSplit')
    vim.cmd.highlight('link VertSplit LineNr')

    local bg = pinnacle.dump('StatusLine')['bg']
    pinnacle.set('User1', {fg = pinnacle.fg('DiagnosticError'), bg = bg})
    pinnacle.set('User2', {fg = pinnacle.fg('DiagnosticWarn'), bg = bg})
    pinnacle.set('User3', pinnacle.embolden('StatusLine'))
end

vim.api.nvim_create_augroup('TermColor', {clear = true})
vim.api.nvim_create_autocmd('FocusGained', {
    group = 'TermColor',
    pattern = '*',
    callback = setColor
})

setColor()
