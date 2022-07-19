local on_attach = function ()
    vim.keymap.set('n', 'K', "<cmd>lua vim.lsp.buf.hover()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', 'gd', "<cmd>lua vim.lsp.buf.definition()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', '<leader>3', "<cmd>lua vim.diagnostic.setloclist()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', '[d', "<cmd>lua vim.diagnostic.goto_prev()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', ']d', "<cmd>lua vim.diagnostic.goto_next()<CR>", {buffer = true, silent = true})
end

local util = require('lspconfig/util')
local path = util.path

local py_before_init = function(params, config)
    local match = vim.fn.glob(path.join(config.root_dir, '*', 'pyvenv.cfg'))
    if match ~= '' then
        config.settings.pylsp.plugins.jedi = {environment = path.dirname(match)}
    end
end

require'lspconfig'.pylsp.setup{
    name = 'pylsp',
    on_attach = on_attach,
    before_init = py_before_init,
    root_dir = function(fname)
        if vim.b['workspace'] then
            return vim.b['workspace']
        end
    end,
    settings = {
        pylsp = {
            plugins = {
                pycodestyle = {enabled = false},
                pyflakes = {enabled = false},
                flake8 = {enabled = true, maxLineLength = 120}
            }
        }
    },
}

vim.cmd('augroup diagnostics')
vim.cmd('autocmd!')
vim.cmd('autocmd DiagnosticChanged * lua vim.diagnostic.setloclist({open = false})')
vim.cmd('augroup END')
    
