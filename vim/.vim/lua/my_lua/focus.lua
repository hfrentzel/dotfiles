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

focus.focus_window = function()
    vim.wo.number = true
    vim.wo.relativenumber = true
    vim.wo.winhighlight = 'EndOfBuffer:ColorColumn'
    vim.wo.colorcolumn = colorcolumns
end

focus.blur_window = function()
    vim.wo.number = true
    vim.wo.relativenumber = false
    vim.wo.winhighlight = winhighlight_blurred
end

return focus
