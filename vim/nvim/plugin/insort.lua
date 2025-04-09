local function insort()
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

vim.api.nvim_create_user_command('Insort', insort, {})
