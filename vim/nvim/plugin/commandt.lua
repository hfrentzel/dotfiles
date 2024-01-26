local has_commandt, commandt = pcall(require, 'wincent.commandt')
if not has_commandt then
    return
end
vim.g.CommandTCancelMap = { '<esc>', '<C-c>'}

vim.keymap.set('n', '<leader>b', '<Plug>(CommandTBuffer)')
vim.keymap.set('n', '<leader>t', '<Plug>(CommandTRipgrep)')
vim.keymap.set('n', '<leader>h', '<Plug>(CommandTHelp)')

commandt.setup({
    always_show_dot_files = true,
    height = 30,
    mappings = {
        i = {
            ['<C-\\>'] = 'open_vsplit',
        }
    }
})
