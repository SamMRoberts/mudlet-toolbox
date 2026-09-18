MudletToolboxDemo = MudletToolboxDemo or { calls = 0, active = false }
local PACKAGE_NAME = "@PKGNAME@"

function MudletToolboxDemo.start()
  MudletToolboxDemo.active = true
end

function MudletToolboxDemo.status()
  MudletToolboxDemo.calls = MudletToolboxDemo.calls + 1
  echo(string.format("Mudlet Toolbox demo: %s; calls=%d\n",
    MudletToolboxDemo.active and "ready" or "inactive", MudletToolboxDemo.calls))
end

function MudletToolboxDemoLifecycle(event, packageName)
  if event == "sysLoadEvent" then
    MudletToolboxDemo.start()
  elseif event == "sysInstallPackage" and packageName == PACKAGE_NAME then
    MudletToolboxDemo.start()
    echo("Mudlet Toolbox demo installed. Run toolbox-demo for status.\n")
  elseif event == "sysUninstallPackage" and packageName == PACKAGE_NAME then
    MudletToolboxDemo = nil
    MudletToolboxDemoLifecycle = nil
  end
end
