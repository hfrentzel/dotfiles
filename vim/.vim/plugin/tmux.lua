require('tmux').setup({
    copy_sync = {
        enable = false
    },
    navigation = {
        cycle_navigation = false,
        enable_default_keybindings = true,
        persist_zoom = true
    },
    resize = {
        enable_default_keybindings = false,
        resize_step_x = 1,
        resize_step_y = 1,
    }
})
vim.keymap.set('n', '<c-right>', '<cmd>lua require("tmux").resize_right()<cr>')
vim.keymap.set('n', '<c-up>', '<cmd>lua require("tmux").resize_up()<cr>')
vim.keymap.set('n', '<c-left>', '<cmd>lua require("tmux").resize_left()<cr>')
vim.keymap.set('n', '<c-down>', '<cmd>lua require("tmux").resize_down()<cr>')
