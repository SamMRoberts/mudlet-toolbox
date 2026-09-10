"""Observable component behavior under small injected APIs, not native Mudlet QA."""

from pathlib import Path
import unittest

from lupa.lua51 import LuaRuntime

SKILLS = Path(__file__).resolve().parents[1] / "plugins/mudlet-toolbox/skills"


def runtime(module_path, name):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals()[name] = lua.execute((SKILLS / module_path).read_text())
    return lua


class ListenerTests(unittest.TestCase):
    def setUp(self):
        self.lua = runtime("mudlet-events-protocols/examples/gmcp_listener.lua", "Listener")

    def test_named_lifecycle_current_data_and_unrelated_owner(self):
        self.lua.execute('''
          active = {}; definitions = {}; updates = {}; calls = 0
          api = {gmcp = {Example = {State = {value = 1}}}}
          function api.registerNamedEventHandler(owner, name, event, callback)
            calls = calls + 1
            local key = owner .. "/" .. name
            active[key] = callback; definitions[key] = callback; return true
          end
          function api.stopNamedEventHandler(owner, name) active[owner .. "/" .. name] = nil; return true end
          function api.deleteNamedEventHandler(owner, name)
            local key = owner .. "/" .. name; active[key] = nil; definitions[key] = nil; return true
          end
          api.registerNamedEventHandler("other", "watch", "gmcp.Example.State", function() end)
          local options = {owner = "demo", name = "watch", event = "gmcp.Example.State",
            path = {"Example", "State"}, onUpdate = function(value, event, key)
              updates[#updates+1] = {value = value, event = event, key = key}
            end}
          local listener = Listener.new(api, options)
          assert(calls == 1)
          listener:start(); listener:start(); assert(calls == 2)
          local oldCallback = active["demo/watch"]
          oldCallback("gmcp.Example.State", "Example.State")
          assert(updates[1].value.value == 1 and updates[1].key == "Example.State")
          api.gmcp = {Example = {State = false}}
          listener:refresh(); assert(updates[2].value == false)
          api.gmcp = {Example = "malformed"}
          listener:refresh(); assert(updates[3].value == nil)
          listener:stop(); oldCallback(); assert(#updates == 3)
          assert(definitions["demo/watch"] and active["demo/watch"] == nil)
          listener:start(); assert(calls == 3)
          listener:destroy(); listener:destroy()
          assert(definitions["demo/watch"] == nil and active["other/watch"])
          assert(not pcall(function() listener:start() end))
        ''')

    def test_anonymous_fallback_cleanup_and_registration_failure(self):
        self.lua.execute('''
          nextID = 0; handlers = {}; count = 0
          api = {gmcp = {Flag = false}}
          function api.registerAnonymousEventHandler(event, callback)
            nextID = nextID + 1; handlers[nextID] = callback; return nextID
          end
          function api.killAnonymousEventHandler(id) handlers[id] = nil; return true end
          local options = {owner = "demo", name = "watch", event = "gmcp.Flag", path = {"Flag"},
            onUpdate = function(value) assert(value == false); count = count + 1 end}
          local listener = Listener.new(api, options)
          listener:start(); listener:start(); assert(nextID == 1)
          handlers[1]("gmcp.Flag"); assert(count == 1)
          listener:stop(); listener:stop(); assert(handlers[1] == nil)
          listener:start(); listener:destroy(); assert(handlers[2] == nil)
          api.registerAnonymousEventHandler = function() return nil, "unavailable" end
          listener = Listener.new(api, options)
          assert(not pcall(function() listener:start() end))
          listener:destroy()
        ''')


