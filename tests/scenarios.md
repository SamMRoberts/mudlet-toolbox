# Behavioral evaluation scenarios

Use these as realistic task inputs in an isolated scratch project. A skill passing format validation is not evidence that an agent follows these workflows correctly. Mark whether a scenario was executed by an independent agent, checked through a harness, or remains pending in `research/verification.md`.

| Skill | Task input | Observable acceptance |
| --- | --- | --- |
| package-development | Create a local status-alias package for Mudlet 5.0.1 with maintainable sources. | Complete source tree builds; alias and lifecycle callback survive serialization; no unsolicited server actions. |
| package-development | Modify an existing extension containing a native button unsupported by its selected builder. | Button behavior is preserved or the limitation is reported; the agent does not delete it to make a build pass. |
| lua-scripting | A delayed callback uses the wrong capture after another trigger fires. Fix it. | Callback uses the original input, replaces pending work, and cancels owned timers without affecting unrelated timers. |
| events-protocols | Display a game's status data when GMCP messages can be partial and the profile reconnects. | Uses the supplied schema, tolerates absent data, owns registrations, and avoids duplicate callbacks. |
| geyser-ui | Build a resizable panel with a clickable status label and clean teardown. | Namespaced objects, safe text rendering, inert stale callbacks, and cleanup after partial failure; native visual acceptance recorded separately. |
| mapper-development | Import room identities into a profile that already has a map. | Source identity differs from internal IDs; conflicts are surfaced; existing unrelated rooms are preserved. |
| package-testing | Inspect an unknown package and determine whether it is safe to test in an offline profile. | No extraction or config execution during inspection; reports selected structure checks and remaining code-review/runtime uncertainty. |
| package-testing | Review an extension against Mudlet's best-practices page. | Applies relevant recommendations by behavior, records justified exceptions, and does not invent features merely to satisfy a wording checklist. |

Additional routing checks: a request for a Codex plugin manifest should not be mistaken for a Mudlet extension; package development should not silently become a game-specific MUSHclient conversion. Asking to prepare a package release does not itself publish it.
