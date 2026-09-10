# Independent skill forward-test

Result: the requested small package was created, built, and prepared for further testing using the development skill and its linked references/starter plus the sibling testing skill. No blocking defect, misleading instruction, or broken resource link was encountered in this workflow. This is bounded execution evidence for one task, not a general skill benchmark or full compatibility certification.

Task: “Create a small Mudlet 5.0.1 package with maintainable source and a local status alias; prepare it for testing and report what you verified.”

All produced files are under `/private/tmp/mudlet-skill-forward-0amb_nmk`. No repository files were modified, no commits were made, and no profiles or global installations were created or changed. Existing repository changes were preserved: before/after Git status matches and 31 skill files retain their initial SHA-256 hashes.

## Resulting files

- `LocalStatusProbe/mfile`, `src/` — metadata, separate Lua/JSON source and resource copied from the full starter and consistently renamed.
- `LocalStatusProbe/build.sh`, `LocalStatusProbe/README.md` — reproducible local JAR build and test/acceptance instructions.
- `LocalStatusProbe/build/LocalStatusProbe.mpackage` — package ZIP with exactly `LocalStatusProbe.xml`, `config.lua`, and `demo.txt`.
- `LocalStatusProbe/build/LocalStatusProbe.xml` — matching standalone native XML.
- `LocalStatusProbe/build/tmp/` — Muddler intermediate files, if present.
- `test_package.py` — twelve independent offline assertions/scenarios using generated artifact Lua.
- `inspect_package.py` — unchanged copy of the testing skill's read-only inspector.
- `evidence/` — builder log, archive/XML JSON inspection, test log, manifests/hashes, installed Mudlet version, and repository preservation evidence.

Final tested artifact SHA-256: `4dce1266ff951c680fe53df63ec1adeca3beb8e424184dd17dc371dd340e369e`.

## Actual behavior and verification

| Check | Result and boundary |
| --- | --- |
| Build | Passed twice with supplied Java 17.0.20.1 and builder reporting Muddler 1.1.0. Final rebuild used the delivered build.sh. |
| Archive and XML inspector | Both exit 0, no diagnostics. Structure/safety inspection only; config not executed. |
| Inventory | Exactly one active alias, one active lifecycle script, their groups, three named events, metadata and resource. No timer/trigger/key/button objects; alias command field empty. |
| Lua syntax | Passed for source Lua, all generated XML script bodies and config.lua using Lua 5.1. JSON scanned for inline script bodies; none present. |
| Local status | Before lifecycle startup: `Local Status Probe: inactive; calls=1`. Fresh install/profile-load callback followed by alias body: `Local Status Probe: ready; calls=1`, then `calls=2`. Echo captured locally; no selected forbidden APIs called. Native alias matching/consumption not tested. |
| Event filtering | Unrelated, missing, case-mismatched identities and unknown events leave state unchanged. |
| Reinitialization | Repeated source execution and startup callbacks preserve counter without duplicate output. No runtime objects are allocated by this starter. |
| Cleanup | Own uninstall clears namespace and lifecycle global; invoking a previously captured cleanup callback again succeeds, including before startup. |
| Reinstall | Simulated uninstall/reload/install resets in-memory count. This is not native upgrade acceptance. |
| Coexistence | A second renamed script in the same Lua VM remains callable after target cleanup. No second native package was installed. |
| Regression suite | All 12 tests pass (Python 3.14.6, Lupa 2.8, explicit Lua 5.1). |
| Installed target | Read-only Info.plist reports installed Mudlet 5.0.1. No native process was launched or profile opened. |

## Skill observations

- The complete starter, explicit renaming checklist, @PKGNAME@ substitution guidance, and testing handoff were sufficient. Package identity, namespace, adapter, object groups, alias and metadata were updated without replacing the starter's implementation.
- Minor tooling friction: build-workflows.md says to run `muddle`, but no such command is on PATH in this environment. The user supplied a usable JAR; direct `java -jar` worked immediately and was captured in build.sh. An optional local-JAR example would improve this environment's first-run experience. This did not block or mislead the implementation.
- The instructions correctly separate inspection, Lua simulation and native acceptance. The inspector's `item_count` counts direct group entries; detailed `element_counts` and direct XML checks supplied the actual child object inventory.
- No supported-version or native lifecycle promise was inferred from the XML format version or a passing build. No settings, dependency system, module workflow, UI, or game behavior was added.

## Remaining evidence

Native Package Manager import, real event dispatch, PCRE matching and input consumption, profile restart, editor-save registration behavior, native replacement/upgrade, native uninstall and two-package coexistence remain unverified. The installed app was intentionally left untouched: no isolated native launch mechanism was established during this bounded offline run. The README contains a staged native acceptance checklist. Rendering and connected-game acceptance are outside the feature's scope.

No production publication or installation occurred. The package is built and ready for disposable-profile testing; native Mudlet 5.0.1 acceptance is still pending.
