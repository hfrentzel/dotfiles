require('telescope').setup({
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
vim.keymap.set('n', '<leader>f', builtin.live_grep)
