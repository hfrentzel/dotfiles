-- completion.lua
-- Manage editor autocompletion with nvim-cmp

local column = function()
    local _, col = unpack(vim.api.nvim_win_get_cursor(0))
    return col
end

local in_whitespace = function()
    local col = column()
    return col == 0 or vim.api.nvim_get_current_line():sub(col, col):match('%s')
end

return {
    {
        'nvim-cmp',
        dev = true,
        event = 'InsertEnter',
        dependencies = {
            { 'cmp-buffer', dev = true },
            { 'cmp-nvim-lsp', dev = true },
            { 'cmp-nvim-lua', dev = true },
            { 'cmp-path', dev = true },
            { 'cmp_luasnip', dev = true },
            { 'LuaSnip', dev = true },
            { 'friendly-snippets', dev = true },
        },
        init = function()
            vim.o.completeopt = 'menu,menuone,noselect'
        end,
        opts = function()
            local cmp = require('cmp')
            local luasnip = require('luasnip')
            require('luasnip.loaders.from_vscode').lazy_load()

            return {
                preselect = cmp.PreselectMode.None,
                snippet = {
                    expand = function(args)
                        luasnip.lsp_expand(args.body)
                    end,
                },
                mapping = {
                    ['<S-Tab>'] = cmp.mapping(function(fallback)
                        if cmp.visible() then
                            cmp.select_prev_item()
                        else
                            fallback()
                        end
                    end, { 'i', 's' }),

                    ['<Tab>'] = cmp.mapping(function(_)
                        if cmp.visible() then
                            if #cmp.get_entries() == 1 then
                                cmp.confirm({ select = true })
                            else
                                cmp.select_next_item()
                            end
                        elseif luasnip.expand_or_locally_jumpable() then
                            luasnip.expand_or_jump()
                        elseif in_whitespace() then
                            vim.api.nvim_feedkeys(
                                vim.api.nvim_replace_termcodes('<Tab>', true, true, true),
                                'nt',
                                true
                            )
                        else
                            cmp.complete()
                            if #cmp.get_entries() == 0 then
                                vim.api.nvim_feedkeys(
                                    vim.api.nvim_replace_termcodes('<Tab>', true, true, true),
                                    'nt',
                                    true
                                )
                            end
                        end
                    end, { 'i', 's' }),

                    ['<Enter>'] = cmp.mapping(function(fallback)
                        if cmp.get_selected_entry() ~= nil then
                            cmp.confirm({ select = true })
                        else
                            fallback()
                        end
                    end, { 'i', 's' }),
                },

                sources = cmp.config.sources({
                    { name = 'nvim_lsp' },
                    { name = 'nvim_lua' },
                    { name = 'luasnip' },
                    { name = 'path' },
                    { name = 'buffer' },
                }),
            }
        end,
    },
}
