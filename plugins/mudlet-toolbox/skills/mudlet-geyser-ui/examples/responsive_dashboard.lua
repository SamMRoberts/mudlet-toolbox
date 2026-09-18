local Dashboard = {}

local function finite(value)
  return type(value) == "number" and value == value
    and value > -math.huge and value < math.huge
end

function Dashboard.escape(text)
  assert(type(text) == "string", "text must be a string")
  return (text:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;")
    :gsub('"', "&quot;"):gsub("'", "&#39;"))
end

local function normalize(state)
  assert(type(state) == "table", "state must be a table")
  assert(type(state.title) == "string", "title must be a string")
  assert(type(state.status) == "string", "status must be a string")
  assert(finite(state.current), "current must be finite")
  assert(finite(state.maximum) and state.maximum > 0, "maximum must be positive and finite")
  assert(state.gaugeText == nil or type(state.gaugeText) == "string", "gaugeText must be a string")
  local current = math.max(0, math.min(state.current, state.maximum))
  local gaugeText = state.gaugeText or string.format("%s / %s", tostring(state.current), tostring(state.maximum))
  return {
    title = state.title,
    status = state.status,
    current = current,
    maximum = state.maximum,
    gaugeText = gaugeText,
  }
end

function Dashboard.new(api, owner, onSubmit)
  assert(type(owner) == "string" and owner ~= "", "owner required")
  assert(type(onSubmit) == "function", "onSubmit required")
  local root, title, status, gauge, output, input = nil, nil, nil, nil, nil, nil
  local active, generation = false, 0
  local state = normalize({title = "Status", status = "Waiting", current = 0, maximum = 1})
  local self = {}

  local function applyState()
    title:echo(Dashboard.escape(state.title))
    status:echo(Dashboard.escape(state.status))
    gauge:setValue(state.current, state.maximum, Dashboard.escape(state.gaugeText))
  end

  function self:destroy()
    active = false
    generation = generation + 1
    if root then
      -- Keep the root reference if deletion raises so cleanup can be retried.
      root:delete()
      root, title, status, gauge, output, input = nil, nil, nil, nil, nil, nil
    end
    return self
  end

  function self:mount(parent)
    if active then return self end
    assert(root == nil, "retry destroy before mounting after cleanup failure")
    local geyser = assert(api.Geyser, "Geyser required")
    assert(type(geyser.Container.delete) == "function", "recursive deletion required")
    generation = generation + 1
    local currentGeneration = generation
    local ok, err = pcall(function()
      root = geyser.Container:new({
        name = owner .. ".root", x = 0, y = 0, width = "100%", height = "100%"
      }, parent)
      local header = geyser.HBox:new({
        name = owner .. ".header", x = 0, y = 0, width = "100%", height = "2c"
      }, root)
      title = geyser.Label:new({name = owner .. ".title", h_stretch_factor = 2}, header)
      status = geyser.Label:new({name = owner .. ".status", h_stretch_factor = 1}, header)
      local body = geyser.VBox:new({
        name = owner .. ".body", x = 0, y = "2c", width = "100%", height = "100%-4c"
      }, root)
      gauge = geyser.Gauge:new({
        name = owner .. ".gauge", height = "2c", v_policy = geyser.Fixed,
        orientation = "horizontal"
      }, body)
      output = geyser.MiniConsole:new({
        name = owner .. ".output", autoWrap = true, scrollBar = true
      }, body)
      input = geyser.CommandLine:new({
        name = owner .. ".input", x = 0, y = "-2c", width = "100%", height = "2c",
        stylesheet = "QPlainTextEdit { border: 1px solid silver; }"
      }, root)
      input:setAction(function(text)
        if active and generation == currentGeneration and type(text) == "string" then
          onSubmit(text)
        end
      end)
      active = true
      applyState()
    end)
    if not ok then
      local cleaned, cleanupError = pcall(self.destroy, self)
      if not cleaned then
        error(tostring(err) .. "; cleanup failed: " .. tostring(cleanupError), 0)
      end
      error(err, 0)
    end
    return self
  end

  function self:render(nextState)
    state = normalize(nextState)
    if active then applyState() end
    return self
  end

  function self:append(text)
    assert(active, "mount before appending")
    assert(type(text) == "string", "text must be a string")
    output:echo(text)
    return self
  end

  return self
end

return Dashboard
