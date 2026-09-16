local Planner = {}

local function positiveInteger(value)
  return type(value) == "number" and value > 0 and value < math.huge
    and value == math.floor(value)
end

local function part(value)
  return tostring(#value) .. ":" .. value
end

function Planner.planRoom(api, owner, source, externalID)
  if type(owner) ~= "string" or owner == ""
    or type(source) ~= "string" or source == ""
    or type(externalID) ~= "string" or externalID == "" then
    return nil, "identity strings required"
  end
  local prefix = "toolbox-room:" .. part(owner)
  local hash = prefix .. part(source) .. part(externalID)
  local plan = {
    hash = hash, owner = owner, source = source, externalID = externalID,
    ownerKey = prefix .. ":owner", sourceKey = prefix .. ":source",
    externalKey = prefix .. ":external"
  }
  local id = api.getRoomIDbyHash(hash)
  if id == -1 then
    local err
    id, err = api.createRoomID()
    if not positiveInteger(id) then return nil, err or "invalid candidate room ID" end
    if api.getRoomName(id) ~= nil then return nil, "candidate room already exists" end
    if api.getRoomHashByID(id) ~= nil then return nil, "candidate has a stale hash" end
    plan.action, plan.roomID = "create", id
    return plan
  end
  if not positiveInteger(id) then return nil, "invalid hash lookup result" end
  if api.getRoomName(id) == nil then return nil, "hash points to a missing room" end
  if api.getRoomHashByID(id) ~= hash then return nil, "inconsistent reverse hash" end
  if api.getRoomUserData(id, plan.ownerKey) ~= owner then return nil, "room ownership conflict" end
  if api.getRoomUserData(id, plan.sourceKey) ~= source
    or api.getRoomUserData(id, plan.externalKey) ~= externalID then
    return nil, "room source identity conflict"
  end
  plan.action, plan.roomID = "reuse", id
  return plan
end

return Planner
