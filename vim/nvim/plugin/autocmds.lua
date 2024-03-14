local focus = require('my_lua.focus')

vim.o.eventignore='FocusGained'
vim.api.nvim_create_augroup('firstunfocus', {clear = true})
vim.api.nvim_create_autocmd('FocusLost', {
    group = 'firstunfocus',
    pattern = '*',
    callback = function()
        vim.o.eventignore=''
        vim.api.nvim_del_augroup_by_name('firstunfocus')
    end
})

vim.api.nvim_create_augroup('focus', {clear = true})
vim.api.nvim_create_autocmd('FocusGained', {
    group = 'focus',
    pattern = '*',
    callback = focus.focus_window
})
vim.api.nvim_create_autocmd('FocusLost', {
    group = 'focus',
    pattern = '*',
    callback = focus.blur_window
})
vim.api.nvim_create_autocmd('WinEnter', {
    group = 'focus',
    pattern = '*',
    callback = focus.focus_window
})
vim.api.nvim_create_autocmd('WinLeave', {
    group = 'focus',
    pattern = '*',
    callback = focus.blur_window
})

focus.focus_window()
