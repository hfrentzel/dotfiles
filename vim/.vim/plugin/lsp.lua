local on_attach = function ()
    vim.keymap.set('n', 'K', "<cmd>lua vim.lsp.buf.hover()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', 'gd', "<cmd>lua vim.lsp.buf.definition()<CR>", {buffer = true, silent = true})
    vim.keymap.set('n', '<leader>3', "<cmd>lua vim.diagnostic.setloclist()<CR>", {buffer = true, silent = true})
end

require'lspconfig'.pylsp.setup{
    on_attach = on_attach,
    settings = {
        pylsp = {
            plugins = {
                flake8 = {maxLineLength = 120}
            }
        }
    }
}
