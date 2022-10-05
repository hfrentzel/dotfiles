vim.g.CommandTCancelMap = { '<esc>', '<C-c>'}

vim.keymap.set('n', 'gb', '<Plug>(CommandTBuffer)', { remap = true})
vim.keymap.set('n', '<leader>t', '<Plug>(CommandTRipgrep)', { remap = true})
vim.keymap.set('n', '<leader>h', '<Plug>(CommandTHelp)', { remap = true})

require('wincent.commandt').setup({
    always_show_dot_files = true,
    height = 30,
    mappings = {
        i = {
            ['<C-\\>'] = 'open_vsplit',
        }
    }
})
