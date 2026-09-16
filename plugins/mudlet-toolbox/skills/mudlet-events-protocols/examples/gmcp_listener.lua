local Listener = {}

function Listener.readPath(root, path)
  local value = root
  for _, key in ipairs(path) do
    if type(value) ~= "table" then return nil end
    value = value[key]
  end
  return value
end

function Listener.new(api, options)
  assert(type(options.owner) == "string" and options.owner ~= "", "owner required")
  assert(type(options.name) == "string" and options.name ~= "", "name required")
  assert(type(options.event) == "string" and options.event ~= "", "event required")
  assert(type(options.onUpdate) == "function", "onUpdate required")
  assert(type(options.path) == "table" and #options.path > 0, "path required")
  local path = {}
  for i, key in ipairs(options.path) do
    assert(type(key) == "string" and key ~= "", "path keys must be strings")
    path[i] = key
  end
  local owner, name, event = options.owner, options.name, options.event
  local update = options.onUpdate
  local named = type(api.registerNamedEventHandler) == "function"
    and type(api.stopNamedEventHandler) == "function"
    and type(api.deleteNamedEventHandler) == "function"
  if not named then
    assert(type(api.registerAnonymousEventHandler) == "function", "event API required")
    assert(type(api.killAnonymousEventHandler) == "function", "cleanup API required")
  end
  local running, registered, destroyed, id = false, false, false, nil
  local self = {}

  function self:refresh(eventName, fullKey)
    if running then update(Listener.readPath(api.gmcp, path), eventName or event, fullKey) end
  end

  function self:start()
    assert(not destroyed, "listener destroyed")
    if running then return self end
    local callback = function(eventName, fullKey) self:refresh(eventName, fullKey) end
    if named then
      assert(api.registerNamedEventHandler(owner, name, event, callback), "registration failed")
    else
      id = api.registerAnonymousEventHandler(event, callback)
      assert(type(id) == "number", "registration must return an ID")
    end
    registered, running = true, true
    return self
  end

  function self:stop()
    if not running then return self end
    running = false
    if named then
      api.stopNamedEventHandler(owner, name)
    else
      api.killAnonymousEventHandler(id)
      id, registered = nil, false
    end
    return self
  end

  function self:destroy()
    if destroyed then return self end
    self:stop()
    if named and registered then api.deleteNamedEventHandler(owner, name) end
    registered, destroyed = false, true
    return self
  end

  return self
end

return Listener
