# UI, protocol, and mapper source audit

Research scope: only `mudlet-events-protocols`, `mudlet-geyser-ui`, and `mudlet-mapper-development`. Consulted 2026-09-09 (America/New_York). No live profiles were opened or changed. Distributed references are synthesized guidance; this file holds provenance and evidence boundaries.

## Release identity

Official repository: [Mudlet/Mudlet](https://github.com/Mudlet/Mudlet).

- Requested baseline: `Mudlet-5.0.1`.
- [Tag ref](https://api.github.com/repos/Mudlet/Mudlet/git/ref/tags/Mudlet-5.0.1) resolves to annotated tag object `9d037bb4ccfb6b5885d464fbaaa7590fd84b1d94`.
- [Commit lookup](https://api.github.com/repos/Mudlet/Mudlet/commits/Mudlet-5.0.1) resolves to commit `592821c8c0c6a638be87a9de5995b8a278f2e4b4`, with tree `d555d7bd443af46505b66b4e4cda159d0370c58a`.
- Source files were retrieved from the official raw-content host, first by tag and then by pinned commit for additional files. Temporary inspection copies live outside the plugin in `/tmp/mudlet-ui-protocol-mapper-501`. They are not runtime dependencies or deliverables.

## Official wiki discovery

The wiki is rolling documentation, not a release-pinned contract. No manual text was copied into the skill resources.

- [Event Engine](https://wiki.mudlet.org/w/Manual:Event_Engine): callback/event model, custom events, lifecycle event discovery.
- [Miscellaneous Functions](https://wiki.mudlet.org/w/Manual:Miscellaneous_Functions#registerNamedEventHandler): named handler arguments and replacement behavior.
- [Lua Functions](https://wiki.mudlet.org/w/Manual:Lua_Functions#killAnonymousEventHandler): anonymous handler cleanup and helper discovery.
- [Technical Manual](https://wiki.mudlet.org/w/Manual:Technical_Manual#Managing_GMCP_modules): GMCP table consumption and shared `gmod` usage.
- [Geyser](https://wiki.mudlet.org/w/Manual:Geyser): parent-relative constraints, widget construction, responsive layouts, rich-text labels.
- [Mapper Functions](https://wiki.mudlet.org/w/Manual:Mapper_Functions): map API inventory, room identity, metadata cleanup, graph operations.

## Release-specific implementation evidence

All links below pin the verified 5.0.1 commit. Conclusions describe source inspection, not live acceptance.

### Events and protocols

- [IDManager.lua, lines 11–75 and 277–342](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/IDManager.lua#L11): register stops the old name before replacement; stop retains the definition; resume registers it again; delete removes it. Public named registration returns `true` or reports an error, not an anonymous ID. Missing named definitions return `false` on stop/delete/resume. Registration failure is not an atomic restoration of the old handler.
- [Other.lua, lines 847–953](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/Other.lua#L847): anonymous registration returns numeric IDs; removal returns `true` or `nil, message`; function-reference registrations can duplicate; dispatch uses unordered iteration and passes event name first. One-shot implementation checks truthiness, broader than the wiki's wording about returning `true`. Guidance recommends explicit booleans.
- [GMCP.lua, lines 14–140](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/GMCP.lua#L14): owner registration is automatic; exact module names hold sets of owners; initial dotted prefix advertisements use version `1`; ordinary enable/disable success has no return value. Reconnect hooks `sysProtocolEnabled`, but `reenableModules` exits for an empty `gmcp` table. No general parent/child dependency accounting or version parameter was inferred.
- [TLuaInterpreter.cpp, lines 3801–3920](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreter.cpp#L3801): protocol parsing replaces leaves except configured merge keys; events include prefixes and the full key argument. Decoder errors can still reach event emission. [Host.cpp line 318](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/Host.cpp#L318) initializes the merge-key list with `Char.Status`. No server's field schema or delivery completeness was established.

### UI

- [GeyserContainer.lua, lines 328–465](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/geyser/GeyserContainer.lua#L328): parent/root attachment and special `Class` naming; deletion recurses through children, unlinks tracking, and invokes type cleanup. This supports the 5.0.1 example's recursive-delete requirement; it does not prove all older releases implement the same cleanup.
- [GeyserLabel.lua, lines 499–508](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/geyser/GeyserLabel.lua#L499): callback binding delegates to native API and retains callback/arguments. [Lines 1102–1111](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/geyser/GeyserLabel.lua#L1102): label-specific deletion invokes `deleteLabel`.
- [TLabel.cpp, lines 45–72](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLabel.cpp#L45): labels use Qt rich text; native destructor frees callback registry references. This supports escaping label text and deleting native labels, but not a claim that native events/destructors were exercised offline.
- [Host.cpp, lines 2535–2565](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/Host.cpp#L2535): uninstall events carry package/module name; package, UI-module, sync-module, and script-module uninstall events differ.
- [GeyserMapper.lua](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/geyser/GeyserMapper.lua): inspected native mapper delegation. No universal ScrollBox placement ban or visual-parity guarantee was inferred; complex placement remains a live verification concern.

### Mapper

- [TLuaInterpreterMapper.cpp, lines 605–638](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L605): `addRoom` may create a room but return `nil, message` on failed area assignment, leaving it in default area. The guidance explicitly records this partial mutation.
- [Lines 900–930](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L900): `clearRoomUserDataItem` distinguishes removed (`true`), absent (`false`), and invalid room/map (`nil, message`). Prior workspace memory suggested checking this edge case; current source independently confirms it.
- [Lines 1229–1250](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L1229) and [TMap.cpp, lines 493–505](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TMap.cpp#L493): `createRoomID` finds an unused ID without reservation or insertion.
- [Lines 2293–2315](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L2293) and [4196–4212](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L4196): missing hash lookup returns `-1`; reverse lookup has nullable errors; hash assignment replaces both links, validates no room existence, and returns zero Lua values.
- [Lines 2399–2433](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L2399) and [4235–4267](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L4235): metadata getter default empty-string behavior versus full errors; setter string values and success/error returns.
- [TMap.cpp, lines 507 onward](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TMap.cpp#L507) and [mapper binding line 3717](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L3717): standard exits are directed; absent positive destinations fail; nonpositive destinations remove the exit.

## Scope completion: MSDP, common widgets, persistence/navigation

Added compact workflow sections to the three references only; examples, scripts, assets, dependencies, and parent-owned tests remain unchanged.

- MSDP wiki: [Supported Protocols, MSDP](https://wiki.mudlet.org/w/Manual:Supported_Protocols#MSDP) establishes profile settings/reconnect, server-dependent GMCP/MSDP coexistence, and `msdp` event/table usage. [Networking Functions, sendMSDP](https://wiki.mudlet.org/w/Manual:Networking_Functions#sendMSDP) supplies string-vararg request forms. Pinned [TLuaInterpreterNetworking.cpp, lines 455–502](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterNetworking.cpp#L455) confirms wire encoding, connected/write checks, `true`/nullable-error returns, and intentional absence of a negotiated-enable check. [ctelnet.cpp, lines 3002–3052](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/ctelnet.cpp#L3002) confirms preference gating, commands-list/client identification requests, and the `sysProtocolEnabled` MSDP event. The previously cited `setMSDPTable`/`parseJSON` source confirms current table storage and full-key callback arguments. Choosing a single authoritative producer and coordinating MSDP ownership are synthesized design guidance, not built-in gmod functionality.
- Common Geyser widgets: [Geyser wiki](https://wiki.mudlet.org/w/Manual:Geyser) plus pinned [GeyserGauge.lua, lines 265–295 and 353–357](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/geyser/GeyserGauge.lua#L265) confirm ratio/percentage updates, invalid-maximum handling, and label-backed text. [GeyserMiniConsole.lua, lines 55–85 and 594 onward](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/geyser/GeyserMiniConsole.lua#L55) confirms bounded buffers, manual/automatic wrapping distinction, and construction. Inherited [GeyserWindow.lua, lines 28–38](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/geyser/GeyserWindow.lua#L28) supplies echo/cecho. [GeyserContainer.lua, lines 131–174](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/mudlet-lua/lua/geyser/GeyserContainer.lua#L131) supports visibility-based tabs; label callbacks were verified above. Simple tabs are a composition recommendation, not a newly claimed Geyser tab API or dependency.
- Persistence/navigation wiki: [Mapper Functions](https://wiki.mudlet.org/w/Manual:Mapper_Functions#saveMap). Pinned [mapper binding lines 3128–3150](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L3128) establishes `saveMap(path, formatVersion)`; the wiki's version-only example was not propagated because the 5.0.1 binding expects a string first. [Lines 2703–2763](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L2703) and [3106–3124](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L3106) confirm JSON mapper prerequisites and nullable failures, plus distinct native/XML load return handling. [TMap.cpp, lines 2650–2663](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TMap.cpp#L2650) includes clearing the map for XML import; no load API was treated as an ownership-aware merge.
- [Mapper binding lines 2056–2084](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L2056) confirms path results and assembly without travel. [Lines 2588–2613](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/TLuaInterpreterMapper.cpp#L2588) invokes speedwalking for `gotoRoom`. [Host.cpp, lines 1441–1463 and 1488–1495](https://github.com/Mudlet/Mudlet/blob/592821c8c0c6a638be87a9de5995b8a278f2e4b4/src/Host.cpp#L1441) confirms the three shared speedwalk tables and call to `doSpeedWalk`. Cancellation is a caller/adapter workflow recommendation, not an invented universal mapper API.

These additions have source-inspection evidence only. MSDP negotiation, gauge rendering, chat routing/tab interaction, save/load round-trips, and actual navigation/cancellation were not run. The parent owns durable integration tests. No live actions or new runtime dependencies were introduced.

## Validation performed

- Read the requested skill-creator instructions and `references/openai_yaml.md`. Generated only the three owned `agents/openai.yaml` files using its generator, then added explicit `$skill-name` default prompts for the integration validator. No policy disables implicit invocation.
- Ran `quick_validate.py` on each of the three skills: all passed.
- Used isolated `/tmp/mudlet-ui-protocol-mapper-venv` with PyYAML and Lupa; no global installation. Lupa's `lua51` runtime reports Lua 5.1.
- Loaded all three Lua files under an environment that errors on global reads/writes: all returned modules without accessing Mudlet or creating resources at load time.
- Executed ephemeral stub checks for named/anonymous listener duplicate start, stop/restart, terminal destroy, missing/intermediate malformed data, partial updates, and false values; all passed.
- Executed panel stub checks for idempotent mount/destroy, names, HTML escaping, resize validation, stale callback guards after remount, and cleanup following label construction failure; all passed.
- Executed mapper stub checks for create/reuse decisions, leading-zero identity preservation, missing IDs, stale candidate hashes, ownership conflicts, mismatched metadata, and missing linked rooms. Stub API exposed only reads/candidate lookup; all passed.

These are smoke checks of examples, not the parent agent's permanent test suite. No test files or sibling skills were changed. No real GMCP traffic, gmod reconnect sequence, Qt rendering, native callback destruction, mapper writes, persistence, pathfinding, movement, packaging, or cross-version runtime behavior was tested. A full importer and game-specific normalization are intentionally outside these examples.
