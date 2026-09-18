# Event ownership and protocol contracts

## Handler lifecycle

Verified against Mudlet 5.0.1; choose capabilities for the actual target.

| API | Contract and consequence |
| --- | --- |
| `registerNamedEventHandler(owner, name, event, fn, oneShot)` | Returns `true`, not a handler ID; invalid registration raises an error. Reusing the owner/name stops the previous registration and replaces it. Use function references for closures. |
| `stopNamedEventHandler(owner, name)` | Removes the active handler but keeps its definition; returns `false` if no definition exists. |
| `resumeNamedEventHandler(owner, name)` | Re-registers the saved definition; returns `false` when absent. |
| `deleteNamedEventHandler(owner, name)` | Stops and forgets the definition; repeated deletion returns `false`. Delete only names owned by this component. |
| `registerAnonymousEventHandler(event, fn, oneShot)` | Returns a numeric ID. Repeated function-reference registrations can duplicate work. Retain the ID and kill it before replacement. Do not rely on string-handler deduplication as an ownership strategy. |
| `killAnonymousEventHandler(id)` | Returns `true` when removed; missing IDs return `nil, message`. Distinguish already-removed one-shot handlers from lost ownership records. |

Callbacks receive `(eventName, ...)`. `raiseEvent(name, ...)` delivers locally; avoid a global event unless cross-profile delivery is intentional. Handler ordering is unspecified. Do not coordinate consumers through registration order. In 5.0.1, a one-shot callback survives while its result is truthy; return exactly `true` to request another evaluation, and `nil`/`false` to finish. Named one-shot definitions still need lifecycle cleanup.

For an event intended as a package integration point, use an owner-qualified name, document the argument order, value types, missing-value behavior, and whether payload tables are borrowed or copied. Raise it after normalization so consumers do not need to know protocol table internals. Do not create events for purely private calls where a direct function is simpler.

Re-registering the same name is not an atomic rollback: validation failure can leave the previous handler stopped. Validate configuration before replacement. Stable names prevent duplicates but do not prevent an old instance from deleting a new instance's handler; tear down old instances first.

## GMCP data

For a message `Example.State`, Mudlet updates the protocol table and raises prefix events including `gmcp.Example` and `gmcp.Example.State`. The callback's next argument is the full protocol key, not the decoded table. Read `gmcp.Example.State` at callback time; a previous table reference may have been replaced. Broad and narrow subscriptions can observe the same message twice.

In 5.0.1, decoded leaves normally replace prior values. Configured merge keys are an exception; `Char.Status` is initially configured for merging. Neither that default nor a familiar field layout establishes your server's schema. Do not change profile-wide merge configuration just to simplify one consumer. An event is also not proof of valid fresh data: the 5.0.1 decoder error path can still raise events after logging an error.

Define normalization per message: snapshot replacement versus application-owned delta merge, field types, deletion representation, and freshness. Missing is not zero; preserve `false` where meaningful. Parse numeric strings only for fields whose schema allows them, reject non-finite values, and protect ratios from missing or nonpositive maxima. Copy only needed values into component state; do not mutate shared `gmcp` tables. On disconnect invalidate component freshness and rebuild it from new-session data; do not erase other consumers' protocol state.

## Shared module requests with gmod

Use `gmod.enableModule(owner, moduleName)` and pair it with `gmod.disableModule(owner, moduleName)` on final teardown. These auto-register the owner; `gmod.registerUser(owner)` is optional. Calls can send protocol traffic and are not pure configuration. Track the component's own requested module set rather than modifying the table returned by `gmod.isRegisteredModule(name)`.

In 5.0.1, enabling tracks a set of users for each exact module string and initially advertises dotted prefixes with version `1`. Re-enabling for the same owner does not create a reference count. Disabling removes that owner's interest and sends removal only once no users of that exact module remain. This is not a general dependency resolver for independently requested parent and child module strings. Do not send blanket `Core.Supports.Set` or direct removals that invalidate other consumers.

The bundled reconnect handler calls `gmod.reenableModules()` on `sysProtocolEnabled` with protocol `"GMCP"`; that function returns early for an empty `gmcp` table. Do not promise reconnect delivery from registration alone. Test actual ordering with the server, using a deliberate reconnect policy rather than adding duplicate hooks. If the server requires another advertised version, design an explicit owner-aware negotiation path; `enableModule` has no version argument in this baseline. It returns no success value on its ordinary path, so a truthiness check cannot verify server acceptance.

If the extension is authored by a game administrator, prefer publishing stable GMCP data and distributing the client package through an approved automatic installation path or the Mudlet Package Repository instead of requiring users to scrape presentation text. This is a server/distribution decision, not authority for a client-package task to change the game server or auto-install itself.

## MSDP and choosing a protocol

Choose GMCP or MSDP from the server's documented capabilities and the existing profile configuration. Some servers provide only one when both are enabled. Select one authoritative producer per application field and normalize behind a common consumer; do not double-apply updates or infer equivalent schemas from similar names.

For MSDP, confirm the profile's MSDP setting and reconnect when changing negotiation settings within the authorized scope. In 5.0.1, accepting the server's MSDP offer sends a commands-list request and client identification, then raises `sysProtocolEnabled` with `"MSDP"`. Install an owned handler for that event and rebuild required reporting on each negotiated session. Invalidate freshness on `sysProtocolDisabled` or disconnect.

Use `sendMSDP("LIST", "REPORTABLE_VARIABLES")` to discover reportable fields where supported; `sendMSDP("REPORT", variableName)` requests ongoing updates and `sendMSDP("SEND", variableName)` requests a current value. Pass strings as separate arguments, not a Lua table or GMCP JSON. Commands and variables must match the server's contract. In 5.0.1, `sendMSDP` returns `true` for a socket write or `nil, message` on connection/write failure; it does not check negotiated MSDP enablement, so success is not evidence of protocol acceptance.

Subscribe to `"msdp." .. variableName` and read the corresponding current `msdp` value inside the callback. The parser supplies the event name and full key, not the payload table. Apply the same missing/partial/type checks as for GMCP. `gmod` does not track MSDP reporting: coordinate subscription ownership before removing server reports, and always remove the component's own event handlers on teardown.

## Example contract

`local Listener = dofile(path)` is safe outside Mudlet. `Listener.new(api, options)` takes `owner`, `name`, `event`, a dense string-array `path` relative to `api.gmcp`, and `onUpdate(value, eventName, fullKey)`. It returns an object exposing `start`, `stop`, `refresh`, and `destroy`. Inject `_G` in Mudlet or a stub API offline. Methods use colon calls; `destroy` is terminal and repeated calls are harmless.

Named mode requires register/stop/delete helpers; otherwise the example uses anonymous register/kill. `start` is idempotent; restarting registers afresh. `refresh` reads current data only while running. The callback receives `nil` for a missing/non-table path and otherwise a borrowed value, with no schema coercion or delta merge. It does not enable modules, negotiate GMCP, or manage session freshness. Those belong to the caller's protocol contract.
