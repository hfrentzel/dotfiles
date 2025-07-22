vim.api.nvim_create_user_command('Encode', function()
    local start = vim.fn.getpos("'<")
    local last = vim.fn.getpos("'>")
    local text = vim.fn.getregion(start, last)[1]
    text = text:gsub('([^%w%-%.~_])', function(c)
        -- For multi-byte characters, each byte is encoded.
        local bytes = { string.byte(c, 1, #c) }
        local encoded = {}
        for _, b in ipairs(bytes) do
            table.insert(encoded, string.format('%%%02X', b))
        end
        return table.concat(encoded)
    end)
    vim.api.nvim_buf_set_text(0, start[2] - 1, start[3] - 1, last[2] - 1, last[3], { text })
end, { range = true })
