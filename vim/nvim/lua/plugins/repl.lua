-- repl.lua
-- Implement REPL integration using vim-slime

return {
    {
        'vim-slime',
        dev = true,
        keys = {
            { '<leader><enter>', '<Plug>SlimeRegionSend', mode = 'x' },
            { '<leader><enter>', '<Plug>SlimeParagraphSend' },
        },
        init = function()
            vim.g.slime_no_mappings = 1
        end,
        config = function()
            vim.g.slime_paste_file = vim.fn.tempname()
            vim.g.slime_target = 'tmux'
            vim.g.slime_default_config = {
                socket_name = 'default',
                target_pane = '{right-of}',
            }
        end,
    },
}
