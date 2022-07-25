local cmp = require'cmp'

local column = function() 
    local _line, col = unpack(vim.api.nvim_win_get_cursor(0))
    return col
end

local in_whitespace = function()
    local col = column()
    return col == 0 or vim.api.nvim_get_current_line():sub(col, col):match('%s')
end

cmp.setup {
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
            elseif in_whitespace() then
                vim.api.nvim_feedkeys(
                vim.api.nvim_replace_termcodes('<Tab>', true, true, true),
                'nt', true)
            else
                cmp.complete()
            end
        end, {'i', 's'}),
    },

    sources = cmp.config.sources({
        { name = 'buffer'},
        { name = 'nvim_lsp'},
        { name = 'nvim_lua'},
        { name = 'path'}
    })
}

