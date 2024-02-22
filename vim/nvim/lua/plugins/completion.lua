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
    {'nvim-cmp', dir = '~/.config/nvim/pack/vendor/opt/nvim-cmp',
        event = "InsertEnter",
        dependencies = {
            {'cmp-buffer', dir = '~/.config/nvim/pack/vendor/opt/cmp-buffer'},
            {'cmp-nvim-lsp', dir = '~/.config/nvim/pack/vendor/opt/cmp-nvim-lsp'},
            {'cmp-nvim-lua', dir = '~/.config/nvim/pack/vendor/opt/cmp-nvim-lua'},
            {'cmp-path', dir = '~/.config/nvim/pack/vendor/opt/cmp-path'},
            {'cmp_luasnip', dir = '~/.config/nvim/pack/vendor/opt/cmp_luasnip'},
            {'LuaSnip', dir = '~/.config/nvim/pack/vendor/opt/LuaSnip'},
        },
        opts = function()
            local cmp = require('cmp')
            local luasnip = require('luasnip')

            return{
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
                    end, {'i', 's'}),

                    ['<Tab>'] = cmp.mapping(function(_)
                        if cmp.visible() then
                            if #cmp.get_entries() == 1 then
                                cmp.confirm({select = true})
                            else
                                cmp.select_next_item()
                            end
                        elseif luasnip.expand_or_locally_jumpable() then
                            luasnip.expand_or_jump()
                        elseif in_whitespace() then
                            vim.api.nvim_feedkeys(
                                vim.api.nvim_replace_termcodes('<Tab>', true, true, true),
                                'nt', true)
                        else
                            cmp.complete()
                            if #cmp.get_entries() == 0 then
                                vim.api.nvim_feedkeys(
                                    vim.api.nvim_replace_termcodes('<Tab>', true, true, true),
                                    'nt', true)
                            end
                        end
                    end, {'i', 's'}),

                    -- Leaving for now, reevaluate when I properly use snippets
                    -- ['<Enter>'] = cmp.mapping(function(fallback)
                    --     if cmp.visible() then
                    --         cmp.confirm({select = true})
                    --     else
                    --         fallback()
                    --     end
                    -- end, {'i', 's'})
                },

                sources = cmp.config.sources({
                    { name = 'nvim_lsp'},
                    { name = 'buffer'},
                    { name = 'luasnip'},
                    { name = 'nvim_lua'},
                    { name = 'path'}
                })
            }
        end
    }
}
