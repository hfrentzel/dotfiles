local wezterm = require('wezterm')
local config = {}
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = true

local colon = ':'
wezterm.on('update-right-status', function(win, _)
    if colon == ':' then
        colon = ' '
    else
        colon = ':'
    end
    local date = wezterm.strftime('%H' .. colon .. '%M %m/%d/%y')
    local name = os.getenv('USERNAME') .. '@' .. wezterm.hostname()
    local workspace = '(' .. win:active_workspace() .. ')'

    win:set_right_status(workspace .. ' ' .. name .. ' ' .. date)
end)

return config
