# Verification evidence

Initial implementation checked 2026-09-09/10; the 0.1.1 best-practices alignment, 0.2.0 comprehensive Geyser update, and 0.2.1 sparse-grid mapper patch were checked 2026-09-18. This is a record of observed checks, not a claim that all future versions or MUDs work.

## 0.2.1 sparse-grid mapper patch

The existing Python 3.14.6 environment at `/private/tmp/mudlet-toolbox-020-venv` was reused with PyYAML 6.0.3 and Lupa 2.8; its directory name is historical and does not identify the validated plugin version.

| Check | Result | Scope |
| --- | --- | --- |
| `scripts/validate_toolbox.py` | Passed: six skills and 41 plugin files | Metadata, 0.2.1 manifest, local links, expected skill inventory, JSON, and example Lua 5.1 syntax. |
| Codex skill-creator `quick_validate.py` | Passed for `mudlet-mapper-development` | Updated skill format and frontmatter. |
| Codex plugin-creator `validate_plugin.py` | Passed | Plugin manifest, skill, and UI metadata contract. |
| `python -m unittest discover -s tests -v` | 49 tests passed | Existing component behavior, inspectors, Geyser coverage, and reproducible 0.2.1 archive checks. |
| Sparse manor-loop scenario review | Passed by direct guidance review | Long-axis links, occupied adjacent coordinates, loop closure, coordinate authority, provisional-only reflow, and unresolved off-axis placement are addressed without filler rooms or topology changes. This is not an executed layout algorithm. |
| `scripts/build_plugin.py` | Passed | Two temporary archives and the final archive compare byte-for-byte; source-only marketplace policy remains unchanged. |

Final 0.2.1 plugin archive: `dist/mudlet-toolbox.zip`, 37 members, 66,603 bytes; SHA-256 `633cb515e056f56b0b11415f175cd9ee9dd42ab22adaec1e8fc79d0bc6b504de`. Archive inspection confirmed the 0.2.1 manifest and updated sparse-grid reference while excluding research, tests, caches, generated output, and Finder metadata.

No native Mudlet rendering, persistence, pathfinding, server synchronization, or gameplay checks were run for this documentation-focused patch. The plugin was not installed, published, committed, pushed, tagged, or used to modify a Mudlet profile.

## 0.2.0 baseline toolchain

- Python 3.14.6, isolated 0.2.0 virtual environment under `/private/tmp/mudlet-toolbox-020-venv`.
- PyYAML 6.0.3 and Lupa 2.8. Lua tests and syntax checks explicitly use `lupa.lua51`.
- Muddler 1.1.0 release JAR and Eclipse Temurin Java 17.0.20.1, unpacked into temporary directories. No global tool installation.
- Installed Mudlet 5.0.1 identified through its bundle metadata; release-specific source inspected separately.

## 0.2.0 baseline checks

| Check | Result | Scope |
| --- | --- | --- |
| `scripts/validate_toolbox.py` | Passed: six skills and 41 plugin files | Metadata, 0.2.0 manifest, local links, expected skill inventory, JSON, and example Lua 5.1 syntax. |
| Codex skill-creator `quick_validate.py` | Passed for all six | Skill format checks. |
| Codex plugin-creator `validate_plugin.py` | Passed | Plugin manifest, skill and UI metadata contract. |
| `python -m unittest discover -s tests -v` | 49 tests passed | Inspector, timer/lifecycle logic including install-only onboarding, injected event/UI/map APIs, complete pinned Geyser-topic routing, and reproducible 0.2.0 plugin archive. |
| `scripts/check_starter.py` with Muddler 1.1.0 and Temurin 17.0.20.1 | Passed | Real Muddler build, expected archive/XML objects and assets, substituted package identity, serialized Lua syntax, exact-package greeting, load silence, alias behavior, and uninstall cleanup. |
| Prior 0.1.0 independent package-development forward-test | Passed for one bounded task; 12 additional tests reported | Historical evidence that an independent agent followed the skill, renamed/adapted its starter, built a new status package, and checked generated Lua in a scratch project; not rerun for the documentation-focused 0.1.1 change. |
| `scripts/build_plugin.py` | Passed | Distributable source ZIP contains the plugin; tests/research/caches are excluded. Two temporary archives and the final archive compare byte-for-byte. |
| Whitespace and scope review | Passed | Changes are confined to plugin source, README/changelog, research, tests, and version-aware validation; marketplace metadata and the starter source are unchanged. |

Commands are documented in the repository README. The bundled skill/plugin validators were invoked from the installed Codex system skills, without copying those validators into this plugin. The package inspector alone also runs under plain Python without Lupa or PyYAML.

The 49 repository tests include 30 inspector tests, 10 component tests, 2 Geyser coverage tests, 4 timer/starter tests, and 3 archive tests. Component tests use small injected APIs: they establish behavior such as ownership, state validation, cancellation, and stale-callback suppression, not native function correctness or event-loop timing. The coverage test checks the pinned manual's topic inventory and local reference routes; it does not validate the advice by text matching.

The independent agent's [full report](evaluations/package-development-forward-test.md) records its scope, actual output, evidence, and remaining checks. The parent inspected that report and the generated lifecycle source. Its one actionable usability observation was addressed: the packaging reference now documents direct `java -jar` use when the `muddle` launcher is absent. The reported temporary paths are historical evidence locations, not installed plugin dependencies.

## Native runtime limits

Directly running the installed Mudlet binary with `--help` aborted with macOS pasteboard/GUI-service connection errors in the tool environment. A second attempt using `QT_QPA_PLATFORM=offscreen` also aborted because this app bundle supplies only the Cocoa platform plugin. Neither attempt opened or modified a test/live profile. No isolated native execution route was established.

Consequently these checks were **not run**: native Package Manager import, PCRE alias/trigger dispatch, actual profile restart, native timer/event-loop behavior, upgrade/uninstall/coexistence, Geyser constraint geometry, Qt rich text/CSS/selector rendering, mouse/focus/history/scroll behavior, console selection/gagging, UserWindow docking/layout persistence, Adjustable.Container menus/dragging/saved state/borders, `changeContainer`, native Mapper rendering, server GMCP/MSDP negotiation, mapper persistence/pathfinding, and connected gameplay. Pure Lua tests and successful packaging do not substitute for them. The acceptance matrix in the testing skill specifies the next runtime checks.

The repository-local catalog still points to the source folder with unchanged `AVAILABLE`/`ON_INSTALL` policy. The 0.2.0 working tree was not committed, pushed, tagged, published, refreshed in the Git-backed marketplace, or reinstalled. No ordinary Mudlet profiles were changed.

Final 0.2.0 plugin archive: `dist/mudlet-toolbox.zip`, 37 members, 65,472 bytes; SHA-256 `1a46df3bee97f05996e4df53534985e7ce3266372b0adb875faf8991a4a0b652`. Two temporary builds and the final build compared byte-for-byte. Archive inspection confirmed the six skills and 0.2.0 manifest while excluding research, tests, caches, generated output, and Finder metadata.

Archive inventory: one plugin manifest; six `SKILL.md` entrypoints; six `agents/openai.yaml` files; two event/protocol support files; eight Geyser support files (two examples and six references); two Lua-scripting support files; two mapper support files; eight package-development files (two references and the six-file Muddler starter); and two package-testing support files. The full member list was inspected with `zipinfo -1` after the deterministic comparison.
