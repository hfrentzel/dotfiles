local function switch_source_header(bufnr, client)
    local method_name = 'textDocument/switchSourceHeader'
    local params = vim.lsp.util.make_text_document_params(bufnr)

    client:request(method_name, params, function(err, result)
        if err then
            error(tostring(err))
        end
        if not result then
            vim.notify('corresponding file cannot be determined')
            return
        end
        vim.cmd.edit(vim.uri_to_fname(result))
    end, bufnr)
end

return {
    cmd = {
        'clangd',
        '--background-index',
        '--clang-tidy',
        '--header-insertion=iwyu',
        '--completion-style=detailed',
        '--function-arg-placeholders',
        '--fallback-style=llvm',
    },
    filetypes = { 'c', 'cpp' },
    root_markers = {
        'compile_commands.json',
        'compile_flags.txt',
        'configure.ac',
    },
    init_options = {
        usePlaceholders = true,
        completeUnimported = true,
        clangdFileStatus = true,
    },
    on_attach = function(client, bufnr)
        vim.api.nvim_buf_create_user_command(bufnr, 'Switch', function()
            switch_source_header(bufnr, client)
        end, {})
    end,
}
