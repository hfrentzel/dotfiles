-- lsp.lua
-- Configure LSPs

local format = function()
    require('conform').format({ async = true, lsp_fallback = true })
end

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
    {
        'nvim-lspconfig',
        dir = '~/.config/nvim/pack/vendor/opt/nvim-lspconfig',
        event = { 'BufReadPre', 'BufNewFile' },
        config = function()
            local diags_on = true
            local toggleDiagnostics = function()
                if diags_on then
                    diags_on = false
                    vim.diagnostic.hide()
                    vim.lsp.handlers['textDocument/publishDiagnostics'] = vim.lsp.with(
                        vim.lsp.diagnostic.on_publish_diagnostics,
                        { virtual_text = false, underline = false, signs = false }
                    )
                else
                    diags_on = true
                    vim.diagnostic.show(
                        nil,
                        nil,
                        nil,
                        { virtual_text = true, underline = true, signs = true }
                    )
                    vim.lsp.handlers['textDocument/publishDiagnostics'] = vim.lsp.with(
                        vim.lsp.diagnostic.on_publish_diagnostics,
                        { virtual_text = true, underline = true, signs = true }
                    )
                end
            end

            local on_attach = function()
                local args = { buffer = true, silent = true }
                vim.diagnostic.config({ severity_sort = true })
                vim.wo.signcolumn = 'yes'
                vim.keymap.set('n', 'g=', format, args)
                vim.keymap.set('n', 'K', vim.lsp.buf.hover, args)
                vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, args)
                vim.keymap.set('n', ']d', vim.diagnostic.goto_next, args)
                vim.keymap.set('n', '<leader>d', vim.diagnostic.open_float, args)
                vim.keymap.set('n', '<leader>3', vim.diagnostic.setloclist, args)
                vim.keymap.set('n', '<leader>4', toggleDiagnostics, args)
            end

            local updateDiags = function()
                vim.diagnostic.setloclist({ open = false })
                vim.b['diagnostic_counts'] = {
                    error = vim.fn.len(vim.diagnostic.get(0, { severity = 1 })),
                    warning = vim.fn.len(vim.diagnostic.get(0, { severity = 2 })),
                    info = vim.fn.len(vim.diagnostic.get(0, { severity = 3 })),
                    hint = vim.fn.len(vim.diagnostic.get(0, { severity = 4 })),
                }
            end

            vim.api.nvim_create_augroup('diagnostics', { clear = true })
            vim.api.nvim_create_autocmd('DiagnosticChanged', {
                group = 'diagnostics',
                pattern = '*',
                callback = updateDiags,
            })

            local helpers = require('dot_helpers')
            local nvim_lsp = require('lspconfig')
            local capabilities = vim.lsp.protocol.make_client_capabilities()
            capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

            nvim_lsp.pylsp.setup({
                name = 'pylsp',
                on_attach = on_attach,
                before_init = require('my_lua.lsp.python').before_init,
                capabilities = capabilities,
                root_dir = function(_)
                    if vim.b['workspace'] then
                        return vim.b['workspace']
                    else
                        return helpers.get_git_root()
                    end
                end,
                settings = {
                    pylsp = {
                        plugins = {
                            jedi_rename = { enabled = false },
                            pylsp_mypy = { enabled = true },
                            pylint = { enabled = true },
                            ruff = {
                                enabled = true,
                                format = { 'I' },
                                unsafeFixes = true,
                            },
                            pylsp_rope = { rename = true },
                        },
                    },
                },
            })

            nvim_lsp.eslint.setup({
                on_attach = on_attach,
                capabilities = capabilities,
            })

            nvim_lsp.gopls.setup({
                on_attach = on_attach,
                capabilities = capabilities,
            })

            nvim_lsp.jsonls.setup({
                on_attach = on_attach,
                capabilities = capabilities,
            })

            nvim_lsp.rust_analyzer.setup({
                on_attach = on_attach,
                capabilities = capabilities,
                settings = {
                    ['rust-analyzer'] = {
                        check = {
                            command = 'clippy',
                        },
                    },
                },
            })

            nvim_lsp.tsserver.setup({
                on_attach = on_attach,
                capabilities = capabilities,
                filetypes = { 'typescript', 'typescriptreact', 'typescript.tsx' },
            })

            nvim_lsp.vimls.setup({
                on_attach = on_attach,
                capabilities = capabilities,
            })

            nvim_lsp.lua_ls.setup({
                on_attach = on_attach,
                capabilities = capabilities,
                settings = {
                    Lua = {
                        diagnostics = { globals = { 'vim' } },
                        runtime = {
                            path = vim.split(package.path, ';'),
                            version = 'LuaJIT',
                        },
                    },
                },
            })

            nvim_lsp.yamlls.setup({
                on_attach = on_attach,
                capabilities = capabilities,
                before_init = require('my_lua.lsp.yaml').before_init,
                settings = {
                    yaml = {
                        schemas = {},
                    },
                },
            })
        end,
    },
}
