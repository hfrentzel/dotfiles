-- lsp.lua
-- Configure LSPs

return {
    {
        'dressing.nvim',
        dir = '~/.config/nvim/pack/vendor/opt/dressing.nvim',
        keys = {
            { '<leader>r', vim.lsp.buf.rename },
            { '<leader>a', vim.lsp.buf.code_action },
        },
        opts = {
            input = { mappings = { i = { ['<Esc>'] = 'Close' } } },
            select = {
                backend = { 'builtin' },
                builtin = { relative = 'cursor' },
            },
        },
    },
    {
        'conform.nvim',
        dir = '~/.config/nvim/pack/vendor/opt/conform.nvim',
        ft = { 'lua' },
        opts = {
            formatters_by_ft = {
                lua = { 'stylua' },
            },
        },
    },
    {
        'nvim-lint',
        dir = '~/.config/nvim/pack/vendor/opt/nvim-lint',
        ft = { 'lua' },
        config = function()
            local lint = require('lint')
            lint.linters_by_ft = {
                lua = { 'selene' },
            }
            local timer = vim.uv.new_timer()
            vim.api.nvim_create_autocmd({ 'TextChanged', 'TextChangedI', 'BufReadPost' }, {
                pattern = { '*.lua' },
                group = vim.api.nvim_create_augroup('nvim-lint', { clear = true }),
                callback = function()
                    timer:start(100, 0, function()
                        timer:stop()
                        vim.schedule_wrap(lint.try_lint)()
                    end)
                end,
            })
        end,
    },
}
