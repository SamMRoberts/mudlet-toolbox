# Input, state, and diagnostics

## Choose the correct object

| Input | Appropriate boundary |
| --- | --- |
| User command | Anchored alias pattern; parse and call a function. |
| Incoming game text | Trigger of the appropriate type: substring, exact, regex, multiline, prompt, or color. |
| Structured server data | Protocol event handler reading the relevant protocol table. |
| Elapsed time | Owned timer with explicit cancellation. |
| Keyboard shortcut | Native keybinding calling the same function as an alias. |

Use the native object types already present. Inspect both the code and the object's settings; a timer's active state, parent group, or trigger's filter/multiline settings are observable behavior.

## Locals, namespaces, and initialization

Make temporary variables and internal helpers local. Globals share one profile-wide table, so generic names can collide with Mudlet APIs or another package. Avoid indirect `_G[name]` reads and writes unless dynamic global access is the actual contract. Expose only the package surface that other objects or packages need under one unique table, and use local aliases for frequently reused values when that improves a hot path without obscuring the code.

Use `PackageName = PackageName or {}` to preserve an existing namespace when a script is compiled again. That protects data but does not make resource creation idempotent: retain and stop the old timers, handlers, triggers, and widgets before replacing their implementations. If some initialization must run once, track that state inside the namespace and keep normal function definitions safe to recompile.

Colon methods are appropriate when the function operates on its table/object and needs `self`; dot functions are clearer for stateless helpers. Do not use metatables or object patterns solely to imitate classes when a small module table is enough. The Lua `condition and x or y` idiom is safe only when `x` cannot be `false` or `nil`; otherwise use an explicit branch.

## Captures and matching

For an ordinary regex match, `matches[1]` is the complete match, and subsequent entries hold captures. Named captures and `multimatches` depend on trigger mode/version; inspect real results rather than guessing the table shape. Copy the specific values needed by a deferred callback into locals. Copy nested tables if later mutation matters; assigning another reference is not a snapshot.

Mudlet regex triggers/aliases use PCRE-style expressions. Lua `string.match` uses Lua patterns: `\d`, alternation, and lookarounds are not portable into Lua patterns. JSON and Lua strings add another escaping layer; check the final runtime pattern rather than counting escapes in source alone. Long-bracket Lua strings can clarify literal backslashes.

Anchor command aliases to avoid swallowing unrelated input. Preserve the meaning of optional capture groups and validate conversion before arithmetic. A number can be zero; do not conflate zero with absent data. Avoid treating a generic `hp` field or room identifier as universal across MUDs.

Complex regex triggers are evaluated frequently. When a stable literal must be present, use a substring trigger/condition as a cheap gate before the regex; for a multiline trigger, a preceding substring condition with line delta zero can serve the same purpose. Do not add a gate that changes which lines or captures reach the regex, and do not assume every regex is expensive enough to justify extra structure.

## Output and actions

Use `echo` for plain untrusted text and `cecho` only when interpreting color markup is intended. Escape data for the specific HTML, color, JSON, or command context where it is inserted. Do not create `loadstring` expressions from captures.

Keep the native command field and Lua `send` calls consistent: having both can send twice. Distinguish server output from locally printed feedback. If gagging or redirecting text, preserve formatting and consider how changes to the current selection or line affect subsequent triggers.

Owned aliases, triggers, and keys should call the package function that implements the behavior. Avoid using `expandAlias` as internal control flow: it invokes the alias engine again, can recurse, depends on command-separator settings, and can overwrite the current `matches` table. Reserve it for cases where intentionally processing text through the user's alias stack is the requested behavior.

## Timers and reload

Store the ID returned by `tempTimer` and clear it inside a one-shot callback. When replacing a pending action, kill its old ID first. Where the target runtime and project conventions support named timers, use a stable owner/name and stop, resume, or delete only that owned registration. A teardown path cancels pending work before removing its state. If callback registration fails, report the error without pretending the feature started.

For repeated work, use the existing project's named/permanent timer conventions or an owned rescheduling timer. Do not use blocking sleeps in Mudlet's UI thread. A cancelled or stopped feature must not rearm itself from an already running callback.

The supplied delayed-action example takes `new(emit, delay)`, then `schedule(text)`/`cancel()`. To react to a capture, pass `matches[2]` immediately to `schedule`; the saved string survives later changes to `matches`. Replace `emit` with a local presentation or domain function. Introducing a server command is a separate behavior choice.

## State and settings

Use a unique table for public package state; keep internal values local. `Namespace = Namespace or {}` preserves state on compilation, but it does not clean up old closures or resources. Capture the old instance and stop it before replacing implementations that own timers/handlers.

For persistence, follow existing settings conventions and distinguish defaults, runtime caches, and durable values. Store only needed data, outside replaceable assets. Test missing, malformed, and older settings when changing persistence; do not invent persistence for a transient feature.

## Diagnose the smallest boundary

1. Confirm the object is enabled, its parent admits the input, and its pattern sees the actual text.
2. Observe captures and function arguments with the Errors view/Debug tools, excluding secrets.
3. Exercise the parser/function directly with captured input.
4. Verify the native trigger/alias invocation separately.
5. If duplicates occur, inspect native objects and owned timer/handler IDs before adding debounce logic.

`feedTriggers`, `cfeedTriggers`, `dfeedTriggers`, and related helpers re-enter the trigger engine. Use them for isolated replay/testing, not to connect production components. Production callers should invoke the shared function directly so behavior does not depend on the trigger tree or activate unrelated sends.