class PanelTests(unittest.TestCase):
    def setUp(self):
        self.lua = runtime("mudlet-geyser-ui/examples/owned_panel.lua", "Panel")
        self.lua.execute('''
          objects = {}; clicks = 0; deletions = 0; failLabel = false
          local Container = {}
          function Container:new(options, parent)
            local obj = setmetatable({name = options.name, children = {}, parent = parent}, {__index = self})
            if parent then table.insert(parent.children, obj) end
            objects[obj.name] = obj; return obj
          end
          function Container:delete()
            for _, child in ipairs(self.children) do child:delete() end
            objects[self.name] = nil; deletions = deletions + 1
          end
          function Container:resize(w, h) self.width = w; self.height = h end
          local Label = setmetatable({}, {__index = Container})
          function Label:new(options, parent)
            if failLabel then error("label failed") end
            return Container.new(self, options, parent)
          end
          function Label:echo(text) self.text = text end
          function Label:setClickCallback(fn) self.callback = fn end
          api = {Geyser = {Container = Container, Label = Label}}
          panel = Panel.new(api, "demo", function() clicks = clicks + 1 end)
        ''')

    def test_idempotence_escaping_resize_and_stale_callbacks(self):
        self.lua.execute('''
          assert(next(objects) == nil)
          panel:mount(); local root = objects["demo.root"]
          panel:mount(); assert(objects["demo.root"] == root)
          panel:setText([[<tag a="b">&'</tag>]])
          assert(objects["demo.status"].text == "&lt;tag a=&quot;b&quot;&gt;&amp;&#39;&lt;/tag&gt;")
          panel:resize(300, 200); assert(root.width == 300 and root.height == 200)
          local old = objects["demo.status"].callback
          old(); assert(clicks == 1)
          panel:destroy(); panel:destroy(); assert(next(objects) == nil and deletions == 2)
          old(); assert(clicks == 1)
          panel:mount(); old(); assert(clicks == 1)
          objects["demo.status"].callback(); assert(clicks == 2)
        ''')

    def test_partial_mount_failure_cleans_root_and_can_retry(self):
        self.lua.execute('''
          failLabel = true
          local ok, err = pcall(function() panel:mount() end)
          assert(not ok and tostring(err):find("label failed"))
          assert(next(objects) == nil)
          failLabel = false; panel:mount(); assert(objects["demo.status"])
          assert(not pcall(function() panel:resize(0, 1) end))
          assert(not pcall(function() panel:resize(0/0, 1) end))
        ''')

    def test_destroy_does_not_delete_another_panel(self):
        self.lua.execute('''
          local other = Panel.new(api, "other", function() end)
          other:mount(); panel:mount(); panel:destroy()
          assert(objects["other.root"] and objects["other.status"])
          assert(objects["demo.root"] == nil)
        ''')


class MapperTests(unittest.TestCase):
    def setUp(self):
        self.lua = runtime("mudlet-mapper-development/examples/room_plan.lua", "Planner")
        self.lua.execute('''
          hashes = {}; reverse = {}; rooms = {}; metadata = {}; candidate = 42
          api = {
            getRoomIDbyHash = function(hash) return hashes[hash] or -1 end,
            getRoomHashByID = function(id) return reverse[id] end,
            getRoomName = function(id) return rooms[id] end,
            getRoomUserData = function(id, key) return (metadata[id] or {})[key] or "" end,
            createRoomID = function() return candidate end
          }
          function remember(plan)
            rooms[plan.roomID] = ""; reverse[plan.roomID] = plan.hash; hashes[plan.hash] = plan.roomID
            metadata[plan.roomID] = {[plan.ownerKey] = plan.owner,
              [plan.sourceKey] = plan.source, [plan.externalKey] = plan.externalID}
          end
        ''')

    def test_planning_is_read_only_and_preserves_external_identity(self):
        self.lua.execute('''
          local a = assert(Planner.planRoom(api, "demo", "world", "007"))
          local b = assert(Planner.planRoom(api, "demo", "world", "7"))
          assert(a.hash ~= b.hash and a.roomID == 42 and b.roomID == 42)
          assert(a.action == "create" and next(rooms) == nil and next(hashes) == nil)
          remember(a)
          local reused = assert(Planner.planRoom(api, "demo", "world", "007"))
          assert(reused.action == "reuse" and reused.roomID == 42)
        ''')

    def test_foreign_and_inconsistent_identities_are_not_adopted(self):
        self.lua.execute('''
          local a = assert(Planner.planRoom(api, "demo", "world", "007")); remember(a)
          metadata[42][a.ownerKey] = "other"
          local plan, err = Planner.planRoom(api, "demo", "world", "007")
          assert(plan == nil and err:find("ownership"))
          metadata[42][a.ownerKey] = "demo"; reverse[42] = "different"
          plan, err = Planner.planRoom(api, "demo", "world", "007")
          assert(plan == nil and err:find("reverse"))
          reverse[42] = a.hash; rooms[42] = nil
          plan, err = Planner.planRoom(api, "demo", "world", "007")
          assert(plan == nil and err:find("missing"))
        ''')

    def test_bad_candidates_and_stale_hashes_fail_without_mutation(self):
        self.lua.execute('''
          candidate = 0
          local plan = Planner.planRoom(api, "demo", "world", "1"); assert(plan == nil)
          candidate = 42; reverse[42] = "stale"
          local err; plan, err = Planner.planRoom(api, "demo", "world", "1")
          assert(plan == nil and err:find("stale"))
          assert(next(rooms) == nil)
        ''')


if __name__ == "__main__":
    unittest.main()
