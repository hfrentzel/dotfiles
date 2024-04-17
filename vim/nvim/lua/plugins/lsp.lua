-- lsp.lua
-- Configure LSPs

return {
    {'nvim-lspconfig', dir = '~/.config/nvim/pack/vendor/opt/nvim-lspconfig',
        event = {'BufReadPre', 'BufNewFile'},
        config = function()
            local helpers = require('dot_helpers')

            local diags_on = true
            local toggleDiagnostics = function()
                if diags_on then
                    diags_on = false
                    vim.diagnostic.hide()
                    vim.lsp.handlers['textDocument/publishDiagnostics'] = vim.lsp.with(
                        vim.lsp.diagnostic.on_publish_diagnostics,
                            {virtual_text = false, underline = false, signs = false})
                else
                    diags_on = true
                    vim.diagnostic.show(nil, nil, nil,
                        {virtual_text = true, underline = true, signs = true})
                    vim.lsp.handlers['textDocument/publishDiagnostics'] = vim.lsp.with(
                        vim.lsp.diagnostic.on_publish_diagnostics,
                            {virtual_text = true, underline = true, signs = true})
                end
            end

            local on_attach = function ()
                vim.diagnostic.config({severity_sort = true})
                vim.wo.signcolumn = 'yes'
                vim.keymap.set('n', 'K', vim.lsp.buf.hover,
                    {buffer = true, silent = true})
                vim.keymap.set('n', 'gd', vim.lsp.buf.definition,
                    {buffer = true, silent = true})
                vim.keymap.set('n', '<leader>3', vim.diagnostic.setloclist,
                    {buffer = true, silent = true})
                vim.keymap.set('n', '[d', vim.diagnostic.goto_prev,
                    {buffer = true, silent = true})
                vim.keymap.set('n', ']d', vim.diagnostic.goto_next,
                    {buffer = true, silent = true})
                vim.keymap.set('n', '<leader>d', vim.diagnostic.open_float,
                    {buffer = true, silent = true})
                vim.keymap.set('n', '<leader>4', toggleDiagnostics,
                    {buffer = true, silent = true})
            end

            local py_before_init = function(_, config)
                local has_path, util = pcall (require, 'lspconfig/util')
                if not has_path then
                    return
                end
                local path = util.path

                local jedi_args = {} -- object
                local mypy_args = {"--namespace-packages"} -- array
                local pylint_args = {} -- array

                local venv_cfg = vim.fn.glob(path.join(config.root_dir, '*', 'pyvenv.cfg'))
                if venv_cfg ~= '' then
                    local venv_dir = path.dirname(venv_cfg)
                    jedi_args.environment = venv_dir
                    table.insert(mypy_args, "--python-executable")
                    table.insert(mypy_args, path.join(venv_dir, 'bin', 'python'))

                    local version = helpers.get_python_major_version(venv_cfg)
                    table.insert(mypy_args, "--python-version")
                    table.insert(mypy_args, version)
                    table.insert(pylint_args, '--py-version='..version)

                    local site_pkg_dir = vim.fn.glob(path.join(venv_dir, 'lib/*/site-packages/'))
                    if site_pkg_dir ~= '' then
                        table.insert(pylint_args, "--init-hook=\"import sys; sys.path.extend(['"
                            ..site_pkg_dir.."', '"..config.root_dir.."'])\"")
                    elseif config.root_dir then
                        table.insert(pylint_args, "--init-hook=\"import sys; sys.path.append('"
                            ..config.root_dir.."')\"")
                    end
                end

                table.insert(mypy_args, true) -- default args should also be passed in
                if next(jedi_args) ~= nil then
                    config.settings.pylsp.plugins.jedi = jedi_args
                end
                config.settings.pylsp.plugins.pylint.args = pylint_args
                config.settings.pylsp.plugins.pylsp_mypy.overrides = mypy_args
            end

            local yaml_before_init = function(_, config)
                local filename = vim.fn.expand('~/.config/vim/schemas.json')
                if vim.fn.filereadable(filename) == 0 then
                    return
                end
                local schema_file = io.open(filename)
                local schema_overrides = vim.fn.json_decode(schema_file:read('*a'))
                schema_file:close()

                config.settings.yaml.schemas = schema_overrides.all
                for dir, schemas in pairs(schema_overrides) do
                    if dir == config.root_dir then
                        config.settings.yaml.schemas =
                            vim.tbl_extend('force', config.settings.yaml.schemas, schemas)
                    end
                end
            end

            local nvim_lsp = require'lspconfig'
            local capabilities = vim.lsp.protocol.make_client_capabilities()
            capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

            nvim_lsp.pylsp.setup{
                name = 'pylsp',
                on_attach = on_attach,
                before_init = py_before_init,
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
                            flake8 = {enabled = true, maxLineLength = 120},
                            pycodestyle = {enabled = false},
                            pylsp_mypy = {enabled = true},
                            pyflakes = {enabled = false},
                            pylint = {enabled = true}
                        }
                    }
                },
            }

            nvim_lsp.gopls.setup({
                on_attach = on_attach,
                capabilities = capabilities,
            })

            nvim_lsp.rust_analyzer.setup({
                on_attach = on_attach,
                capabilities = capabilities,
            })

            nvim_lsp.eslint.setup({
                on_attach = on_attach,
                capabilities = capabilities,
            })

            nvim_lsp.jsonls.setup({
                on_attach = on_attach,
                capabilities = capabilities,
            })

            nvim_lsp.tsserver.setup({
                on_attach = on_attach,
                capabilities = capabilities,
                filetypes = { "typescript", "typescriptreact", "typescript.tsx" }
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
                        diagnostics = {
                            globals = {"vim"}
                        },
                        runtime = {
                            path = vim.split(package.path, ';'),
                            version = 'LuaJIT'
                        }
                    }
                }
            })

            nvim_lsp.yamlls.setup({
                on_attach = on_attach,
                capabilities = capabilities,
                before_init = yaml_before_init,
                settings = {
                    yaml = {
                        schemas = {}
                    }
                }
            })

            local updateDiags = function()
                vim.diagnostic.setloclist({open = false})
                vim.b['diagnostic_counts'] = {
                    error = vim.fn.len(vim.diagnostic.get(0, {severity = 1})),
                    warning = vim.fn.len(vim.diagnostic.get(0, {severity = 2})),
                    info = vim.fn.len(vim.diagnostic.get(0, {severity = 3})),
                    hint = vim.fn.len(vim.diagnostic.get(0, {severity = 4})),
                }
            end

            vim.api.nvim_create_augroup('diagnostics', {clear = true})
            vim.api.nvim_create_autocmd('DiagnosticChanged', {
                group = 'diagnostics',
                pattern = '*',
                callback = updateDiags
            })

        end
    }
}
