-- treesitter.lua
-- Initialize and configure treesitter for syntax highlighting, indents, folds
-- and selections

return {
    {
        'nvim-treesitter',
        dev = true,
        event = { 'FileType' },
        cmd = { 'TSUpdate', 'TSUpdateSync', 'TSInstall', 'TSInstallSync' },
        dependencies = {
            {
                'nvim-treesitter-textobjects',
                dev = true,
            },
        },
        config = function()
            require('nvim-treesitter').setup({
                install_dir = vim.fn.stdpath('data') .. '/site',
            })

            vim.keymap.set({ 'x', 'o' }, 'af', function()
                require('nvim-treesitter-textobjects.select').select_textobject(
                    '@function.outer',
                    'textobjects'
                )
            end)
            vim.keymap.set({ 'x', 'o' }, 'if', function()
                require('nvim-treesitter-textobjects.select').select_textobject(
                    '@function.inner',
                    'textobjects'
                )
            end)
            vim.keymap.set({ 'x', 'o' }, 'aif', function()
                require('nvim-treesitter-textobjects.select').select_textobject(
                    '@conditional.outer',
                    'textobjects'
                )
            end)
            vim.keymap.set({ 'x', 'o' }, 'iif', function()
                require('nvim-treesitter-textobjects.select').select_textobject(
                    '@conditional.inner',
                    'textobjects'
                )
            end)
            vim.keymap.set({ 'n', 'x', 'o' }, ']f', function()
                require('nvim-treesitter-textobjects.move').goto_next_start(
                    '@function.outer',
                    'textobjects'
                )
            end)
            vim.keymap.set({ 'n', 'x', 'o' }, '[f', function()
                require('nvim-treesitter-textobjects.move').goto_previous_start(
                    '@function.outer',
                    'textobjects'
                )
            end)

            vim.api.nvim_create_autocmd('FileType', {
                pattern = { '*' },
                callback = function()
                    local hasStarted = pcall(vim.treesitter.start)
                    if hasStarted then
                        vim.bo.indentexpr = "v:lua.require'nvim-treesitter'.indentexpr()"
                        vim.o.foldmethod = 'expr'
                        vim.wo.foldexpr = 'v:lua.vim.treesitter.foldexpr()'
                    end
                end,
            })

            vim.api.nvim_create_user_command('QueryEditor', function()
                vim.treesitter.inspect_tree()
                vim.treesitter.query.edit()
                vim.cmd.wincmd('=')
            end, {})

            -- vim.keymap.set(
            --     'n',
            --     '<leader>x',
            --     '<cmd>lua print(require"nvim-treesitter.ts_utils".get_node_at_cursor():type())<CR>'
            -- )
        end,
    },
}
