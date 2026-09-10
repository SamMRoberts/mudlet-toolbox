# Layout, naming, and lifecycle

## Own the widget tree

Names are native window identifiers as well as Geyser tracking keys. Use an owner-qualified prefix for every child, such as `component.instance.root` and `component.instance.status`. Do not reuse another component's names or infer ownership merely because a global or named widget exists. In 5.0.1, names ending in `Class` have special constructor handling; avoid that suffix for ordinary instances.

Keep instance references in the caller's established namespace. Before replacing an instance, run its cleanup; losing the reference loses ownership of native widgets and closures. A repeated initialization event should update or return the existing instance. A new object with the same names is not a safe substitute for teardown.

`Geyser.Container:new(constraints, parent)` attaches to the supplied parent, or to Geyser's root when omitted. Constructor calls allocate/register immediately. Avoid them at module load time. Construct children under the owned root and record any resources outside that tree separately.

## Layout and rendering

Percent constraints refer to the parent, and plain numeric constraints are pixels. Negative offsets measure from the opposite edge. Offsetting a full-width child can put it outside its parent; account for inset space. Geyser already recalculates ordinary constrained layouts on resize. For custom breakpoints, use one owned `sysWindowResizeEvent` handler, read current dimensions, and resize/move existing objects. Filter user-window resize events separately when applicable; do not assume every resize describes the main console.

Keep gauges, text, and layout updates independent. Display missing values explicitly, avoid division by zero, and bound values according to the application contract. Label text is rich text: escape `&`, `<`, `>`, quotes, and apostrophes before inserting external text. MiniConsole color markup is a different output grammar; HTML escaping is not a general console sanitizer. Never interpolate server data into Lua callback source or executable command links.

A native mapper is a special widget, not a normal duplicable label. Confirm mapper parent and visibility behavior in the target runtime, particularly with ScrollBoxes, detached windows, and competing map displays. Do not certify nested placement from a Geyser object tree alone.

## Common widgets without new dependencies

| Need | Concrete entrypoints and workflow |
| --- | --- |
| Numeric gauge | Construct `Geyser.Gauge:new(constraints, parent)` once; update with `gauge:setValue(current, maximum, text)` and change text alone with `gauge:setText(text)`. Without a maximum, `current` is a percentage. Validate finite numbers and a positive maximum first; escape external text because the gauge uses labels. In 5.0.1 an invalid nonpositive/NaN maximum leaves the old reading unchanged and returns `nil, message`; explicitly mark stale/unknown data rather than leaving it apparently current. |
| Chat/history pane | Construct `Geyser.MiniConsole:new({name=ownedName, autoWrap=true, ...}, parent)`. Append plain text with `pane:echo(text)` or intentional color markup with `pane:cecho(text)`. Set a bounded history with `pane:setBufferSize(lineLimit, deletionBatch)`. Let `autoWrap` follow geometry; `pane:setWrap(columns)` is for manual wrapping and is rejected while auto-wrap is enabled in 5.0.1. |
| Chat tabs | Reuse an already-present tab/chat package through its verified API, or build owned label selectors and one container/miniconsole per tab. A selector callback hides inactive panes and shows the active pane with `:hide()`/`:show()`. Keep hidden buffers alive, route each message once, and delete all panes only on teardown. No tab package is required. |
| Action button | Use `Geyser.Label:new(constraints, parent)`, `label:echo(text)`, and `label:setClickCallback(function(...) ... end)`. Derive enabled/disabled styling and callback guards from the same state. Prefer calling an application action function; game commands remain explicit effects of that action. |

These entrypoints are verified for 5.0.1; check methods and behavior on other targets, especially wrapping and cleanup. Widget construction belongs to mount, incoming data to render, and tab selection to visibility changes.

## Callbacks and teardown

`label:setClickCallback(fn, ...)` delegates to the native label callback and retains the callback on the Lua object. Mouse event details arrive as a final argument after bound arguments. Prefer a function closure over a generated Lua string. Guard against callbacks belonging to a destroyed instance, especially if callbacks queue other work.

In 5.0.1, `container:delete()` recursively deletes children, removes Geyser tracking entries, then calls type-specific native cleanup. Label cleanup calls `deleteLabel`; native label destruction releases callback references. This does not remove unrelated anonymous event handlers or timers created by your component. Stop those explicitly before deleting the root. Do not edit Geyser's internal tracking tables to simulate destruction.

Capability-check the actual object's cleanup when supporting other releases. If recursive deletion is absent, implement and verify a type-specific cleanup adapter or narrow the supported runtime. `hide()` only changes visibility; do not silently use it as full teardown. Handle partial construction failure by cleaning up what was created, retaining enough state to retry cleanup if it fails.

Connect owner lifecycle to the appropriate startup and uninstall path. `sysUninstallPackage` receives `(eventName, packageName)`; filter the exact package name before destroying anything. Modules have distinct uninstall events, so do not promise module cleanup from a package-only hook. Remove the cleanup handler itself as part of teardown. Global borders, fonts, and shared mapper placement need coordinated ownership; blindly restoring a stale snapshot can overwrite another component's later change.

## Example and acceptance boundary

`Panel.new(api, owner, onClick)` returns an object with `mount(parent)`, `setText(text)`, `resize(width, height)`, and `destroy()`. Loading it and calling `new` have no UI effects. Inject `_G` or a fake `api.Geyser`. Required Geyser methods are `Container:new`, inherited `Container:delete` and `resize`, plus `Label:new`, `echo`, and `setClickCallback`.

The example requires recursive deletion, creates a `100%` root and label, and lets Geyser handle relative resize. It adds no resize handler or border changes. `setText` accepts a string and escapes it. `resize` accepts positive finite pixel dimensions as an explicit layout override. `mount` is idempotent while active; after destruction it can mount again. Callback generation guards prevent a retained old callback from acting on a remounted panel. Callers must supply a unique owner and destroy the old panel before creating a replacement with that owner.

Offline checks can establish lifecycle calls, naming, escaping, and callback guards. A real disposable profile is required to establish layout at narrow/wide sizes, actual mouse event arguments, focus/scroll behavior, deletion of native widgets, and coexistence with other packages. Run such checks only within the authorized task scope.
