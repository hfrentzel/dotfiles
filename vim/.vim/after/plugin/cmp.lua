local has_cmp, cmp = pcall(require, 'cmp')
if not has_cmp then
    return
end
local luasnip = require'luasnip'

local column = function() 
    local _line, col = unpack(vim.api.nvim_win_get_cursor(0))
    return col
end

local in_whitespace = function()
    local col = column()
    return col == 0 or vim.api.nvim_get_current_line():sub(col, col):match('%s')
end

cmp.setup {
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

        ['<Tab>'] = cmp.mapping(function(_fallback)
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
            end
        end, {'i', 's'}),

        ['<Enter>'] = cmp.mapping(function(fallback)
            if cmp.visible() then
                cmp.confirm({select = true})
            else
                fallback()
            end
        end, {'i', 's'})
    },

    sources = cmp.config.sources({
        { name = 'nvim_lsp'},
        { name = 'buffer'},
        { name = 'luasnip'},
        { name = 'nvim_lua'},
        { name = 'path'}
    })
}

