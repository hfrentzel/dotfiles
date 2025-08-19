-- windows.lua
-- Keymaps for navigating and managing windows and panes, interoperate with
-- wezterm and tmux using smart-splits.nvim

return {
    {
        'smart-splits.nvim',
        dev = true,
        config = function()
            local splits = require('smart-splits')
            splits.setup({
                at_edge = 'stop',
            })
            vim.keymap.set('n', '<C-h>', splits.move_cursor_left)
            vim.keymap.set('n', '<C-j>', splits.move_cursor_down)
            vim.keymap.set('n', '<C-k>', splits.move_cursor_up)
            vim.keymap.set('n', '<C-l>', splits.move_cursor_right)

            vim.keymap.set('n', '<M-h>', splits.resize_left)
            vim.keymap.set('n', '<M-j>', splits.resize_down)
            vim.keymap.set('n', '<M-k>', splits.resize_up)
            vim.keymap.set('n', '<M-l>', splits.resize_right)

            vim.keymap.set('n', '<leader><leader>h', splits.swap_buf_left)
            vim.keymap.set('n', '<leader><leader>j', splits.swap_buf_down)
            vim.keymap.set('n', '<leader><leader>k', splits.swap_buf_up)
            vim.keymap.set('n', '<leader><leader>l', splits.swap_buf_right)
        end,
    },
}
