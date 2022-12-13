has_telescope, telescope = pcall(require, 'telescope')
if not has_telescope then
    return
end

function getVisualSelection()
    vim.cmd('noau normal! "vy"')
    local text = vim.fn.getreg('v')
    vim.fn.setreg('v', {})

    text = string.gsub(text, "\n", "")
    if #text > 0 then
        return text
    else 
        return ''
    end
end


telescope.setup({
    defaults = {
        dynamic_preview_title = true,
        mappings = {
            i = {
                ["<c-j>"] = "move_selection_next",
                ["<c-k>"] = "move_selection_previous",
                ["<c-\\>"] = "select_vertical",
                ["<c-s>"] = "select_horizontal",
            }
        },
        path_display = {truncate = 50},
        -- Default includes --smart-case, I don't want that
        vimgrep_arguments = {
            "rg", "--color=never", "--no-heading", "--with-filename",
            "--line-number", "--column"
        },
    },
    pickers = {
        live_grep = {
            disable_coordinates = true,
            prompt_title = 'Search in Files',
            theme = "dropdown",
            layout_config = {
                anchor = 'N',
                prompt_position = 'top',
                width = 0.8,
            }
        }
    }
})

local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>g', builtin.live_grep)
vim.keymap.set('v', '<leader>g', function()
    local text = getVisualSelection()
    builtin.live_grep({default_text = text})
end)
