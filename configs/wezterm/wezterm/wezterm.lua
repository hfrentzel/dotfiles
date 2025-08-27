local config = {}

config.harfbuzz_features = { 'calt = 0', 'clig = 0', 'liga = 0' }
config.default_prog = { os.getenv('USERPROFILE') .. '/AppData/Local/Programs/nu/bin/nu.exe' }
config.window_padding = { bottom = 0 }

local key_config = require('keys')
for k, v in pairs(key_config) do
    config[k] = v
end

local status_config = require('statusbar')
for k, v in pairs(status_config) do
    config[k] = v
end


return config
