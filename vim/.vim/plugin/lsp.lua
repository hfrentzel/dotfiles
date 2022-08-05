local on_attach = function ()
    vim.wo.signcolumn = 'number'
    vim.keymap.set('n', 'K', "<cmd>lua vim.lsp.buf.hover()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', 'gd', "<cmd>lua vim.lsp.buf.definition()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', '<leader>3', "<cmd>lua vim.diagnostic.setloclist()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', '[d', "<cmd>lua vim.diagnostic.goto_prev()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', ']d', "<cmd>lua vim.diagnostic.goto_next()<CR>", {buffer = true, silent = true})
end

local util = require('lspconfig/util')
local path = util.path

local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities = require('cmp_nvim_lsp').update_capabilities(capabilities)



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
    capabilities = capabilities,
    root_dir = function(fname)
        if vim.b['workspace'] then
            return vim.b['workspace']
        end
    end,
    settings = {
        pylsp = {
            plugins = {
                flake8 = {enabled = true, maxLineLength = 120},
                pycodestyle = {enabled = false},
                pyflakes = {enabled = false},
                pylint = {enabled = true}
            }
        }
    },
}

_G.updateDiags = function()
    vim.diagnostic.setloclist({open = false})
    vim.b['diagnostic_counts'] = { 
        error = vim.fn.len(vim.diagnostic.get(0, {severity = 1})),
        warning = vim.fn.len(vim.diagnostic.get(0, {severity = 2})),
        info = vim.fn.len(vim.diagnostic.get(0, {severity = 3})),
        hint = vim.fn.len(vim.diagnostic.get(0, {severity = 4})),
    }
end


vim.cmd('augroup diagnostics')
vim.cmd('autocmd!')
vim.cmd('autocmd DiagnosticChanged * lua updateDiags()')
vim.cmd('augroup END')
    
