# Verification evidence

Initial implementation checked 2026-09-09/10. This is a record of observed checks, not a claim that all future versions or MUDs work.

## Toolchain

- Python 3.14.6, isolated virtual environment under `/private/tmp/mudlet-toolbox-venv`.
- PyYAML 6.0.3 and Lupa 2.8. Lua tests and syntax checks explicitly use `lupa.lua51`.
- Muddler 1.1.0 release JAR and Eclipse Temurin Java 17.0.20.1, unpacked into temporary directories. No global tool installation.
- Installed Mudlet 5.0.1 identified through its bundle metadata; release-specific source inspected separately.

## Checks performed

| Check | Result | Scope |
| --- | --- | --- |
| `scripts/validate_toolbox.py` | Passed: six skills | Metadata, local links, expected skill inventory, JSON, example Lua 5.1 syntax. |
| Codex skill-creator `quick_validate.py` | Passed for all six | Skill format checks. |
| Codex plugin-creator `validate_plugin.py` | Passed | Plugin manifest, skill and UI metadata contract. |
| `python -m unittest discover -s tests -v` | 44 tests passed | Inspector, timer/lifecycle logic, injected event/UI/map APIs, and reproducible plugin archive. |
| `scripts/check_starter.py` with the selected Java/JAR | Passed | Real Muddler build, expected archive/XML objects and assets, substituted package identity, serialized Lua syntax and local behavior. |
| Independent package-development forward-test | Passed for one bounded task; 12 additional tests reported | An independent agent followed the skill, renamed/adapted its starter, built a new status package, and checked generated Lua in a scratch project. |
| `scripts/build_plugin.py` | Passed | Distributable source ZIP contains the plugin; tests/research/caches are excluded. Two archives produced from identical source compare byte-for-byte. |
| Whitespace and scope review | Passed | Tracked diff plus new authored source checked; changes confined to plugin, catalog, examples, research, tests, build/validation tooling, and README/ignore rules. |

Commands are documented in the repository README. The bundled skill/plugin validators were invoked from the installed Codex system skills, without copying those validators into this plugin. The package inspector alone also runs under plain Python without Lupa or PyYAML.

The 44 repository tests include 30 inspector tests, 8 component tests, 4 timer/starter tests, and 2 archive tests. Component tests use small injected APIs: they establish behavior such as ownership and cancellation, not native function correctness or event-loop timing.

The independent agent's [full report](evaluations/package-development-forward-test.md) records its scope, actual output, evidence, and remaining checks. The parent inspected that report and the generated lifecycle source. Its one actionable usability observation was addressed: the packaging reference now documents direct `java -jar` use when the `muddle` launcher is absent. The reported temporary paths are historical evidence locations, not installed plugin dependencies.

## Native runtime limits

Directly running the installed Mudlet binary with `--help` aborted with macOS pasteboard/GUI-service connection errors in the tool environment. A second attempt using `QT_QPA_PLATFORM=offscreen` also aborted because this app bundle supplies only the Cocoa platform plugin. Neither attempt opened or modified a test/live profile. No isolated native execution route was established.

Consequently these checks were **not run**: native Package Manager import, PCRE alias/trigger dispatch, actual profile restart, native timer/event-loop behavior, upgrade/uninstall/coexistence, Qt rendering/focus/scroll/click behavior, server GMCP/MSDP negotiation, mapper persistence/pathfinding, and connected gameplay. Pure Lua tests and successful packaging do not substitute for them. The acceptance matrix in the testing skill specifies the next runtime checks.

The plugin is built and available through the repository-local marketplace catalog. It was not registered or installed into the user's global Codex configuration. No commits, pushes, public releases, or changes to ordinary Mudlet profiles were made.

Final plugin archive: `dist/mudlet-toolbox.zip`, 31 members, 41,073 bytes; SHA-256 `ddfaf547292eaded309be2ea9e47b23b1304a4e8e7169e228508140551ca87c5`. The catalog's source path was resolved against this repository and checked against the manifest identity. Final metadata/link checks and archive reproducibility checks passed after the reference additions.
