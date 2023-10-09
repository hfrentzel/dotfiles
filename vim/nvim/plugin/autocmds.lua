local focus = require('my_lua.focus')

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
