"""Pure Lua and ownership tests; these do not emulate Mudlet's native engine."""

from pathlib import Path
import unittest

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "mudlet-toolbox" / "skills"


class DelayedActionTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute('''
          pending = {}; nextId = 0; output = {}
          function tempTimer(delay, callback)
            nextId = nextId + 1; pending[nextId] = callback; return nextId
          end
          function killTimer(id) pending[id] = nil end
          function fire(id) local f = pending[id]; pending[id] = nil; if f then f() end end
          function emit(text) table.insert(output, text) end
        ''')
        module = self.lua.execute((SKILLS / "mudlet-lua-scripting/assets/delayed_action.lua").read_text())
        self.lua.globals().action = module.new(self.lua.globals().emit, 0.2)

    def test_replacement_and_captured_input(self):
        self.lua.execute('''
          matches = {"whole", "first"}; action:schedule(matches[2])
          local old = action.timer
          matches[2] = "second"; action:schedule(matches[2])
          local current = action.timer
          matches[2] = "changed later"
          fire(old); assert(#output == 0)
          fire(current); assert(output[1] == "second" and #output == 1)
          assert(action.timer == nil)
        ''')

    def test_cancel_is_idempotent_and_preserves_unowned_timer(self):
        self.lua.execute('''
          local unrelated = tempTimer(1, function() emit("other") end)
          action:schedule("cancelled"); local owned = action.timer
          action:cancel(); action:cancel(); fire(owned); fire(unrelated)
          assert(#output == 1 and output[1] == "other")
        ''')

    def test_failed_registration_does_not_claim_pending_work(self):
        self.lua.execute('''
          tempTimer = function() return nil, "unavailable" end
          local ok, err = action:schedule("input")
          assert(ok == nil and err == "unavailable" and action.timer == nil)
        ''')


class StarterTests(unittest.TestCase):
    def test_package_events_and_editor_reload_preserve_state(self):
        lua = LuaRuntime(unpack_returned_tuples=True)
        lua.execute('output = {}; function echo(s) table.insert(output, s) end')
        source = (SKILLS / "mudlet-package-development/assets/starter/src/scripts/MudletToolboxDemo/MudletToolboxDemoLifecycle.lua").read_text().replace("@PKGNAME@", "MudletToolboxDemo")
        lua.execute(source)
        lua.execute('''
          MudletToolboxDemoLifecycle("sysInstallPackage", "Other")
          assert(MudletToolboxDemo.active == false)
          MudletToolboxDemoLifecycle("sysInstallPackage", "MudletToolboxDemo")
          MudletToolboxDemo.status()
          assert(output[1] == "Mudlet Toolbox demo: ready; calls=1\\n")
        ''')
        lua.execute(source)
        lua.execute('''
          assert(MudletToolboxDemo.calls == 1)
          MudletToolboxDemoLifecycle("sysUninstallPackage", "Other")
          assert(MudletToolboxDemo.active)
          MudletToolboxDemoLifecycle("sysLoadEvent", false)
          assert(MudletToolboxDemo.calls == 1)
          MudletToolboxDemoLifecycle("sysUninstallPackage", "MudletToolboxDemo")
          assert(MudletToolboxDemo == nil and MudletToolboxDemoLifecycle == nil)
        ''')
        lua.execute(source)
        lua.execute('MudletToolboxDemoLifecycle("sysLoadEvent"); assert(MudletToolboxDemo.active)')


if __name__ == "__main__":
    unittest.main()
