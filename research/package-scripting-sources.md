# Package and scripting research

Reviewed 2026-09-09/10. Initial compatibility target: Mudlet 5.0.1, Muddler 1.1.0, Lua 5.1-compatible examples. Wiki pages are live documents and may describe newer or older behavior; release-tagged implementation resolves version-specific questions. These records are outside the distributable plugin.

| Source | Decisions supported |
| --- | --- |
| [Manual contents](https://wiki.mudlet.org/w/Manual:Contents) | Scope divided into package work, scripting, events/protocols, UI, mapper, and validation. |
| [Package Manager](https://wiki.mudlet.org/w/Manual:Package_Manager) | Package/module distinction, export workflow, resource location, metadata, and modules writing back to source. |
| [Scripting](https://wiki.mudlet.org/w/Manual:Scripting) | Input objects, scripting boundaries, trigger/alias settings, and debugging workflow. |
| [Lua API](https://wiki.mudlet.org/w/Manual:Lua_Functions) | Runtime API lookup, Lua 5.1 reference, timer/capture/output functions. |
| [Event engine](https://wiki.mudlet.org/w/Manual:Event_Engine) | Profile-load versus installation events and package-filtered uninstall cleanup. |
| [Best practices](https://wiki.mudlet.org/w/Manual:Best_Practices) | Namespacing, resource ownership, duplicate registrations, and cleanup. |
| [Mudlet 5.0.1](https://github.com/Mudlet/Mudlet/releases/tag/Mudlet-5.0.1) | Stable initial target; avoid treating public-test-build additions as stable APIs. |
| [Host.cpp at 5.0.1](https://github.com/Mudlet/Mudlet/blob/Mudlet-5.0.1/src/Host.cpp) | Root XML/trigger discovery, config handling, distinct module events, and queued installation notifications. |
| [XMLexport.cpp at 5.0.1](https://github.com/Mudlet/Mudlet/blob/Mudlet-5.0.1/src/XMLexport.cpp) | Native document structure, version marker, object sections, and bare MudletPackage DOCTYPE. |
| [Muddler](https://github.com/demonnic/muddler) | Lua/JSON source builds and capability boundaries. |
| [Muddler usage](https://github.com/demonnic/muddler/wiki/Usage) | mfile, directory layout, resources, token substitution, and generator overwrite behavior. |
| [Muddler scripts](https://github.com/demonnic/muddler/wiki/Scripts) | scripts.json and eventHandlerList. |
| [Muddler aliases](https://github.com/demonnic/muddler/wiki/Aliases) | aliases.json, source filename convention, and regex property. |
| [Muddler 1.1.0](https://github.com/demonnic/muddler/releases/tag/1.1.0) | Exact builder used for the starter integration check. |
| [Package repository](https://github.com/Mudlet/mudlet-package-repository) | Distribution paths; publication remains a requested action, not an automatic build step. |

## Implementation findings

Mudlet 5.0.1 discovers root-level `.xml` and `.trigger` members for import. Nested XML can instead be an asset. The inspector preserves that distinction, inventories all imported documents, and never evaluates `config.lua`. Its checks are deliberately narrower than a runtime importer: unknown sections are reported, not discarded or declared compatible.

Installation events in this release are queued for a later event-loop iteration. The acceptance guidance therefore requires observing completion between package operations. It does not prescribe arbitrary sleeps as proof of success.

Muddler's wiki examples contain explanatory comments that are not valid JSON. The starter uses actual JSON and is built with the selected builder. Muddler must run with the project as its working directory; passing a project path as an arbitrary positional argument did not select it during our check. That failed attempt printed a missing-src error despite exiting zero, so build acceptance also checks that expected artifacts exist and contain the expected objects.

The starter uses one static lifecycle script and one alias. Its function name matches the registered script name. It demonstrates package events only; module workflows must use their corresponding install/uninstall events, not assume the package example is a universal bootstrap.

## Authoring and installation contract

The local Codex skill-creator and plugin-creator instructions/specification were consulted. The plugin has six independently discoverable skills with focused references. The repository's local marketplace is named `mudlet-toolbox` because the existing personal marketplace already uses `personal`. No installed marketplace or global plugin configuration was changed.

The installed Codex CLI help was checked for `plugin marketplace add` and `plugin add`; the README uses those commands rather than an assumed reinstall command. Generated skill metadata explicitly names its skill in `default_prompt`.

## Remaining research boundaries

Game-specific GMCP/MSDP message shapes and native UI/transport acceptance require the actual game's documentation and runtime observations. No automatic converter, full Mudlet XML schema, general-purpose replacement package builder, or game behavior is claimed.
