-- windows.lua
-- Keymaps for navigating and managing windows and panes, interoperate with
-- tmux using tmux.nvim

return {
    {
        'tmux.nvim',
        dir = '~/.config/nvim/pack/vendor/opt/tmux.nvim',
        keys = {
            '<C-h>',
            '<C-j>',
            '<C-k>',
            '<C-l>',
            '<M-Up>',
            '<M-Down>',
            '<M-Left>',
            '<M-Right>',
        },
        config = function()
            local tmux = require('tmux')
            tmux.setup({
                copy_sync = {
                    enable = false,
                },
                navigation = {
                    cycle_navigation = false,
                    enable_default_keybindings = true,
                    persist_zoom = true,
                },
                resize = {
                    enable_default_keybindings = false,
                    resize_step_x = 1,
                    resize_step_y = 1,
                },
            })
            vim.keymap.set('n', '<m-right>', tmux.resize_right)
            vim.keymap.set('n', '<m-up>', tmux.resize_top)
            vim.keymap.set('n', '<m-left>', tmux.resize_left)
            vim.keymap.set('n', '<m-down>', tmux.resize_bottom)
        end,
    },
}
