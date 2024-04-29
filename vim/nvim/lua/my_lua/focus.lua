local focus = {}

local colorcolumns = '+' .. table.concat(vim.fn.range(0, 254), ',+')

local winhighlight_blurred = table.concat({
    'CursorLineNr:LineNr',
    'EndOfBuffer:ColorColumn',
    'IncSearch:ColorColumn',
    'Normal:ColorColumn',
    'NormalNC:ColorColumn',
    'Search:ColorColumn',
    'SignColumn:ColorColumn',
}, ',')

local number_blacklist = {
    ['fugitiveblame'] = true,
    ['help'] = true,
    ['NvimTree'] = true,
    ['qf'] = true,
}

local focus_full_window = {
    ['qf'] = true,
}

focus.focus_window = function()
    local filetype = vim.bo.filetype
    local filename = vim.api.nvim_buf_get_name(0)

    if
        vim.api.nvim_win_get_config(0).relative == ''
        and filetype ~= ''
        and number_blacklist[filetype] ~= true
    then
        vim.wo.number = true
        vim.wo.relativenumber = true
    end
    if filename == '' or focus_full_window[filetype] == true then
        vim.wo.winhighlight = ''
        vim.wo.colorcolumn = ''
    else
        vim.wo.winhighlight = 'EndOfBuffer:ColorColumn'
        vim.wo.colorcolumn = colorcolumns
    end
end

focus.blur_window = function()
    local filetype = vim.bo.filetype

    if
        vim.api.nvim_win_get_config(0).relative == ''
        and filetype ~= ''
        and number_blacklist[filetype] ~= true
    then
        vim.wo.number = true
        vim.wo.relativenumber = false
    end
    vim.wo.winhighlight = winhighlight_blurred
end

return focus
