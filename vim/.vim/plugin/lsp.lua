local on_attach = function ()
    vim.keymap.set('n', 'K', "<cmd>lua vim.lsp.buf.hover()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', 'gd', "<cmd>lua vim.lsp.buf.definition()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', '<leader>3', "<cmd>lua vim.diagnostic.setloclist()<CR>", {buffer = true, silent = true})
end

local util = require('lspconfig/util')
local path = util.path

local py_before_init = function(params, config)
    local match = vim.fn.glob(path.join(config.root_dir, '*', 'pyvenv.cfg'))
    if match ~= '' then
        config.settings.pylsp.plugins.jedi.environment = path.dirname(match)
    end
end

require'lspconfig'.pylsp.setup{
    name = 'pylsp',
    on_attach = on_attach,
    before_init = py_before_init,
    root_dir = function(fname)
        if vim.g['workspaces'] then
            for _, directory in pairs(vim.g['workspaces']) do
                if vim.fn.stridx(fname, directory) > -1 then
                    return directory
                end
            end
        end
    end,
    settings = {
        pylsp = {
            plugins = {
                flake8 = {maxLineLength = 120},
                jedi = {environment = nil}
            }
        }
    },
}
