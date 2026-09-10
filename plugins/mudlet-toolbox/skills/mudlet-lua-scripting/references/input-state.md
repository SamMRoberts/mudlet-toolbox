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

## Captures and matching

For an ordinary regex match, `matches[1]` is the complete match, and subsequent entries hold captures. Named captures and `multimatches` depend on trigger mode/version; inspect real results rather than guessing the table shape. Copy the specific values needed by a deferred callback into locals. Copy nested tables if later mutation matters; assigning another reference is not a snapshot.

Mudlet regex triggers/aliases use PCRE-style expressions. Lua `string.match` uses Lua patterns: `\d`, alternation, and lookarounds are not portable into Lua patterns. JSON and Lua strings add another escaping layer; check the final runtime pattern rather than counting escapes in source alone. Long-bracket Lua strings can clarify literal backslashes.

Anchor command aliases to avoid swallowing unrelated input. Preserve the meaning of optional capture groups and validate conversion before arithmetic. A number can be zero; do not conflate zero with absent data. Avoid treating a generic `hp` field or room identifier as universal across MUDs.

## Output and actions

Use `echo` for plain untrusted text and `cecho` only when interpreting color markup is intended. Escape data for the specific HTML, color, JSON, or command context where it is inserted. Do not create `loadstring` expressions from captures.

Keep the native command field and Lua `send` calls consistent: having both can send twice. Distinguish server output from locally printed feedback. If gagging or redirecting text, preserve formatting and consider how changes to the current selection or line affect subsequent triggers.

## Timers and reload

Store the ID returned by `tempTimer` and clear it inside a one-shot callback. When replacing a pending action, kill its old ID first. A teardown path cancels pending work before removing its state. If callback registration fails, report the error without pretending the feature started.

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
