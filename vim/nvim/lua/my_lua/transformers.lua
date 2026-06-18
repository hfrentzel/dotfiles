local M = {}

-- https://vim.fandom.com/wiki/Convert_between_hex_and_decimal
M.hex2dec = function(args)
    if args.args == "" then
        local save_search = vim.fn.getreg('/')
        local search_active = vim.v.hlsearch

        local cmd
        if vim.startswith(vim.fn.histget(':', -1), "^'<,'>") and vim.fn.visualmode() == 'V' then
            cmd = 's/%V0x\\x+/=submatch(0)+0/ge'
        else
            cmd = 's/0x\\x\\+/\\=submatch(0)+0/ge'
        end
        vim.fn.execute(args.line1..','..args.line2..cmd)

        vim.fn.setreg('/', save_search)
        if search_active == 0 then
            vim.cmd.nohlsearch()
        end
    else
        if vim.startswith(args.args, '0x') then
            print(args.args + 0)
        else
            print(('0x' .. args.args) + 0)
        end
    end
end

M.urlencode= function()
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
end

M.insort = function()
    local startpos = vim.fn.searchpos('{\\|(\\|[', 'bcWn')
    local startchar = vim.api.nvim_buf_get_text(
        0,
        startpos[1] - 1,
        startpos[2] - 1,
        startpos[1] - 1,
        startpos[2],
        {}
    )[1]
    local endchar = ''
    if startchar == '[' then
        startchar = '\\['
        endchar = '\\]'
    elseif startchar == '{' then
        endchar = '}'
    else
        endchar = ')'
    end
    local endpos = vim.fn.searchpairpos(startchar, '', endchar, 'zn')
    local text =
        vim.api.nvim_buf_get_text(0, startpos[1] - 1, startpos[2], endpos[1] - 1, endpos[2] - 1, {})
    text = vim.fn.join(text)

    local start_space = false
    local end_space = false
    if string.sub(text, 1, 1) == ' ' then
        start_space = true
    end
    if string.sub(text, #text, #text) == ' ' then
        end_space = true
    end

    local items = vim.fn.split(text, ',\\s\\+')

    for index, item in ipairs(items) do
        items[index] = vim.fn.trim(item)
    end
    items = vim.fn.sort(items)
    local newtext = vim.fn.join(items, ', ')
    if start_space then
        newtext = ' ' .. newtext
    end
    if end_space then
        newtext = newtext .. ' '
    end
    vim.api.nvim_buf_set_text(
        0,
        startpos[1] - 1,
        startpos[2],
        endpos[1] - 1,
        endpos[2] - 1,
        {newtext}
    )
end

return M
