# Build workflows

## Select the least disruptive source format

| Existing or requested work | Workflow |
| --- | --- |
| Small package authored in Mudlet | Use Package Exporter; select the complete object tree, metadata, and assets. Export and reimport into a disposable profile. |
| Editing native objects in an external editor | Use a module when source synchronization is wanted. Protect the original file: module saves can rewrite it. Check synchronization and priority settings per profile. |
| Existing Muddler project | Preserve its layout, version, and build command. Edit Lua and JSON sources, not generated XML. |
| New source-controlled Lua package | Muddler is a useful option if it supports the requested object types. Native export is also valid. |
| Unsupported object or unusual exported XML | Preserve the native object. Inspect an actual export from the target Mudlet version and its importer/exporter source before generating XML. |

`.mpackage` is a ZIP container, not a different scripting language. It can hold Mudlet XML, `config.lua` metadata, and assets. Plain XML is also installable. Do not unzip an unknown package over a working directory or execute `config.lua` to inspect metadata. XML version attributes describe the document format, not a promise of runtime compatibility.

## Muddler starter

Copy this skill's entire `assets/starter/` directory to a new, absent destination. It contains:

```text
mfile
src/scripts/MudletToolboxDemo/scripts.json
src/scripts/MudletToolboxDemo/MudletToolboxDemoLifecycle.lua
src/aliases/MudletToolboxDemo/aliases.json
src/aliases/MudletToolboxDemo/status.lua
src/resources/demo.txt
```

The example package is named `MudletToolboxDemo`. Its `toolbox-demo` alias prints a local status message and sends nothing to a game. The lifecycle adapter handles startup, installation, and uninstall. It intentionally has no network, settings, UI, or gameplay behavior.

From the copied project directory, run `muddle`. Muddler writes `build/MudletToolboxDemo.xml` and `build/MudletToolboxDemo.mpackage`. The starter was designed for Muddler 1.1.0. Verify the installed builder version and inspect its output before claiming compatibility with another release.

If the launcher is not on `PATH` but the distribution JAR and a suitable Java runtime are available, run `/path/to/java -jar /path/to/muddle-1.1.0-all.jar` from the project directory. Passing the project path as an arbitrary positional argument does not replace setting the working directory. Check artifact existence and content as well as the process exit code.

For real work, rename the package metadata, namespace, lifecycle adapter, object groups, and alias together. Set the actual author/version/description; the example's values identify the example only. Do not leave sample identities in the user's extension.

Muddler conventions used here:

- `mfile` is JSON; `package`, `version`, `title`, `description`, and `author` describe the package.
- `scripts.json` and `aliases.json` are arrays. A named item obtains its code from the matching `.lua` file unless a script is specified inline. Spaces in item names become underscores in filenames.
- `eventHandlerList` registers script event callbacks; use a callable function matching the script's name. Do not also register the same callbacks anonymously.
- `src/resources/` supplies package assets. Additional native Mudlet XML placed there may be imported too; inventory it rather than treating it as inert documentation.
- Build substitutions such as `@PKGNAME@` are a builder feature. They are not interpreted by plain Lua or native Package Exporter.
- The documented `dependencies` value is a comma-separated string. Confirm current builder and package-manager behavior before relying on dependency resolution.

Do not run `muddle --default` in a directory containing a valuable `TemplateProject`: this generator can recreate that directory. Prefer a fresh destination or the included small starter.

## Asset paths and portability

Packaged assets are installed below `getMudletHomeDir() .. "/" .. packageName`. Use `/` path separators on all platforms. Resolve assets at runtime instead of embedding developer-machine paths. Avoid assuming the process working directory is the profile directory.

Check filename case on case-sensitive systems. Include required fonts/images/sounds and their redistribution notices. Do not invent or assign a license to third-party files.
