return {
    cmd = { 'pylsp' },
    filetypes = { 'python' },
    before_init = require('my_lua.lsp.python').before_init,
    root_dir = function(_, callback)
        local root
        if vim.b['workspace'] then
            root = vim.b['workspace']
        else
            root =  vim.fs.root(0, '.git') or vim.fn.expand('%:p:h')
        end
        callback(root)
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
}
