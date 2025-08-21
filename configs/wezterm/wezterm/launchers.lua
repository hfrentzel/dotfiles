local wezterm = require('wezterm')
local launchers = {}

local workspace_choices = {}
table.insert(workspace_choices, { id = 'local', label = 'local' })

local wsl_domains = wezterm.default_wsl_domains()
local keeper_domains = {}

for _, domain in ipairs(wsl_domains) do
    if string.find(domain.name, 'Ubuntu') ~= nil then
        domain.name = string.gsub(domain.name, 'WSL:', '')
        domain.name = string.gsub(domain.name, '-', '')
        table.insert(keeper_domains, domain)
        table.insert(workspace_choices, { id = domain.name, label = domain.name })
    end
end

launchers.wsl_domains = keeper_domains

local function includes(list, item)
    for _, el in ipairs(list) do
        if item == el then
            return true
        end
    end

    return false
end

launchers.workspace_launcher = wezterm.action.InputSelector({
    title = 'Workspace Launcher',
    alphabet = '1234567890',
    description = 'Create a new workspace in the selected domain',
    choices = workspace_choices,
    action = wezterm.action_callback(function(win, pane, id, _)
        local count = 0
        local name = id
        local existing_workspaces = wezterm.mux.get_workspace_names()
        while includes(existing_workspaces, name) do
            name = id .. count
            count = count + 1
        end

        win:perform_action(
            wezterm.action.SwitchToWorkspace({
                name = name,
                spawn = {
                    domain = { DomainName = id },
                },
            }),
            pane
        )
    end),
})

launchers.tab_launcher = wezterm.action.InputSelector({
    title = 'Tab Launcher',
    alphabet = '1234567890',
    description = 'Create a new tab',
    choices = workspace_choices,
    action = wezterm.action_callback(function(win, pane, id, _)
        -- TODO use SpawnCommandInNewTab and offer more options
        win:perform_action(wezterm.action.SpawnTab({ DomainName = id }), pane)
    end),
})

return launchers
