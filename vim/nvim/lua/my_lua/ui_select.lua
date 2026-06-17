-- Custom vim.ui.select override --
-- Originally adapted from the builtin select ui at 
-- https://github.com/stevearc/dressing.nvim
local M = {}
local _on_choice_callback = function(_, _) end
local _items = {}

local calculate_float_width = function(content_width)
  local parent_width = vim.api.nvim_win_get_width(0)
  local min_width = math.max(40, 0.2 * parent_width)
  local max_width = math.min(140, 0.8 * parent_width)
  return math.floor(math.max(math.min(content_width, max_width), min_width))
end

local calculate_float_height = function(content_height)
  local win_height = vim.api.nvim_win_get_height(0)
  local min_height = math.max(10, 0.2 * win_height)
  local max_height = 0.9 * win_height
  return math.floor(math.max(math.min(content_height, max_height), min_height))
end

local function close_select_window(idx)
  local callback = _on_choice_callback
  local items = _items
  _on_choice_callback = function() end
  _items = {}
  vim.api.nvim_win_close(0, true)
  callback(idx ~= nil and items[idx] or nil, idx)
end

local choose = function()
  close_select_window(vim.api.nvim_win_get_cursor(0)[1])
end

local cancel = function()
  close_select_window(nil)
end

local function remove_newlines(line)
  return string.gsub(tostring(line), "\n", " ")
end

M.select = vim.schedule_wrap(function(items, opts, on_choice)
  vim.validate("items", items, vim.islist, true)
  vim.validate("on_choice", on_choice, "function")
  opts = opts or {}

  local parent_winid = vim.api.nvim_get_current_win()
  local cursor_pos = vim.api.nvim_win_get_cursor(parent_winid)
  _on_choice_callback = vim.schedule_wrap(function(...)
    if vim.api.nvim_win_is_valid(parent_winid) then
      vim.api.nvim_win_set_cursor(parent_winid, cursor_pos)
    end
    on_choice(...)
  end)
  _items = items

  local bufnr = vim.api.nvim_create_buf(false, true)
  vim.bo[bufnr].swapfile = false
  vim.bo[bufnr].bufhidden = "wipe"

  local prompt = vim.trim(remove_newlines(opts.prompt or "Select one of:"))
  if prompt:sub(-1, -1) == ":" then
    prompt = prompt:sub(1, -2)
  end

  local format_item_func = opts.format_item or remove_newlines
  local lines = {}
  local max_width = vim.api.nvim_strwidth(prompt)
  for idx, item in ipairs(items) do
    vim.api.nvim_buf_set_keymap(bufnr, "n", tostring(idx), "", {
      callback = function()
        close_select_window(idx)
      end,
    })
    local line = "[" .. idx .. "] " .. format_item_func(item)
    max_width = math.max(max_width, vim.api.nvim_strwidth(line))
    table.insert(lines, line)
  end
  vim.api.nvim_buf_set_lines(bufnr, 0, -1, true, lines)
  vim.bo[bufnr].modifiable = false

  local ns = vim.api.nvim_create_namespace("CustomSelectFloat")
  for lnum = 1, #lines do
    vim.api.nvim_buf_add_highlight(bufnr, ns, "CustomSelectIdx", lnum - 1, 0, lnum > 9 and 5 or 4)
  end

  local winopt = {
    relative = "cursor",
    row = 1,
    col = 0,
    border = "rounded",
    width = calculate_float_width(max_width + 1),
    height = calculate_float_height(#lines),
    zindex = 150,
    title = prompt:gsub("^%s*(.-)%s*$", " %1 "),
    title_pos = "center",
    style = "minimal",
  }
  local winid = vim.api.nvim_open_win(bufnr, true, winopt)

  vim.api.nvim_set_option_value("cursorline", true, { scope = "local", win = winid })
  vim.api.nvim_set_option_value("cursorlineopt", "both", { scope = "local", win = winid })
  vim.api.nvim_set_option_value("winhighlight", "MatchParen:", { scope = "local", win = winid })
  vim.api.nvim_set_option_value("statuscolumn", " ", { scope = "local", win = winid })
  vim.bo[bufnr].filetype = "custom_select_popup"

  vim.keymap.set("n", "<Esc>", cancel, { buffer = bufnr, remap = true, nowait = true })
  vim.keymap.set("n", "<C-c>", cancel, { buffer = bufnr, remap = true, nowait = true })
  vim.keymap.set("n", "<CR>", choose, { buffer = bufnr, remap = true, nowait = true })
  vim.api.nvim_create_autocmd("BufLeave", {
    buffer = bufnr,
    nested = true,
    once = true,
    callback = cancel,
  })
end)

return M
