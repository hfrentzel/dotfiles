local path = require('lspconfig/util').path
local helpers = require('dot_helpers')

local diags_on = true
toggleDiagnostics = function()
    if diags_on then
        vim.diagnostic.hide()
        diags_on = false
    else
        vim.diagnostic.show()
        diags_on = true
    end
end

local on_attach = function ()
    vim.wo.signcolumn = 'yes'
    vim.keymap.set('n', 'K', "<cmd>lua vim.lsp.buf.hover()<CR>", 
        {buffer = true, silent = true})
    vim.keymap.set('n', 'gd', "<cmd>lua vim.lsp.buf.definition()<CR>", 
        {buffer = true, silent = true})
    vim.keymap.set('n', '<leader>3', "<cmd>lua vim.diagnostic.setloclist()<CR>", 
        {buffer = true, silent = true})
    vim.keymap.set('n', '[d', "<cmd>lua vim.diagnostic.goto_prev()<CR>", 
        {buffer = true, silent = true})
    vim.keymap.set('n', ']d', "<cmd>lua vim.diagnostic.goto_next()<CR>", 
        {buffer = true, silent = true})
    vim.keymap.set('n', '<leader>d', "<cmd>lua vim.diagnostic.open_float()<CR>", 
        {buffer = true, silent = true})
    vim.keymap.set('n', '<leader>4', "<cmd>lua toggleDiagnostics()<CR>", 
        {buffer = true, silent = true})
end

local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities = require('cmp_nvim_lsp').update_capabilities(capabilities)

local py_before_init = function(params, config)
    local match = vim.fn.glob(path.join(config.root_dir, '*', 'pyvenv.cfg'))
    if match ~= '' then
        venv_dir = path.dirname(match)
        version = helpers.get_python_major_version(match)

        config.settings.pylsp.plugins.jedi = {environment = venv_dir}
        config.settings.pylsp.plugins.pylsp_mypy.overrides =
        {"--python-executable", path.join(venv_dir, 'bin', 'python'), 
            "--python-version", version, "--namespace-packages", true}
    end

    local pylint_match = vim.fn.glob(
        path.join(config.root_dir, '*/lib/*', 'site-packages/'))
    if pylint_match ~= '' then
        config.settings.pylsp.plugins.pylint.args = {'--init-hook="import sys; sys.path.extend([\''
        .. pylint_match
        .. '\', \''
        .. config.root_dir
        .. '\'])"'}
    elseif config.root_dir then
        config.settings.pylsp.plugins.pylint.args = {'--init-hook="import sys; sys.path.append(\'' .. config.root_dir .. '\')"'}
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

updateDiags = function()
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
    
