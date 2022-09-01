vim.keymap.set('n', '<leader>t', '<Plug>(CommandTGit)', { remap = true})
vim.keymap.set('n', 'gb', '<Plug>(CommandTBuffer)', { remap = true})

require('wincent.commandt').setup({
    always_show_dot_files = true,
    height = 30
})
