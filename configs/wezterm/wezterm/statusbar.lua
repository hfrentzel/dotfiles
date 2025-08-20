local wezterm = require('wezterm')
local config = {}
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = true
config.tab_max_width = 50

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

wezterm.on('format-tab-title', function(tab, tabs, _, _, _, _)
    local index = tab.tab_index + 1
    local title = tab.active_pane.title

    local domain = tab.active_pane.domain_name
    local show_domain = false
    for _, tabi in ipairs(tabs) do
        if tabi.active_pane.domain_name ~= domain then
            show_domain = true
            break
        end
    end

    if show_domain then
        return ' '..index..': ('..domain..') '..title..' '
    else
        return ' '..index..': '..title..' '
    end
end)

return config
