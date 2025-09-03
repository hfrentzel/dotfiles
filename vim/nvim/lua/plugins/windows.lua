-- windows.lua
-- Keymaps for navigating and managing windows and panes, interoperate with
-- wezterm and tmux using smart-splits.nvim

local directions = {
    left = "h",
    down = "j",
    up = "k",
    right = "l"
}

local function move_pane(dir)
    return function()
        local start_win = vim.fn.winnr()
        vim.cmd.wincmd(directions[dir])
        if vim.fn.winnr() == start_win then
            vim.fn.system({'wezterm', 'cli', 'activate-pane-direction', dir})
        end
    end
end

return {
    {
        'smart-splits.nvim',
        dev = true,
        config = function()
            local splits = require('smart-splits')
            splits.setup({
                at_edge = 'stop',
            })

            if vim.trim((vim.env.TERM_PROGRAM or ''):lower()) == 'wezterm' then
                vim.keymap.set('n', '<C-h>', move_pane("left"))
                vim.keymap.set('n', '<C-j>', move_pane("down"))
                vim.keymap.set('n', '<C-k>', move_pane("up"))
                vim.keymap.set('n', '<C-l>', move_pane("right"))
            else
                vim.keymap.set('n', '<C-h>', splits.move_cursor_left)
                vim.keymap.set('n', '<C-j>', splits.move_cursor_down)
                vim.keymap.set('n', '<C-k>', splits.move_cursor_up)
                vim.keymap.set('n', '<C-l>', splits.move_cursor_right)
            end

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
