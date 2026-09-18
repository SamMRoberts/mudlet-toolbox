# Windows, adjustable containers, and mapper

Use this reference for `Geyser.UserWindow`, `Adjustable.Container`, `Geyser.ScrollBox`, border attachment, saved layouts, and `Geyser.Mapper`. These features cross native-window, filesystem, or profile-wide layout boundaries and require native acceptance.

## UserWindow

`Geyser.UserWindow` is documented from Mudlet 4.6.1 and acts as a Container with MiniConsole behavior. It can host Labels, Gauges, MiniConsoles, Mappers, and other compatible Geyser objects. A separate MiniConsole is unnecessary when the UserWindow's own console surface meets the requirement.

Create a globally unique named window. A floating window uses its supplied geometry; a docked window can ignore creation position/size. Mudlet 4.8+ documentation includes title text, `setTitle`, `resetTitle`, `dockPosition`, `setDockPosition`, and auto-dock enable/disable. Valid dock positions include left, right, top, bottom, and floating in the practical manual. Feature-check methods for other targets.

`saveWindowLayout()` and `loadWindowLayout()` persist/restore native window placement. Create the named windows before loading their layout. Treat the saved layout as user state: define when it loads, whether a reset is offered, how renamed/removed windows migrate, and whether uninstall preserves it. Verify multi-monitor removal, scale changes, off-screen recovery, floating/docked transitions, and restart.

The manual documents UserWindow frame/title-area styles from Mudlet 4.10+ as Linux-only; Windows and macOS use native OS theming. Do not promise cross-platform frame CSS. Style child widgets separately and test all supported platforms.

## Adjustable.Container selection

Use `Adjustable.Container` when users should move, resize, minimize, hide, lock, or attach a panel. Use a normal Container when geometry is product-controlled or adjustment would break the UI. The practical manual marks Adjustable.Container as Mudlet 4.8+.

Give each adjustable container a stable owner-qualified name because its saved state is keyed by identity. It accepts ordinary Container constraints plus its own title, button, padding, menu, persistence, and style options. Child content should normally fill the inner content region using parent-relative constraints rather than assuming the outer frame size.

## Titles, save/load, and all-container operations

Set initial `titleText` or call `setTitle`; call the target release's reset form when returning to the default. Saved state documented by the manual includes position, size, minimized, locked, lock style, padding, and hidden state.

`autoLoad` and `autoSave` control automatic persistence. Disabling them does not necessarily disable manual `save`/`load` or menu operations. Decide whether the package or the user controls state before choosing defaults. Avoid auto-loading stale geometry before child construction can tolerate it.

Use instance `save(slot)`/`load(slot)` for one panel and `Adjustable.Container:saveAll(slot)`/`loadAll(slot)` only when the package intentionally coordinates every relevant adjustable container. `showAll`/`doAll` are similarly broad; do not affect foreign containers. If the upstream implementation's global registry cannot scope these operations by owner, iterate only the package's retained instances instead.

Namespace custom storage below a package/user-settings directory using portable `/` paths. Validate and create only the intended directory. A custom slot can represent layouts such as default/combat, but loading a slot is a visible user-state change. `deleteSaveFile` is destructive; expose it as an explicit reset and target only the owned container/slot.

## Menus, locking, and styles

Adjustable.Container provides a right-click menu for movement/attachment, locking, and related operations. The manual describes standard, light, full, and border lock styles, plus light/dark menu styles in newer releases. Verify keyboard access and retain an escape/reset route when a full lock removes the visible menu margin.

Use `newCustomItem(name, function)` for package-owned menu actions and `newLockStyle(name, function)` only when the custom behavior is fully reversible. Names must not collide with existing items/styles. Keep callbacks local, validate state, and do not let arbitrary data select a function.

Appearance options include frame/inside Label styles, buttons, menu text, title color, button size, and padding. Treat these as a coherent theme and test minimized, hidden, locked, and high-DPI states. Do not reach into undocumented child fields merely to force a style when a public constraint/method exists.

## Borders and connected frames

`attachToBorder(side)` and border margin controls let an adjustable panel occupy a Mudlet border. This changes shared profile layout. Record the exact side/margin the component owns, coordinate with other border users, and reverse only the state still owned by the component.

`connectToBorder`/`disconnect` can join attached containers into a movable border frame; the manual notes that minimizing disconnects and that connected containers can remain resizable while locked. Validate creation order and ensure every required side/container exists before connecting. Provide recovery when a saved or partially created frame is inconsistent.

Menu helpers such as `addConnectMenu` and global `doAll` can affect more than one container. Prefer calls on retained owned instances. Never interpret a package teardown as permission to detach or delete another package's panels.

## ScrollBox

`Geyser.ScrollBox` can be a child of an Adjustable.Container; the practical manual marks that composition as Mudlet 4.15+. Keep one owner-qualified ScrollBox and place content beneath it. Verify scroll range after child creation/removal, wheel and keyboard behavior, clipping, nested interactive controls, and teardown.

Do not assume every special native widget behaves correctly inside a ScrollBox. In particular, test Mapper placement natively rather than inferring support from the Lua hierarchy.

## `changeContainer`

`changeContainer(destination)` moves an existing element or hierarchy to another parent, including returning it to the `Geyser` root. Preserve the object's constraints, but reevaluate them against the new parent. Prevent cycles, foreign ownership, and moving a child into a destination that will be deleted first. Verify visibility, focus, callbacks, clipping, and persistence after every supported move.

## Geyser.Mapper

An embedded `Geyser.Mapper` displays the profile's existing map inside an owned layout; it does not define room identity, import data, or confirm current room. A non-embedded Mapper (`embedded = false`) creates a dock/floating map window. The practical manual documents dock-position selection and `setDockPosition` from Mudlet 4.8+.

Keep display concerns in this skill and map-data/topology changes in `mudlet-mapper-development`. A mapper can be a singleton/special native resource; inspect existing map displays and target behavior before creating another. Verify coexistence with the default mapper, saved dock layout, current-room following, visibility, reparenting, ScrollBox/UserWindow placement, and deletion. Do not claim map persistence, pathfinding, or gameplay movement because the widget renders.

## Native acceptance

Use a disposable profile to test floating/docking on supported platforms, title and frame styling, multi-monitor layout save/load, off-screen recovery, CommandLine focus, adjustable drag/resize/minimize/hide/lock/menu/reset, custom slots/directories, border attachment and connected frames, ScrollBox scrolling/clipping, `changeContainer`, mapper rendering/coexistence, restart/reload, and uninstall. Filesystem inspection alone does not prove layout restoration; a Geyser tree stub does not prove native windows or mapper ownership.
