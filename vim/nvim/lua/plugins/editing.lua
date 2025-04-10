-- editing.lua
-- Shortcuts and features designed to speed up text editing and manipulation
-- Currently includes vim-surround and CamelCaseMotion

return {
    {
        'vim-sleuth',
        dev = true,
        init = function()
            vim.o.expandtab = true
            vim.o.shiftwidth = 4
            vim.o.tabstop = 4
        end,
    },
    {
        'vim-surround',
        dev = true,
        event = 'VeryLazy',
    },
    {
        'CamelCaseMotion',
        dev = true,
        keys = {
            { 'i<leader>w', '<Plug>CamelCaseMotion_iw', mode = { 'o', 'x' } },
        },
    },
}
