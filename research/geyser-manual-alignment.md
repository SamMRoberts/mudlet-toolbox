# Geyser manual alignment

Reviewed 2026-09-18 (America/New_York). Primary source: [Manual:Geyser](https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser), pinned for this audit to [revision `oldid=21692`](https://wiki.mudlet.org/index.php?title=Manual:Geyser&oldid=21692). Supporting live source: [Geyser technical API](https://www.mudlet.org/geyser/files/index.html). The wiki and technical API are rolling documentation; distributed guidance uses canonical live links while this record identifies the reviewed snapshot.

No manual prose or example was copied wholesale. The skill resources synthesize decision guidance, ownership/lifecycle rules, version caveats, and acceptance boundaries. A structural test enumerates every heading in the pinned manual table of contents and requires one corresponding topic identifier in the distributed index.

## Coverage map

| Pinned manual area | Distributed reference |
| --- | --- |
| Introduction, assets, constraints, math, Container, HBox/VBox, reparenting | `foundations-layouts.md` |
| Label content/images/styles, tooltips, hover, state controls, sprites, flyouts, right-click menus, names, StyleSheet | `labels-styles-interaction.md` |
| MiniConsole output/copy/edit/gag/links/background/input, Gauge, CommandLine | `consoles-gauges-input.md` |
| UserWindow, Adjustable.Container, persistence, menus, lock styles, borders/frames, ScrollBox, Mapper | `windows-adjustable-mapper.md` |
| Hello World, compass, tabs, resize, ownership, assets, teardown, acceptance | `layout-lifecycle.md` |
| Every manual heading, local route, version/evidence boundary | `topic-index.md` |

The technical API contains additional modules not given standalone practical sections: Button, Color, TextEdit, Window, SetConstraints, GeyserReposition, Util, and Tests. The foundations reference routes them without asserting that the current generated docs match Mudlet 5.0.1.

## Version and platform notes captured

These are discovery cues from the pinned practical page, not replacements for release/source verification:

- Label/Gauge tooltips are marked 4.6+; flyouts 3.0+; custom cursor, `changeContainer`, Mapper docking, and most adjustable/user-window enhancements 4.8+.
- Label right-click menus, standalone CommandLine, MiniConsole background/command-line examples, and several window/adjustable enhancements are marked 4.10+.
- UserWindow itself is marked 4.6.1+; its frame/title stylesheet is marked 4.10+ and Linux-only.
- Adjustable.Container is marked 4.8+; connected border frames 4.10+; its ScrollBox composition 4.15+.
- The historical resize-label walkthrough points to Adjustable.Container instead.

The toolbox baseline remains Lua 5.1 and Mudlet 5.0.1. Existing pinned 5.0.1 research already covers Container deletion, Label callbacks/native cleanup, Gauge values, MiniConsole behavior, Mapper delegation, uninstall events, and related APIs. New references preserve feature checks for other versions and do not introduce a new runtime dependency.

## Evidence boundary

The new dashboard is exercised under an injected Lua 5.1 API for names, construction order, render validation, plain console output, state retention, stale callback suppression, failure cleanup, and owner isolation. Structural checks verify topic inventory and local routes.

No live Mudlet profile was controlled for this release preparation. The audit does not establish Qt geometry/CSS, rich text, hover/click/right-click dispatch, selection/gagging, focus/history, UserWindow docking, Adjustable.Container persistence or border behavior, ScrollBox clipping, native Mapper rendering, profile restart, uninstall, or connected-game behavior. The testing skill records those as separate native or connected acceptance work.
