local wezterm = require('wezterm')
local launchers = require('launchers')
local config = {}


config.leader = { key = ' ', mods = 'CTRL' }
config.wsl_domains = launchers.wsl_domains

config.keys = {
    -- General keymaps similar to most applications
    { key = 'F11', mods = 'NONE', action = wezterm.action.ToggleFullScreen },
    { key = 'Enter', mods = 'LEADER', action = wezterm.action.ActivateCopyMode },
    { key = 'v', mods = 'CTRL', action = wezterm.action.PasteFrom('Clipboard') },

    -- Pane Management
    { key = '\\', mods = 'LEADER', action = wezterm.action.SplitHorizontal },
    { key = '-', mods = 'LEADER', action = wezterm.action.SplitVertical },
    { key = '8', mods = 'CTRL', action = wezterm.action.RotatePanes('Clockwise') },
    { key = '7', mods = 'CTRL', action = wezterm.action.PaneSelect(
        {mode = 'SwapWithActiveKeepFocus' }) },

    -- Tab Management
    { key = 'c', mods = 'LEADER', action = wezterm.action.SpawnTab('CurrentPaneDomain') },
    { key = '0', mods = 'CTRL', action = wezterm.action.ActivateTabRelative(1) },
    { key = '9', mods = 'CTRL', action = wezterm.action.ActivateTabRelative(-1) },
    { key = 's', mods = 'LEADER', action = wezterm.action.ShowLauncherArgs({flags = 'WORKSPACES'})},
    { key = 'w', mods = 'ALT', action = launchers.workspace_launcher},
    { key = 't', mods = 'ALT', action = launchers.tab_launcher}
}

local splits = require('splits')
for _,v in ipairs(splits.keys) do
    table.insert(config.keys, v)
end

-- Copy Mode bindings
local copy_mode = wezterm.gui.default_key_tables().copy_mode
local new_copy_mode_keys = {
    {
        key = 'Escape',
        mods = 'NONE',
        action = wezterm.action_callback(function(win, pane)
            if win:get_selection_text_for_pane(pane) ~= '' then
                win:perform_action(wezterm.action.CopyMode('ClearSelectionMode'), pane)
            else
                win:perform_action(wezterm.action.CopyMode('Close'), pane)
            end
        end),
    },
    {
        key = 'n',
        mods = 'CTRL',
        action = wezterm.action_callback(function(win, pane)
            if win:get_selection_text_for_pane(pane) == '' then
                win:perform_action(wezterm.action.CopyMode({ SetSelectionMode = 'Line' }), pane)
            end
            win:perform_action(
                wezterm.action.Multiple({
                    wezterm.action.CopyTo('Clipboard'),
                    wezterm.action.CopyMode('ClearSelectionMode'),
                    wezterm.action.CopyMode('Close'),
                    wezterm.action.PasteFrom('Clipboard'),
                }),
                pane
            )
        end),
    },
    {
        key = 'I',
        mods = 'NONE',
        action = wezterm.action.CopyMode({ SetSelectionMode = 'Word' }),
    },
}
for _, value in ipairs(new_copy_mode_keys) do
    table.insert(copy_mode, value)
end
config.key_tables = {
    copy_mode = copy_mode,
}

return config
