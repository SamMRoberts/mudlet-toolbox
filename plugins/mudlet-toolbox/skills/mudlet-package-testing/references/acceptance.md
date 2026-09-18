# Acceptance matrix

| Layer | Checks | What passing establishes |
| --- | --- | --- |
| Container | ZIP members, bounded size, paths, XML well-formedness, expected object/resource inventory | Selected artifact structure is sane; no Lua was executed. |
| Syntax | Correct Lua language version; generated/embedded code included | The selected interpreter can parse the code. |
| Pure logic | Positive, negative, missing, partial, and malformed input; cancellation and state transitions | The tested functions behave under the harness assumptions. |
| Native engine | Install, alias/trigger invocation, real event dispatch, timer scheduling | The actual Mudlet runtime accepts and invokes the tested code. |
| UI | Rendering, resizing, input focus, callbacks, scrolling, reload, cleanup | The observed native interface behaves in the tested configuration. |
| Connected game | Protocol exchange and gameplay-specific behavior | The tested server/profile exchange works; offline fixtures alone cannot prove this. |

## Lifecycle scenarios

- **Fresh install:** inventory expected objects/assets; check no missing-dependency errors; verify any introduction is filtered to the exact package and occurs only on install; invoke a harmless documented command.
- **Profile restart:** ensure initialization runs when no install event occurs. Confirm saved settings if persistence is part of the feature.
- **Editor save/reinitialize:** run the actual path twice. Confirm a single handler/timer/window instance and no duplicate output.
- **Module workflow:** test Module Manager separately when promised, including priority and synchronization. Preserve the source file because module saves can rewrite it.
- **Upgrade:** install the intended replacement through its supported update path. Check migrated settings and removal of obsolete owned resources.
- **Partial start failure:** a missing dependency or failed registration should produce an actionable error and no orphaned callbacks.
- **Uninstall:** ensure owned work stops, UI disappears, and shared profile resources remain correct. Pending timers must not access deleted objects.
- **Coexistence:** install two packages, exercise both, remove one, and exercise the survivor. Filter lifecycle events by the appropriate package/module identity.

For callbacks, distinguish observing the callback's side effect from merely observing that its name was registered. For timer cleanup, advance the event loop beyond the timer delay and check nothing fires. Do not run install and uninstall back-to-back in one callback and claim normal lifecycle behavior was tested.

## Replays

Keep fixtures small and representative. Store the original line sequence, ANSI where relevant, and expected state/output. A parser test is separate from a Mudlet regex-engine test. `feedTriggers` may activate other scripts, including sends; use isolated offline profiles and capture outgoing actions when relevant.

Synthetic GMCP tests need the correct protocol table shape and event order, including missing/partial fields and disconnect. They prove the handler under those inputs, not server negotiation. Avoid presenting guessed game schemas as standards.

`feedTriggers` and its formatted variants are replay tools, not a production integration mechanism. Keep replay in a disconnected or otherwise isolated profile, capture unintended sends, and make production adapters call shared functions directly.

## Best-practices review

- **Lua/state:** internal values are local; required globals share one unique namespace; recompilation preserves intended state without stacking resources; `_G` is not used as a convenience registry.
- **Input/performance:** aliases and triggers call functions directly; `expandAlias` is used only for intentional alias-stack processing; stable literal gates protect demonstrably expensive regex triggers without changing matches.
- **Ownership:** temporary IDs or named registrations are retained and removed by their owner; start/reload/uninstall do not duplicate timers, handlers, triggers, or UI.
- **UI:** widget names are owner-qualified; scalable relationships use parent-relative constraints; user-adjustable containers are considered when appropriate; fonts/assets are packaged; uninstall reverses owned layout changes.
- **Package/protocol:** install guidance is package-filtered; public custom events have documented contracts; optional modules have intentional boundaries; `gmod` requests are paired; paths use `/`; update distribution is explicit.
- **Mapper:** generic mapper customizations live outside the managed `generic_mapper` folder and survive its upgrade.

Review observable behavior and project intent rather than scanning for particular words or APIs. A recommendation can be inapplicable; record that decision instead of forcing unnecessary abstractions.

## Geyser UI review

Select the rows that apply to the interface; mark unrun native/connected checks explicitly.

| Concern | Static or stub evidence | Native disposable-profile acceptance |
| --- | --- | --- |
| Ownership/lifecycle | Unique owner-qualified names; one retained instance; failure cleanup; stale callback guards; producer teardown before root deletion | No duplicate native objects after save/reload; widgets disappear on uninstall; another package survives. |
| Constraints/containers | Parent tree, units, negative-anchor math, HBox/VBox policies, intended `changeContainer` destinations | Geometry at narrow/wide/high-DPI sizes; show/hide, clipping, z-order, and reparenting. |
| Label/StyleSheet | External text escaped; packaged image/font/cursor paths; scoped selectors; owned animation timers/menu callbacks | Rich text, wrap/alignment, tooltip inheritance, images, hover/click/right-click, flyouts, cursors, animation cancellation. |
| MiniConsole | Plain versus markup output is intentional; bounded buffer policy; capture/gag trigger is narrow | ANSI/color copy, selection edits, exact-line gagging, links, scrolling, background image, buffer behavior. |
| Gauge | Finite values, positive maximum, explicit out-of-range/stale policy, escaped text | Orientation/color/style, tooltip, click layers, and click-through routing. |
| CommandLine | Default send/alias behavior versus custom action is explicit; input stays data | Focus, history, input method, command echo, aliases, captured outgoing actions, accessibility. |
| UserWindow | Stable name, supported platform/version, saved-layout policy, child ownership | Float/dock/autoDock, title/frame platform behavior, multi-monitor restart and off-screen recovery. |
| Adjustable/ScrollBox | Owned persistence directory/slots, scoped operations, reversible custom menu/lock/border choices | Drag/resize/minimize/hide/lock, save/load/reset, menus, border/frame behavior, scroll/clipping. |
| Mapper display | Display ownership separated from map-data ownership; no inferred import/path/movement result | Coexistence, embedded/docked/floating display, saved position, current-room follow, teardown. |

For command-capable callbacks, capture unintended sends while offline. Connected-game acceptance is separate and should cover only the explicit protocol or gameplay contract.

## Evidence record

Record the source revision or working-tree identity, archive hash, tool versions, profile name, connected/offline state, commands, expected/actual outcome, and limitations. Mark checks `passed`, `failed`, or `not run`; never convert unavailable native checks into passes because a stub succeeded.

Useful regression cases include duplicate timer registration, another package's uninstall event, settings surviving replacement, changed room-ID mappings, absent GMCP fields, and repeated UI teardown. Choose cases based on the changed behavior rather than testing headings or implementation wording.
