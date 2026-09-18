# Mudlet best-practices alignment

Reviewed 2026-09-18 (America/New_York). Primary source: [Manual:Best Practices](https://wiki.mudlet.org/w/Manual:Best_Practices), observed revision `oldid=22381`. Supporting source: [Manual:Functions vs expandAlias](https://wiki.mudlet.org/w/Manual:Functions_vs_expandAlias), observed revision `oldid=6517`. These wiki pages are rolling documentation; the canonical links remain in distributed guidance while this audit records the reviewed revisions.

The source recommendations are applied contextually. The audit does not make every optional pattern mandatory, invent public APIs, or override release-specific evidence from Mudlet 5.0.1 source.

| Source recommendation | Toolbox application |
| --- | --- |
| Prefer locals, avoid `_G`, preserve tables on recompilation, and group required globals | Lua scripting guidance now distinguishes local internals, one public package namespace, state-preserving initialization, and owned-resource replacement. |
| Use table methods/metatables where they improve self-contained design | Lua guidance explains colon methods and avoids requiring object machinery for simple modules. |
| Give Geyser elements unique names and prefer percentages | Geyser guidance requires owner-qualified native names and parent-relative percentage constraints where relationships should scale. |
| Use adjustable containers when users should control layout | Geyser guidance makes `Adjustable.Container` a conditional product choice with persistence and cleanup checks. |
| Shield expensive regex triggers with substring conditions | Lua guidance adds literal substring gates when they preserve semantics and have a demonstrated benefit. |
| Avoid `expandAlias` between owned features | Lua/package guidance keeps aliases thin and calls shared functions directly; intentional user alias-stack processing remains an explicit exception. |
| Keep `feedTriggers` for testing | Lua and package-testing guidance prohibit it as an owned production data path and require isolated replay. |
| Retain temporary/anonymous IDs or use named registrations | Lua, event, package, and testing guidance cover stable ownership, duplicate prevention, and teardown. |
| Use repository updates, optional modules, install onboarding, custom events, namespaces, uninstall cleanup, packaged fonts, `gmod`, and portable paths | Package, protocol, Geyser, and testing references distribute these checks to the workflows that own them. Game-administrator server/automatic-install recommendations remain conditional and separately authorized. |
| Keep generic mapper customization outside `generic_mapper` | Mapper guidance now assigns custom triggers/scripts to a separately owned folder or package that survives mapper updates. |

## Compatibility and evidence boundary

No new runtime dependency or API is introduced. The examples remain Lua 5.1-compatible and use Mudlet 5.0.1 as the verified baseline. The only changed example behavior is a concise installation greeting filtered to the exact starter package; it does not fire for profile loads or unrelated package events.

Documentation alignment and injected Lua checks do not establish native trigger performance, Qt layout, user-adjustable geometry persistence, package-manager event timing, protocol delivery, mapper upgrade survival, or connected gameplay. Those require the relevant native/disposable or live acceptance layer.
