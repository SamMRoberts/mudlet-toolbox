---
name: mudlet-lua-scripting
description: Implement or debug Mudlet Lua scripts, aliases, triggers, timers, and keybindings, including regex captures and configuration. Use for scripting behavior inside a Mudlet extension or profile.
---

# Mudlet Lua scripting

Implement the requested behavior at the correct Mudlet input boundary and make it reproducible without depending on live game timing.

## Identify the boundary

Inspect the actual script/alias/trigger/timer definition, its parent groups, active state, patterns, command field, and caller. Request or inspect representative input and expected output. A correct Lua function can still fail because the native object is disabled, its parent filters input, or its pattern is wrong.

Check the target Mudlet version and Lua runtime. Use Lua 5.1-compatible syntax for the included examples; a newer standalone Lua interpreter is not evidence of compatibility. Check optional libraries and APIs before introducing them.

## Implement and diagnose

Read [input and state](references/input-state.md) for capture semantics, PCRE versus Lua patterns, output handling, timer ownership, and persistence. Keep input adapters thin and put reusable behavior into a package namespace or pure functions.

- Capture event/trigger data before deferring work. `matches`, `multimatches`, `line`, and protocol globals can change before a timer callback runs.
- Prefer functions or closures over assembling executable Lua from matched text. Treat game text as data.
- Preserve trigger ordering, multiline semantics, enable/disable behavior, and explicit send behavior when refactoring. Do not replace a persistent object with a temporary one without accounting for reload and teardown.
- Keep temporary resources owned and cancellable. Retain IDs, clear them when one-shot work completes, and prevent duplicate registrations on script saves.
- Use direct function calls between your own features. `expandAlias` passes through alias processing; `send` sends game commands; `echo` displays locally. Select the behavior the user requested.

For a cancellable delayed action, adapt [delayed_action.lua](assets/delayed_action.lua). It snapshots a string argument, replaces pending work, and exposes `cancel`; it creates no timers until called. Load it with `dofile(path)` and instantiate it with an injected callback. It is an example, not a package bootstrap.

## Verify

First test parsing and state transitions with representative positive, negative, and malformed input. Then verify the actual Mudlet object's pattern and callback using a disposable offline profile. Lua's pattern matcher or a Python regex engine does not prove a Mudlet PCRE trigger matches.

Replaying captured lines through `feedTriggers` can execute every matching trigger, including commands that send to a server. Isolate replay from live gameplay and unrelated trigger trees. For multiline and ANSI-dependent behavior, preserve the original sequence and formatting.

Report what changed, the input that reproduces it, and which checks exercised pure logic versus Mudlet's actual trigger/event engine. Use `mudlet-events-protocols` for protocol negotiation or event infrastructure, and `mudlet-package-testing` for a complete installation lifecycle.
