# Foundations and automatic layouts

Use this reference for Geyser's coordinate model, ownership hierarchy, Containers, HBox/VBox, reparenting, and resize decisions. The [official manual](https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser) supplies practical examples; the [technical API](https://www.mudlet.org/geyser/files/index.html) is the live method inventory.

## Constraint model

Each Geyser object has `x`, `y`, `width`, and `height` constraints relative to its direct parent. A number is pixels. A string can use pixels (`px`), character cells (`c`), percentages (`%`), and supported arithmetic such as `100%-30px`. Zero coordinates start at the parent's top-left.

Negative positions anchor from the parent's right or bottom edge. Account for the object's own dimensions: a 20%-wide right panel normally uses `x = "-20%"`, not `x = 0`. Negative widths/heights and mixed arithmetic can describe an inset from the far edge, but validate them at narrow sizes. A child at `x = 10` with `width = "100%"` extends beyond its parent; percentages do not subtract the offset automatically.

Character units are useful for text surfaces whose font metrics define their natural size. Pixels suit fixed details. Percentages suit scalable relationships. Do not mix units without an explicit reason, and do not convert a working parent-relative layout into manual `getMainWindowSize()` arithmetic merely because a resize event exists.

## Root, Container, and hierarchy

`Geyser.Container:new(constraints, parent)` creates an invisible layout boundary. Omitting `parent` attaches to the main Geyser root. Passing a parent or calling the parent's `add(child)` makes child geometry relative to that parent. Show/hide cascades through descendants; a hidden child remains allocated and may retain buffers/state.

Use Containers to express ownership, clipping, visibility, or a meaningful layout region. Avoid gratuitous nesting: it complicates names, stacking, mouse routing, and cleanup. Give every object a globally unique owner-qualified name even when a constructor appears to accept an omitted name; unnamed objects can duplicate during save/reload workflows.

Geyser already responds to the main resize event and recalculates constrained geometry. Add an owned `sysWindowResizeEvent` handler only for a relationship such as an aspect ratio or breakpoint that constraints/HBox/VBox cannot express. UserWindows also have their own resize boundary; do not assume every resize event refers to the main console.

## HBox and VBox

`Geyser.HBox` and `Geyser.VBox` are Containers that lay out children in insertion order. HBox allocates horizontally and VBox vertically. Use them for toolbars, tab headers, evenly divided panels, and rows/columns that should respond automatically to parent size.

Dynamic children share available space. Use `h_stretch_factor` or `v_stretch_factor` to assign relative shares. Use `h_policy = Geyser.Fixed` or `v_policy = Geyser.Fixed` when a child's explicit dimension should not stretch; the default is dynamic. Confirm the combination at minimum and maximum supported sizes, because fixed children can exhaust the available area.

Do not add the same child to multiple automatic containers. Preserve insertion order deliberately when rebuilding a layout. Prefer updating, hiding, or reparenting an existing child to repeatedly constructing objects with the same native name.

## Moving and changing parents

Use `move` and `resize` to change constraints on an existing object; a `nil` dimension retains the current value where supported. Use `changeContainer(destination)` when content must move between an owned main-window Container, UserWindow, or another compatible destination. Use the Geyser root as the destination when moving an object back to the main window.

Reparenting is not proof of visual equivalence. Verify constraint interpretation, clipping, z-order, focus, callbacks, and show/hide state in the destination. Keep destination lifetime at least as long as the child and prevent either owner from deleting the other's objects.

## Technical companion classes

The practical manual emphasizes the common UI elements. The live technical index also documents these supporting modules:

- `Geyser.Window` is the abstract base for native-window-backed classes; use a concrete class unless implementing a reviewed extension.
- `Geyser.SetConstraints` and `GeyserReposition` implement constraint calculation and resize response; consume public object methods instead of editing their internals.
- `Geyser.Color` parses and converts colors; validate parse results before using them in styles or state.
- `Geyser.Button` and `Geyser.TextEdit` are available through the technical API even though the practical page focuses on Label-based controls and CommandLine. Inspect their target-version contracts before choosing them.
- `Geyser.Util` contains helpers; treat current documentation as rolling and feature-check helpers not verified for the package's target release.
- `Geyser.Tests` is upstream test material, not a runtime dependency or substitute for package acceptance.

The technical API was regenerated after Mudlet 5.0.1 and can contain newer modules or methods. For a 5.0.1 package, confirm the release source or a native disposable profile before depending on a live-doc-only API.

## Layout diagnosis

When geometry is wrong, inspect in this order:

1. direct parent and its actual size;
2. each raw constraint and unit;
3. negative-anchor math and fixed/stretch policies;
4. parent visibility, clipping, borders, and sibling overlap;
5. whether another resize handler overwrites Geyser's result;
6. native behavior at narrow, wide, high-DPI, floating, and docked sizes.

Object tables and stubbed constraints can expose hierarchy mistakes. They cannot establish native pixels, font-cell measurements, Qt layout policy, or platform window behavior.
