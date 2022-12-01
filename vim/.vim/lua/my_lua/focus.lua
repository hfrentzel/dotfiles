focus = {}

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
    ['help'] = true,
    ['NvimTree'] = true,
    ['qf'] = true,
}

focus.focus_window = function()
    local filetype = vim.bo.filetype

    if filtype ~= '' and number_blacklist[filetype] ~= true then
        vim.wo.number = true
        vim.wo.relativenumber = true
    end
    vim.wo.winhighlight = 'EndOfBuffer:ColorColumn'
    vim.wo.colorcolumn = colorcolumns
end

focus.blur_window = function()
    local filetype = vim.bo.filetype

    if filetype ~= '' and number_blacklist[filetype] ~= true then
        vim.wo.number = true
        vim.wo.relativenumber = false
    end
    vim.wo.winhighlight = winhighlight_blurred
end

return focus
