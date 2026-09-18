# Consoles, gauges, and input

Use this reference for `Geyser.MiniConsole`, `Geyser.Gauge`, and `Geyser.CommandLine`. Consult the live [MiniConsole](https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser#Geyser.MiniConsole), [Gauge](https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser#Geyser.Gauge), and [CommandLine](https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser#Geyser.CommandLine) sections for practical syntax.

## MiniConsole construction and output

Create one owner-qualified `Geyser.MiniConsole` per distinct text surface. Choose font size, scrollbar, background, wrapping, and buffer limits as product behavior rather than copying demo defaults. `autoWrap` follows geometry; a manual wrap column is a different policy and conflicts with auto-wrap in the 5.0.1 implementation. Character (`c`) constraints are useful when a pane's dimensions should follow its font metrics.

Use `echo` for plain text and `cecho`, `decho`, or `hecho` only for intentionally interpreted color formats. Preserve newlines explicitly. Bound chat/history buffers with `setBufferSize` when unbounded output is not required. `clear()` removes the MiniConsole contents; it is not teardown.

`setBackgroundImage` is documented for newer baselines such as Mudlet 4.10+. Package the image, select its placement deliberately, and test text contrast, transparency, resizing, and missing files. A background image is presentation; do not encode application state only in the image.

## Copy, edit, redirect, and gag

Color-preserving capture uses Mudlet's active selection/current-line APIs before `appendBuffer`. Editing a copied line uses selection and replacement APIs, which mutate the active console selection and formatting state. Keep this logic in a narrowly matched trigger, preserve foreground/background when replacing, and reset or leave selection state as the surrounding package expects.

Gagging the main line with `deleteLine()` is destructive presentation behavior. Classify and copy the intended line first, then gag only the line owned by that feature. Do not install a universal `^` trigger or hide unrelated/manual output in production. Preserve actionable errors and verify trigger ordering with other packages.

These workflows depend on Mudlet's trigger engine and current-line context. Pure Lua tests cannot establish ANSI/color fidelity, trigger ordering, selection state, or whether the correct line was deleted.

## Links and menus in consoles

Clickable text can use Mudlet link APIs with the MiniConsole's window name. Prefer function-backed application actions where the API permits. If a target release accepts only command strings, generate them only from fixed trusted commands; never interpolate game/protocol/user text into executable Lua. Supply useful hints and a non-pointer command path.

Set foreground/background formatting on the intended console and restore/reset formatting afterward. Verify scrolling, selection, copy/paste, link activation, tooltip text, and keyboard accessibility natively.

## MiniConsole command line

MiniConsoles and UserWindows can expose their built-in command line with `enableCommandLine`. With no custom action, entered text follows Mudlet's normal command/alias path and can be sent to the server. This is a material behavior, not a neutral text field.

Use `setCmdAction(function(input) ... end)` when the field is custom input, and feature-check it for targets outside the verified baseline. Keep user input as a string, call a normal function, and decide whether to clear, retain, echo, or add it to history. Never use `loadstring` or generated callbacks.

## Gauge values and presentation

Construct `Geyser.Gauge` once and call `setValue(current, maximum, text)` when normalized state changes. When no maximum is supplied, the value is treated as a percentage in the common API; do not switch between forms accidentally. Call `setText` when only the label changes.

Validate finite numeric inputs and a positive maximum before division. Define how to handle current values below zero or above maximum. Escape external gauge text because the visible text is Label-backed rich text. In the 5.0.1 source, an invalid nonpositive/NaN maximum can leave the previous reading visible and return an error; surface stale/unknown state rather than silently retaining it.

Gauge orientation values documented by the practical manual are `horizontal` (left-to-right), `vertical` (bottom-to-top), `goofy` (right-to-left), and `batty` (top-to-bottom). Confirm those names for the target release. Use `setColor` for simple colors or style the `front`, `back`, and `text` Labels separately for deliberate Qt CSS. Treat those child names as the documented Gauge composition, not as unrelated widgets to re-own.

For clicks, bind the top `text` Label or deliberately enable its click-through and bind the underlying `front`/`back` Labels. Use `enableClickthrough` only when the intended event routing is understood. Put tooltips on the appropriate child Label. Verify which layer receives each mouse button and whether zero-width/empty regions remain clickable.

## Standalone `Geyser.CommandLine`

`Geyser.CommandLine` is documented for Mudlet 4.10+. Create it with an owner-qualified name, parent-relative geometry, and a scoped stylesheet. By default, input is processed like the main command line, including aliases and possible server sends. Use `setAction(function(input) ... end)` to turn it into application input and keep the callback local/owned.

Scope CommandLine CSS to `QPlainTextEdit` when a broader stylesheet could bleed into an associated MiniConsole or UserWindow. Confirm placeholder, selection, focus, input-method, history, command echo, and accessibility behavior in the actual platform build. An extra CommandLine can live inside a normal or Adjustable.Container, but user resizing must not make it unreachable or overlap content.

## Data-driven updates

Keep transport and presentation separate:

1. an owned event/trigger handler validates and normalizes data;
2. application state records freshness and missing values;
3. one render function updates Gauge, Label, and MiniConsole objects;
4. teardown stops the producer before deleting those objects.

Do not mutate shared `gmcp`/`msdp` tables from UI code. A protocol event or stubbed payload does not prove server negotiation, update frequency, or completeness.

## Native acceptance

Test wrapping and font-cell sizing, bounded buffers, ANSI/color copy, selection edits, exact-line gagging, link activation, scroll position, background images, Gauge ratios/orientations/click layers, built-in and standalone command-line default sends, custom actions, focus/history/input methods, reload, and deletion. Capture unintended sends in an offline profile before any connected-game acceptance.
