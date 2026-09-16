local DelayedAction = {}

function DelayedAction.new(emit, delay)
  assert(type(emit) == "function", "emit must be a function")
  assert(type(delay) == "number" and delay >= 0 and delay < math.huge,
    "delay must be a finite nonnegative number")
  local action = { timer = nil }

  function action:cancel()
    if self.timer then
      killTimer(self.timer)
      self.timer = nil
    end
  end

  function action:schedule(text)
    assert(type(text) == "string", "text must be a captured string")
    self:cancel()
    local captured = text
    local id, err = tempTimer(delay, function()
      self.timer = nil
      emit(captured)
    end)
    if not id then
      return nil, err or "timer registration failed"
    end
    self.timer = id
    return true
  end

  return action
end

return DelayedAction
