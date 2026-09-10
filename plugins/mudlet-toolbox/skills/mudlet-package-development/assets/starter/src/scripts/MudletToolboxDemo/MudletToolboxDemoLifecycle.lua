MudletToolboxDemo = MudletToolboxDemo or { calls = 0, active = false }

function MudletToolboxDemo.start()
  MudletToolboxDemo.active = true
end

function MudletToolboxDemo.status()
  MudletToolboxDemo.calls = MudletToolboxDemo.calls + 1
  echo(string.format("Mudlet Toolbox demo: %s; calls=%d\n",
    MudletToolboxDemo.active and "ready" or "inactive", MudletToolboxDemo.calls))
end

function MudletToolboxDemoLifecycle(event, packageName)
  if event == "sysLoadEvent"
      or (event == "sysInstallPackage" and packageName == "@PKGNAME@") then
    MudletToolboxDemo.start()
  elseif event == "sysUninstallPackage" and packageName == "@PKGNAME@" then
    MudletToolboxDemo = nil
    MudletToolboxDemoLifecycle = nil
  end
end
