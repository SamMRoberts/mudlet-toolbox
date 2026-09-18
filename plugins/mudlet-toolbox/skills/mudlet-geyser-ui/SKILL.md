---
name: mudlet-geyser-ui
description: Build, refactor, or debug Mudlet Geyser interfaces, including layouts, widgets, styles, consoles, windows, adjustable containers, mapper displays, callbacks, persistence, and teardown.
---

# Mudlet Geyser UI

Start with the actual interface: inspect its widget tree, target Mudlet release and platforms, screenshots, naming scheme, data sources, saved layout state, and lifecycle entrypoints. Preserve existing interactions and the user's selected UI scope.

1. Give each component an owner-qualified name and one retained instance. Inventory its widgets, handlers, timers, callbacks, native windows, saved files, and shared borders.
2. Separate construction, rendering, layout, and destruction. Build once, update existing widgets, and dispose of the old instance before rebuilding. Make partial construction failure clean up what it created.
3. Prefer parent-relative constraints and automatic containers. Add resize handlers only for relationships constraints cannot express. Use `Adjustable.Container` only when user-controlled placement is part of the product contract.
4. Bind function callbacks to owned state. Treat command-line input and protocol/game text as data, escape for the destination widget, and validate gauge values and actions before rendering or sending.
5. Stop producers before deleting widgets. Hiding is not teardown. Restore owned border/layout changes on uninstall, preserve user state deliberately, and package required fonts and images with portable paths.
6. Verify repeated mount, update, reparent, resize, destroy, reload, and uninstall. Keep static/stub evidence separate from native geometry, styling, focus, mouse, scroll, docking, persistence, and mapper acceptance.

## Route to the needed reference

- Start with the [manual topic index](references/topic-index.md) for complete coverage and version/evidence routing.
- Read [foundations and automatic layouts](references/foundations-layouts.md) for constraints, containers, HBox/VBox, resizing, reparenting, and technical companion classes.
- Read [labels, styles, and interaction](references/labels-styles-interaction.md) for rich text, images, `StyleSheet`, tooltips, callbacks, flyouts, sprites, and menus.
- Read [consoles, gauges, and input](references/consoles-gauges-input.md) for `MiniConsole`, `Gauge`, and `CommandLine` behavior.
- Read [windows, adjustable containers, and mapper](references/windows-adjustable-mapper.md) for `UserWindow`, persistence, docking, borders, `ScrollBox`, and `Geyser.Mapper`.
- Read [layout, lifecycle, and composition patterns](references/layout-lifecycle.md) for ownership, cleanup, tabs, compass-style controls, assets, and acceptance boundaries.

Adapt [owned_panel.lua](examples/owned_panel.lua) for a minimal owned component. Adapt [responsive_dashboard.lua](examples/responsive_dashboard.lua) when a composed Container/HBox/VBox, Label, Gauge, MiniConsole, and CommandLine example is useful. Both return modules and allocate no UI until `mount()`.

The references synthesize the official Geyser manual and technical API with Mudlet 5.0.1 as the verified source baseline. Check the requested runtime before using version- or platform-dependent behavior, and consult the linked live documentation for APIs outside that baseline.
