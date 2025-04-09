local diags_on = true

local toggleDiagnostics = function()
    if diags_on then
        diags_on = false
        vim.diagnostic.hide()
        vim.diagnostic.config({
            virtual_text = false,
            underline = false,
            signs = false,
        })
    else
        diags_on = true
        vim.diagnostic.show(nil, nil, nil, { virtual_text = true, underline = true, signs = true })
        vim.diagnostic.config({
            severity_sort = true,
            virtual_text = true,
            signs = true,
        })
    end
end

local format = function()
    require('conform').format({ async = true })
end

local on_attach = function()
    local args = { buffer = true, silent = true }
    vim.diagnostic.config({ severity_sort = true, virtual_text = true })
    vim.wo.signcolumn = 'yes'
    vim.keymap.set('n', 'g=', format, args)
    vim.keymap.set('n', 'K', function()
        vim.lsp.buf.hover({ border = 'rounded' })
    end, args)
    vim.keymap.set('n', '<leader>d', function()
        vim.diagnostic.open_float({ border = 'rounded' })
    end, args)
    vim.keymap.set('n', '<leader>3', vim.diagnostic.setloclist, args)
    vim.keymap.set('n', '<leader>4', toggleDiagnostics, args)
end

local updateDiags = function()
    vim.diagnostic.setloclist({ open = false })
    vim.b.diags_ready = true
    vim.wo.statusline = vim.wo.statusline
end

vim.api.nvim_create_augroup('diagnostics', { clear = true })
vim.api.nvim_create_autocmd('DiagnosticChanged', {
    group = 'diagnostics',
    pattern = '*',
    callback = updateDiags,
})

local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

vim.lsp.config('*', {
    capabilities = capabilities,
    on_attach = on_attach,
})
vim.lsp.enable({
    'eslint',
    'cssls',
    'gopls',
    'jsonls',
    'lua_ls',
    'pylsp',
    'rust_analyzer',
    'ts_ls',
    'vimls',
    'yamlls',
})
