# Mudlet Toolbox

A reusable Codex plugin for creating and maintaining Mudlet extensions. Six skills cover packages, Lua scripting, events and protocols, Geyser interfaces, maps, and testing.

The initial examples target Mudlet 5.0.1. The skills require checking the user's actual runtime and existing project conventions. They distinguish offline validation from native Mudlet and connected-game acceptance.

## Skills

| Skill | Use it for |
| --- | --- |
| [mudlet-package-development](plugins/mudlet-toolbox/skills/mudlet-package-development/SKILL.md) | Native exports, modules, Muddler builds, metadata, assets, dependencies, and release preparation. |
| [mudlet-lua-scripting](plugins/mudlet-toolbox/skills/mudlet-lua-scripting/SKILL.md) | Aliases, triggers, scripts, timers, keys, captures, state, and debugging. |
| [mudlet-events-protocols](plugins/mudlet-toolbox/skills/mudlet-events-protocols/SKILL.md) | Owned event handlers, GMCP/MSDP data, negotiation, and connection lifecycle. |
| [mudlet-geyser-ui](plugins/mudlet-toolbox/skills/mudlet-geyser-ui/SKILL.md) | Geyser layout, widgets, callbacks, resizing, and teardown. |
| [mudlet-mapper-development](plugins/mudlet-toolbox/skills/mudlet-mapper-development/SKILL.md) | Room identity, map updates, exits, navigation, and preserving existing maps. |
| [mudlet-package-testing](plugins/mudlet-toolbox/skills/mudlet-package-testing/SKILL.md) | Archive inspection and installation, reload, upgrade, uninstall, and coexistence checks. |

Skills remain available for automatic selection and explicit invocation. For example:

```text
Use $mudlet-package-development to create a package with a local status alias.
Use $mudlet-geyser-ui to add a resizable status panel to this extension.
Use $mudlet-package-testing to inspect this mpackage and test its cleanup.
```

These are development skills, not an automatic MUSHclient converter or a game-specific gameplay system.

## Install in Codex

The repository includes a local marketplace catalog named `mudlet-toolbox`. From a local checkout, register the repository and install the plugin:

```sh
codex plugin marketplace add /absolute/path/to/mudlet-toolbox
codex plugin add mudlet-toolbox@mudlet-toolbox
```

Use your actual checkout path. Start a new Codex task after installation so its skill catalog can load the plugin. Creating this repository does not register a marketplace or change your installed plugins automatically.

The distributable source is `plugins/mudlet-toolbox/`. Research and evaluation material live outside it, so installing the plugin does not load the research archive into every task.

## Examples and package inspection

The [Muddler starter](plugins/mudlet-toolbox/skills/mudlet-package-development/assets/starter/mfile) contains a complete small package with the `toolbox-demo` alias and a lifecycle adapter. Copy the whole starter directory to a fresh project, then run `muddle` from that project's root with Muddler 1.1.0. It produces `build/MudletToolboxDemo.xml` and `build/MudletToolboxDemo.mpackage`.

The alias prints locally; it sends no game commands. The starter demonstrates Package Manager events. Module-specific lifecycle work is described separately in the skills.

Other examples demonstrate delayed-action cancellation, owned protocol listeners, a Geyser panel, and a read-only room identity planner. Their owning skills explain the intended integration and limits.

Inspect a package without executing its Lua or extracting its files:

```sh
python3 plugins/mudlet-toolbox/skills/mudlet-package-testing/scripts/inspect_package.py /absolute/path/example.mpackage
```

The inspector uses only Python 3.10+ standard libraries. It returns JSON and exits nonzero for selected unsafe/malformed container conditions. It inventories native XML and assets; it is not a complete schema validator or malicious-code audit. See `--help` for archive size limits.

## Development checks

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_toolbox.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_plugin.py
```

Validation dependencies are PyYAML and Lupa; the tests deliberately use Lupa's Lua 5.1 runtime. They are needed by repository checks, not by every installed skill. The package inspector and plugin archive builder have no third-party Python dependencies.

The archive builder produces `dist/mudlet-toolbox.zip`, with `.codex-plugin/plugin.json` at its root. This is a Codex plugin source archive, not a Mudlet `.mpackage`. It excludes research, tests, caches, and generated build output. The marketplace installs from the source folder.

The bundled Codex skill-creator `quick_validate.py` and plugin-creator `validate_plugin.py` provide additional format checks when those tools are available. The repository validator is portable and does not depend on their machine-specific paths.

To repeat the actual starter build check with a local Java runtime and Muddler 1.1.0 JAR:

```sh
.venv/bin/python scripts/check_starter.py --java /path/to/java --muddler-jar /path/to/muddle-1.1.0-all.jar
```

This builds a temporary copy and checks the serialized alias, event registrations, assets, Lua syntax, and local behavior. It does not install the result into a profile.

See [research sources](research/package-scripting-sources.md), [evaluation scenarios](tests/scenarios.md), and [verification evidence](research/verification.md) for the evidence and remaining runtime checks.
