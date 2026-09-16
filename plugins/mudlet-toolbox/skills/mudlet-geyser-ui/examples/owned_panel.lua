local Panel = {}

function Panel.escape(text)
  assert(type(text) == "string", "text must be a string")
  return (text:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;")
    :gsub('"', "&quot;"):gsub("'", "&#39;"))
end

function Panel.new(api, owner, onClick)
  assert(type(owner) == "string" and owner ~= "", "owner required")
  assert(type(onClick) == "function", "onClick required")
  local root, label, active, generation = nil, nil, false, 0
  local self = {}

  function self:destroy()
    active = false
    generation = generation + 1
    if root then
      -- Preserve the reference if deletion raises, so cleanup can be retried.
      root:delete()
      root, label = nil, nil
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
      label = geyser.Label:new({
        name = owner .. ".status", x = 0, y = 0, width = "100%", height = "100%"
      }, root)
      label:echo("Ready")
      label:setClickCallback(function(...)
        if active and generation == currentGeneration then onClick(...) end
      end)
      active = true
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

  function self:setText(text)
    assert(active, "mount before rendering")
    label:echo(Panel.escape(text))
    return self
  end

  function self:resize(width, height)
    assert(active, "mount before resizing")
    assert(type(width) == "number" and width > 0 and width < math.huge, "invalid width")
    assert(type(height) == "number" and height > 0 and height < math.huge, "invalid height")
    root:resize(width, height)
    return self
  end

  return self
end

return Panel
