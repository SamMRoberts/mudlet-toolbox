# Behavioral evaluation scenarios

Use these as realistic task inputs in an isolated scratch project. A skill passing format validation is not evidence that an agent follows these workflows correctly. Mark whether a scenario was executed by an independent agent, checked through a harness, or remains pending in `research/verification.md`.

| Skill | Task input | Observable acceptance |
| --- | --- | --- |
| package-development | Create a local status-alias package for Mudlet 5.0.1 with maintainable sources. | Complete source tree builds; alias and lifecycle callback survive serialization; no unsolicited server actions. |
| package-development | Modify an existing extension containing a native button unsupported by its selected builder. | Button behavior is preserved or the limitation is reported; the agent does not delete it to make a build pass. |
| lua-scripting | A delayed callback uses the wrong capture after another trigger fires. Fix it. | Callback uses the original input, replaces pending work, and cancels owned timers without affecting unrelated timers. |
| events-protocols | Display a game's status data when GMCP messages can be partial and the profile reconnects. | Uses the supplied schema, tolerates absent data, owns registrations, and avoids duplicate callbacks. |
| geyser-ui | Build a resizable panel with a clickable status label and clean teardown. | Namespaced objects, safe text rendering, inert stale callbacks, and cleanup after partial failure; native visual acceptance recorded separately. |
| geyser-ui | Build a responsive status dashboard with automatic rows/columns, gauges, history output, and custom command input. | Selects focused Geyser references; retains state across remount; keeps console text and command input in their correct grammars; native geometry/focus acceptance remains separate. |
| geyser-ui | Make a panel dockable and user-adjustable with saved layouts and an embedded mapper. | Separates UserWindow/Adjustable persistence, border ownership, and Mapper display from map-data ownership; records platform/version checks and native gaps. |
| mapper-development | Import room identities into a profile that already has a map. | Source identity differs from internal IDs; conflicts are surfaced; existing unrelated rooms are preserved. |
| mapper-development | Extend a manor map whose perimeter loop has unequal cardinal spans around an inner room cluster; one adjacent cell is occupied and one destination already lies several cells away on the correct axis. | Preserves source exits and authoritative/user/foreign coordinates; accepts the long edge; creates no filler rooms or overlaps; any required reflow moves only owned provisional rooms, or reports a separate unresolved placement conflict. |
| package-testing | Inspect an unknown package and determine whether it is safe to test in an offline profile. | No extraction or config execution during inspection; reports selected structure checks and remaining code-review/runtime uncertainty. |
| package-testing | Review an extension against Mudlet's best-practices page. | Applies relevant recommendations by behavior, records justified exceptions, and does not invent features merely to satisfy a wording checklist. |

Additional routing checks: a request for a Codex plugin manifest should not be mistaken for a Mudlet extension; package development should not silently become a game-specific MUSHclient conversion. Asking to prepare a package release does not itself publish it.
