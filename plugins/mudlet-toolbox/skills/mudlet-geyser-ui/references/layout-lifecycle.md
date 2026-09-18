# Layout, lifecycle, and composition patterns

## Own the complete UI lifecycle

Names are native window identifiers as well as Geyser tracking keys. Use an owner-qualified prefix for every object, such as `package.panel.root` and `package.panel.status`. Names must be globally unique within the profile, including UserWindows and objects from other packages. Avoid ordinary instance names ending in `Class`, which have special constructor handling in the 5.0.1 implementation.

Keep one retained instance in the package's established namespace. Split responsibilities into:

- `mount`: validate capabilities, create the owned root, create children, bind callbacks, and register producers;
- `render`: validate and copy external state, then update existing widgets;
- `layout`: move, resize, or reparent existing widgets without rebuilding them;
- `destroy`: stop producers, delete the owned tree, remove owned persistence, and restore shared layout only when the component still owns it.

Geyser constructors allocate immediately. Do not create widgets at module load merely because a script was compiled. On construction failure, delete the partial root or every created child, leave no active callbacks, and preserve enough state to retry cleanup. A repeated initialization event should update or return the current instance; it should not allocate another object with the same names.

In Mudlet 5.0.1, `container:delete()` recursively removes children and type-specific native widgets. Capability-check cleanup for other releases. Do not edit Geyser's internal tracking tables. `hide()` only changes visibility. Stop owned timers and event/protocol handlers before deleting their target widgets, then remove the uninstall handler itself. Filter `sysUninstallPackage` by exact package name; modules use different lifecycle events.

## Data, output, and callbacks

Treat protocol values, game text, settings, filenames, and command-line input as untrusted data. Copy the needed values into component state rather than retaining mutable protocol tables. Escape label/gauge rich text for HTML; use plain `echo` for plain MiniConsole text; interpret `cecho`/`decho`/`hecho` markup only when the source is intentionally markup. Do not interpolate data into Lua callback strings, command links, or stylesheets.

Prefer function callbacks and closures. Guard them with an instance generation or active flag so a retained native callback cannot act after teardown or remount. Mouse details may arrive after bound callback arguments; inspect the actual event signature when those details matter. Keep command dispatch behind an application function so a label, alias, key, or CommandLine can reuse it without re-entering the alias engine unexpectedly.

Validate finite gauge values and positive maxima. Decide whether out-of-range values are clamped, rejected, or displayed as an explicit over/under state. Missing values are not zero. If an update is rejected, mark the display stale or unknown rather than leaving an apparently current reading silently.

## Composition patterns

### Hello world and nested containers

Start with a named Label for a visual smoke test, then introduce a named Container only when it represents a real ownership or layout boundary. Child coordinates are relative to their direct parent. Use `container:flash()` during diagnosis rather than leaving debugging decoration in production.

### Clickable compass or image control

Package redistributable images under the extension and build their paths from the installed package/profile location with `/` separators. Use a parent Container or Label with a 3-by-3 HBox/VBox or percentage grid. Bind direction functions directly and apply hover/pressed styles without generating Lua strings from direction data. A compass sends commands only when that is an explicit product behavior; construction itself has no server side effect.

### Tabs

Create an owned header HBox, one selector Label per tab, and one content Container/MiniConsole per view. A selector callback hides the previous content and shows the selected content. Keep hidden buffers alive and route each message exactly once. Preserve the selected tab across ordinary renders; persist it only when the product promises that setting. There is no separate Geyser tab primitive implied by this pattern.

### Responsive panel and resize handle

Use parent-relative constraints, HBox/VBox policies, or an `Adjustable.Container` before writing a custom resize handle. The manual's historical resize-label walkthrough now directs readers to adjustable containers. If a custom square/aspect-ratio layout remains necessary, retain one resize handler, read the current parent dimensions, update existing objects, and avoid recreating the tree or writing back the main window size.

### Detachable workspace

Keep content under one owned container and move it with `changeContainer` only after confirming destination support and name ownership. Treat moving between the main root, UserWindow, Adjustable.Container, and ScrollBox as a native acceptance boundary: constraints stay attached to the object but geometry, focus, clipping, and visibility may differ.

## Shared borders, assets, and persistence

Setting a Mudlet border is profile-wide state. Record what the component changed and restore it only if ownership/current-state checks show another package has not replaced it. Adjustable border attachment and connected frames require the same coordination. Do not blindly restore a startup snapshot over a newer user or package choice.

Package every required image and redistributable font. Do not depend on the developer's desktop path or installed font collection. Keep durable user layout/settings outside replaceable package assets and namespace filenames by package/component. Decide separately whether uninstall removes saved layout; default to preserving user-authored settings unless the package contract promises removal or offers a reset.

## Example contracts

`owned_panel.lua` returns `Panel.new(api, owner, onClick)`. It creates a 100% root and Label only from `mount()`, escapes label text, accepts an explicit positive pixel resize, rejects stale callbacks, and deletes its owned root. It targets the 5.0.1 recursive-delete contract.

`responsive_dashboard.lua` returns `Dashboard.new(api, owner, onSubmit)`. It composes Container, HBox, VBox, Label, Gauge, MiniConsole, and CommandLine objects, retains validated render state across remount, accepts plain console text, guards stale input callbacks, and deletes only its root. Its injected API is suitable for pure Lua ownership tests; it does not simulate native layout or input behavior.

## Acceptance boundary

Offline checks can establish construction order, names, state validation, escaped output, callback guards, and cleanup calls. Only a real disposable Mudlet profile can establish constraint geometry, CSS/selector behavior, mouse arguments, click-through, focus and history, selection/edit/gag effects, scrolling, UserWindow docking, saved layouts, Adjustable.Container menus/dragging, border attachment, mapper rendering, native deletion, and coexistence. Connected-game checks are additionally required for protocol-driven freshness and commands sent to a server.
