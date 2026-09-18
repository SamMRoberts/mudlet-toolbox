---
name: mudlet-package-development
description: Create, inspect, modify, and build Mudlet packages or modules, including extensions called plugins, metadata, assets, dependencies, and Muddler projects. Use for distribution or module development workflows.
---

# Mudlet package development

Produce an installable extension and maintainable sources, preserving the user's chosen behavior and build workflow.

## Establish the package contract

- Inspect existing source, exported XML, metadata, build commands, and uncommitted changes before choosing tooling. Record the requested Mudlet version, package identity, supported platforms, and required objects/resources.
- Distinguish a Mudlet package from a development module and a Codex plugin. Packages are imported into a profile; modules can write back to their source and synchronize across profiles. Installing the same file through a different manager changes its lifecycle.
- For a new package, choose a unique package name and Lua namespace. For an existing package, preserve both unless a migration is requested. Keep runtime state and user settings separate from replaceable installed assets.
- Prefer modules for genuinely optional components users may enable independently; do not split a cohesive package merely to satisfy a checklist.
- The initial examples target Mudlet 5.0.1 with Lua 5.1-compatible syntax. Check the actual target version rather than assuming current wiki APIs exist there.

## Choose and implement the build workflow

Read [build workflows](references/build-workflows.md) when choosing between the native exporter, module editing, Muddler, and direct XML work. Use [the starter](assets/starter/mfile) for a small new Muddler package; its complete file tree is under `assets/starter/`.

Preserve all requested triggers, aliases, scripts, timers, keys, buttons, and resources. Compare the selected builder's capabilities with that inventory. If an object is unsupported, retain a native XML/export workflow or implement an equivalent deliberately; report unresolved behavior instead of dropping it.

Keep aliases and triggers thin: they parse input and call package functions. Avoid uncontrolled top-level side effects when scripts compile again after editor saves. Handle first installation and subsequent profile loads explicitly, with package-name filters on install/uninstall events.

Give a concise introduction on the exact package installation event when users need a command or setup hint; do not repeat it on every profile load. For public integration points, expose documented owner-prefixed events rather than depending on script order or another package's internals.

Read [lifecycle and release](references/lifecycle-release.md) for initialization, cleanup, dependencies, asset paths, settings, and release checks. Add only dependencies the extension needs; metadata alone does not prove that a dependency is installed or ready.

For a Geyser interface, use `mudlet-geyser-ui` for the widget/layout contract. Package its redistributable fonts, images, cursor art, and notices below the extension; keep adjustable/UserWindow layout state outside replaceable assets; and make upgrade/uninstall behavior explicit for saved layouts, shared borders, native windows, and mapper displays.

## Verify the result

Build with the project's documented command. Inspect the generated archive/XML and compare object inventory and assets with the contract. For an existing extension, compare before/after inventory as well as source diffs.

Use the sibling `mudlet-package-testing` skill for archive inspection and runtime acceptance. A build proves packaging, not working triggers or rendered UI. Deliver source/build instructions, artifact location, compatibility target, checks actually performed, and any remaining runtime checks.

Preparing a release does not itself publish it or install it into an unrelated live profile. Carry out distribution and profile changes within the user's requested scope.
