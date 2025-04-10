-- lsp.lua
-- Configure LSPs

return {
    {
        'dressing.nvim',
        dev = true,
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
        dev = true,
        ft = { 'lua', 'css' },
        opts = {
            default_format_opts = {
                lsp_format = 'fallback',
            },
            formatters_by_ft = {
                lua = { 'stylua' },
                css = { 'stylelint', lsp_format = 'first' },
            },
            formatters = {
                stylelint = {
                    prepend_args = {
                        '--config',
                        vim.fn.expand('~/.config/stylelint/stylelintrc.json'),
                    },
                },
            },
        },
    },
    {
        'nvim-lint',
        dev = true,
        ft = { 'lua', 'css' },
        config = function()
            local lint = require('lint')
            lint.linters_by_ft = {
                lua = { 'selene' },
                css = { 'stylelint' },
            }
            lint.linters.stylelint.args = {
                '--config',
                vim.fn.expand('~/.config/stylelint/stylelintrc.json'),
                '-f',
                'json',
                '--stdin',
                '--stdin-filename',
                function()
                    return vim.fn.expand('%:p')
                end,
            }
            local timer = vim.uv.new_timer()
            vim.api.nvim_create_autocmd({ 'TextChanged', 'TextChangedI', 'BufReadPost' }, {
                pattern = { '*.lua', '*.css' },
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
