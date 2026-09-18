# Geyser manual topic index

This index routes every heading in the official [Geyser practical manual](https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser), reviewed at revision `oldid=21692`, to maintained guidance. Use the live localized page for current examples and the [technical API index](https://www.mudlet.org/geyser/files/index.html) for current method signatures. The live API is rolling documentation and can be newer than the verified Mudlet 5.0.1 source baseline.

Evidence labels:

- **Static**: source, syntax, ownership, or pure-state checks are meaningful offline.
- **Native**: a disposable Mudlet profile is required for rendering, Qt input, windows, filesystem persistence, or native cleanup.
- **Connected**: an actual game/server session is additionally required for negotiated protocol data or commands.

| Manual section and topics | Local guidance | Baseline and evidence |
| --- | --- | --- |
| Introduction: motivation, main features, picture assets, constraint format, constraint math | [Foundations](foundations-layouts.md#constraint-model), [lifecycle/assets](layout-lifecycle.md#shared-borders-assets-and-persistence) | Static review; native geometry/assets. |
| Geyser elements and technical manual | [Technical companion classes](foundations-layouts.md#technical-companion-classes) | Verify API against target release. |
| Container: create, nest, align from bottom/right | [Root, Container, and hierarchy](foundations-layouts.md#root-container-and-hierarchy) | Static hierarchy; native geometry. |
| Label basics: text colors, font size, parent, images/stretch/alignment, show/hide, clickable images, styles | [Label content](labels-styles-interaction.md#label-content-and-formatting), [images](labels-styles-interaction.md#images-transparency-and-cursors) | Native rich text, CSS, image, and input. |
| Label advanced: tooltips/inheritance, alignment, wrap, hover, checkbox, sprites, whitespace/newlines, transparency, cursors | [Styles](labels-styles-interaction.md#styles-and-geyserstylesheet), [interaction](labels-styles-interaction.md#click-hover-and-state-controls), [tooltips](labels-styles-interaction.md#tooltips-and-visibility) | Static state; native selector/input/rendering. |
| Flyout Labels: demo and layout directions | [Flyout labels](labels-styles-interaction.md#flyout-labels) | Native hover/click/layout. |
| Label right-click menu: style, action, direct access, full example, coexistence with left-click | [Right-click menus](labels-styles-interaction.md#right-click-menus) | Native event/menu behavior; connected for sends. |
| Required Geyser names | [Lifecycle ownership](layout-lifecycle.md#own-the-complete-ui-lifecycle) | Static inventory; native reload/delete. |
| StyleSheet: create, CSS string, target, set/get property, table forms, reset, inheritance | [Styles and StyleSheet](labels-styles-interaction.md#styles-and-geyserstylesheet) | Static data; native Qt result. |
| MiniConsole: text, color-copy, clear, edit, gag, clickable menus, background, command line/action | [MiniConsole](consoles-gauges-input.md#miniconsole-construction-and-output), [copy/gag](consoles-gauges-input.md#copy-edit-redirect-and-gag), [links](consoles-gauges-input.md#links-and-menus-in-consoles), [input](consoles-gauges-input.md#miniconsole-command-line) | Native trigger/selection/focus; connected for sends. |
| Gauge: update, style, orientation, simple colors, click/click-through, tooltip | [Gauge](consoles-gauges-input.md#gauge-values-and-presentation) | Static validation; native rendering/input. |
| HBox/VBox | [Automatic layouts](foundations-layouts.md#hbox-and-vbox) | Static hierarchy; native policies/geometry. |
| UserWindow: floating, docked, autoDock, platform styling, container behavior | [UserWindow](windows-adjustable-mapper.md#userwindow) | Native platform/window/layout persistence. |
| CommandLine: create, bind action, style, extra line in adjustable layout | [Standalone CommandLine](consoles-gauges-input.md#standalone-geysercommandline) | Static callback ownership; native focus/history/sends. |
| Adjustable.Container: create, key functions, constraints, title, auto-save/load, all-container operations | [Selection](windows-adjustable-mapper.md#adjustablecontainer-selection), [persistence](windows-adjustable-mapper.md#titles-saveload-and-all-container-operations) | Native mouse/menu/filesystem/restart. |
| Adjustable storage: custom directory, slot, saved-file deletion | [Persistence](windows-adjustable-mapper.md#titles-saveload-and-all-container-operations) | Static path scope; native save/load/reset. |
| Adjustable menu/custom items, lock styles, themes | [Menus and locking](windows-adjustable-mapper.md#menus-locking-and-styles) | Native menu/lock/accessibility. |
| Adjustable border attachment, movable frame, ScrollBox | [Borders](windows-adjustable-mapper.md#borders-and-connected-frames), [ScrollBox](windows-adjustable-mapper.md#scrollbox) | Native shared border/scroll behavior. |
| Change Container | [Moving and changing parents](foundations-layouts.md#moving-and-changing-parents), [native boundary](windows-adjustable-mapper.md#changecontainer) | Static ownership; native reparent/focus/clip. |
| Geyser.Mapper | [Geyser.Mapper](windows-adjustable-mapper.md#geysermapper) | Native mapper/docking; connected for live room sync. |
| Tutorial: Hello World, Containers, VBox/HBox | [Foundations](foundations-layouts.md), [composition](layout-lifecycle.md#hello-world-and-nested-containers) | Static construction; native geometry. |
| Clickable Compass walkthrough: assets, script, screen size, namespace, parent, style, grid, callback, hover, grid styles, square resize | [Compass pattern](layout-lifecycle.md#clickable-compass-or-image-control), [responsive pattern](layout-lifecycle.md#responsive-panel-and-resize-handle) | Static ownership/assets; native pointer/resize; connected for movement sends. |
| Tabbed Window walkthrough: script, namespace, main container, HBox, labels, tab windows, callback, content | [Tabs](layout-lifecycle.md#tabs) | Static state/routing; native click/visibility/scroll. |
| Historical resize-label walkthrough | [Responsive panel](layout-lifecycle.md#responsive-panel-and-resize-handle) | Prefer Adjustable.Container where user resizing is intended. |

<!-- geyser-topics: introduction motivation main-features assets constraints-format constraint-math -->
<!-- geyser-topics: geyser-elements technical-manual -->
<!-- geyser-topics: container container-create container-nesting container-negative-alignment -->
<!-- geyser-topics: label label-basic label-color label-font-size label-parent label-image label-image-stretch label-image-alignment label-show-hide label-clickable-images label-styling -->
<!-- geyser-topics: label-tooltip label-tooltip-inheritance label-content-alignment label-wordwrap label-hover label-checkboxes label-sprites label-whitespace label-transparency label-cursor -->
<!-- geyser-topics: label-flyouts label-flyout-demo label-flyout-layouts -->
<!-- geyser-topics: label-right-click-menu label-menu-style label-menu-action label-menu-access label-menu-example label-menu-existing-click label-name -->
<!-- geyser-topics: stylesheet stylesheet-basic stylesheet-css stylesheet-target stylesheet-set stylesheet-get stylesheet-table-get stylesheet-table-set stylesheet-reset stylesheet-inheritance -->
<!-- geyser-topics: miniconsole miniconsole-text miniconsole-copy-color miniconsole-clear miniconsole-edit miniconsole-gag miniconsole-clickable miniconsole-background miniconsole-commandline miniconsole-command-action -->
<!-- geyser-topics: gauge gauge-update gauge-style gauge-orientation gauge-colors gauge-click gauge-tooltip -->
<!-- geyser-topics: hbox-vbox -->
<!-- geyser-topics: userwindow userwindow-floating userwindow-docked userwindow-autodock userwindow-style userwindow-container -->
<!-- geyser-topics: commandline commandline-create commandline-action commandline-style commandline-extra -->
<!-- geyser-topics: adjustable adjustable-create adjustable-key-functions adjustable-constraints adjustable-title adjustable-autosave adjustable-all adjustable-custom-storage adjustable-custom-directory adjustable-custom-slot adjustable-delete-save adjustable-menu adjustable-custom-menu adjustable-lock-styles adjustable-style adjustable-border adjustable-frame adjustable-scrollbox -->
<!-- geyser-topics: change-container mapper -->
<!-- geyser-topics: tutorial tutorial-hello tutorial-containers tutorial-boxes -->
<!-- geyser-topics: walkthroughs walkthrough-compass compass-assets compass-script compass-screen-size compass-namespace compass-parent compass-style compass-grid compass-callback compass-hover compass-grid-styles compass-resize -->
<!-- geyser-topics: walkthrough-tabs tabs-script tabs-namespace tabs-container tabs-hbox tabs-label tabs-windows tabs-callback tabs-content -->
<!-- geyser-topics: walkthrough-resize-label -->

## Technical API topics beyond the practical page

The technical index also lists `Geyser.Button`, `Geyser.Color`, `Geyser.TextEdit`, `Geyser.Window`, `Geyser.SetConstraints`, `GeyserReposition`, `Geyser.Util`, and upstream `Geyser.Tests`. They are routed through [technical companion classes](foundations-layouts.md#technical-companion-classes). Their presence in current docs does not establish availability or identical behavior in Mudlet 5.0.1.

## Applying this index

Read only the focused references needed for the task, plus lifecycle guidance for any component that owns native objects. If a manual example conflicts with the package's target version, ownership rules, or requested behavior, preserve the product contract and verify the target API rather than copying the example literally. Record native or connected checks as not run when no authorized disposable profile/session was used.
