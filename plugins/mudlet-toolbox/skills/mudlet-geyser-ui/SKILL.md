---
name: mudlet-geyser-ui
description: Build, refactor, or debug Mudlet Geyser interfaces, including widget ownership, responsive layout, callbacks, and reload or teardown behavior.
---

# Mudlet Geyser UI

Start with the actual interface: inspect its widget tree, runtime release, screenshots if available, naming scheme, data sources, and lifecycle entrypoints. Preserve existing interactions and the user's selected UI scope.

1. Give each component an owner namespace and one retained instance. Inventory its widgets, handlers, timers, callbacks, and any shared borders or windows it changes.
2. Separate construction, rendering, layout, and destruction. Build once, update existing widgets, and dispose of the old instance before rebuilding.
3. Prefer parent-relative percentage constraints. Add a resize event handler only for layout work the constraints cannot express. Reflow without recreating widgets or writing back the main window size. When user-controlled placement is part of the product, consider an `Adjustable.Container` instead of locking the layout.
4. Bind function callbacks to owned state. Escape external text for the destination widget, and validate data before rendering gauges or enabling actions.
5. Tear down event/timer producers before widgets. Choose cleanup supported by the target version; hiding is not deletion. Restore owned border/layout changes on uninstall and restore shared settings only under an explicit ownership arrangement. Package any required fonts rather than assuming host availability.
6. Check repeated mount, update, resize, destroy, reload, and uninstall paths. Separate stub evidence from live geometry, focus, mouse, scroll, and native-widget acceptance.

Read [layout and lifecycle](references/layout-lifecycle.md) for the specific pitfalls. Adapt [owned_panel.lua](examples/owned_panel.lua) for a small component with escaped label text and guarded callbacks. It returns a module; construction begins only at `mount()`.

The reference uses verified Mudlet 5.0.1 semantics. Other targets need capability checks and appropriate cleanup adapters. Keep raw research outside the plugin.
