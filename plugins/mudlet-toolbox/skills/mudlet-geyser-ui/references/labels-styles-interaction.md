# Labels, styles, and interaction

Use this reference for Label content, images, styling, mouse interaction, flyouts, and right-click menus. The [Label section](https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser#Geyser.Label) and [StyleSheet section](https://wiki.mudlet.org/w/Special:MyLanguage/Manual:Geyser#Geyser.StyleSheet) remain the live practical sources.

## Label content and formatting

Create a named `Geyser.Label` under an owned parent, then update it with `echo`, color/font methods, alignment, or one complete stylesheet. Labels render rich text rather than terminal lines. Escape external `&`, `<`, `>`, quotes, and apostrophes before inserting them into HTML. Newlines require HTML such as `<br>`; repeated spaces require deliberate markup such as `&nbsp;` or escaped content inside `<pre>`. Do not apply those substitutions to a MiniConsole, which has different output rules.

Set font size only when the product needs a fixed size; otherwise allow profile/UI scaling. If a particular font is required, package a redistributable copy and define a fallback. Test clipping and wrapping at supported scale factors.

Use `setAlignment` or the stylesheet alignment property consistently. Word wrapping is disabled by default in the manual's baseline and can be enabled through the appropriate Qt property. Set the full stylesheet in one call: later `setStyleSheet` calls replace rather than append earlier declarations.

## Images, transparency, and cursors

Use `setBackgroundImage` for a label image or Qt stylesheet image properties when stretching, tiling, positioning, or borders are needed. Package images below the extension and construct portable paths with `/`; do not ship developer desktop paths. Record licenses/notices for redistributed art.

Use `border-image` when the image should fill the label and `background-image` plus positioning/repeat properties when it should retain its own placement. Verify aspect ratio, scaling quality, transparency, missing-file behavior, and high-DPI results natively. Quote/escape paths for the stylesheet context rather than concatenating untrusted paths.

Transparent visual content does not imply mouse click-through. A fully transparent Label can still cover underlying controls. Use show/hide, click-through support, or layout changes according to the intended interaction and verify native event routing.

Use `setCursor` for a supported system cursor and `setCustomCursor` only with a packaged image and target-platform testing. The manual recommends a small PNG for broad compatibility; do not assume a custom cursor's size/hotspot behaves identically across platforms.

## Styles and `Geyser.StyleSheet`

Plain CSS strings are appropriate for a small fixed style. Use `Geyser.StyleSheet` when properties are shared, inherited, queried, or changed independently.

- Construct from a CSS string or property table.
- Use a target such as `QLabel` or `QPlainTextEdit` to prevent a rule from affecting an associated tooltip, console, or command line.
- Use `getCSS` when applying the generated string to a widget.
- Use `set`/`get` for one property and `setStyleTable`/`getStyleTable` for a property set.
- Use `setCSS` to reset an existing object without breaking children that inherit from that StyleSheet object.
- Pass a parent StyleSheet to inherit defaults; request non-inherited values when diagnosing which layer supplied a property.

Stylesheet inheritance here is the Geyser StyleSheet relationship; Qt selector inheritance is a separate rendering concern. Scope rules to the intended widget type. Tooltips can inherit a Label's unscoped background/image rule, so use a `QLabel` target when the tooltip must remain distinct. Treat Qt CSS support as platform/version-sensitive and test the actual Mudlet build.

## Click, hover, and state controls

Use function callbacks with `setClickCallback`, not Lua source assembled from data. Bound arguments precede the native mouse event value; inspect the target release if button/position details matter. Keep the callback thin and call an owned application function. Disabled controls need both disabled styling and an action guard; appearance alone is not authorization.

Hover styles use Qt selector states. Keep normal and hover rules together so one update cannot discard the other. Verify keyboard accessibility and provide a non-pointer path when the action is important.

A checkbox made from a Label is an application pattern, not a native checkbox contract: keep the boolean in owned state, render both images/styles from that state, and update state before presentation. Do not infer state from the current image filename. Include an accessible text/command alternative when needed.

Sprite animation is another composition pattern. Retain the timer ID, change only the frame/image of the existing Label, stop the timer when hidden/destroyed if animation should cease, and prevent an old callback from rearming after teardown. Package every frame and handle missing assets without leaving a runaway timer.

## Tooltips and visibility

Use `setToolTip` for concise help and verify the target release's duration/format semantics. A tooltip is supplementary; essential state must remain visible or otherwise accessible. Gauges expose Label children, so tooltip/callback guidance applies to the selected child rather than to an invented Gauge-wide behavior.

`show` and `hide` cascade through Containers. Hiding releases screen space and pointer coverage but retains the object, callbacks, and state. Use deletion for teardown and visibility for tabs, collapsible sections, or temporary suppression.

## Flyout labels

Flyouts use a named main Label configured for click nesting (`nestable`) or hover nesting (`nestflyout`). Add named children with `addChild`, choose a two-letter `layoutDir` combining side (`R`, `L`, `T`, `B`) and orientation (`V`, `H`), and use `flyOut` for children that disappear when no longer hovered.

The pinned manual says the main flyout Label is rooted directly rather than placed in another Container. Treat that as a version-specific restriction: verify the target release before changing the hierarchy. Test all expansion directions near screen edges, nested menus, hover transitions, focus, and teardown. Do not build unbounded or data-generated menus without validating item count and names.

## Right-click menus

Right-click Label menus are documented for Mudlet 4.10+. `createRightClickMenu` accepts a nested item structure and menu styling/size/format options. Bind actions with `setMenuAction`; locate a generated element with `findMenuElement` only after confirming it exists. Use unique display paths for nested actions and avoid relying on ambiguous duplicate captions.

If the Label already has a left-click callback, create the context menu first and forward the native event to `onRightClick(event)` from the callback where required. This ordering and event shape need native verification. Keep menu callbacks owned, validate any data they capture, close menu levels deliberately after actions, and do not issue a game command merely because the manual's demonstration does.

## Native acceptance

Exercise rich-text escaping, CSS targets, selector/tooltip behavior, image scaling and missing assets, transparency and click-through, hover/left/right clicks, mouse event arguments, custom cursors, word wrapping, flyout direction, menu nesting, animation cancellation, keyboard alternatives, reload, and deletion. A Lua stub can establish callback ownership and state transitions but not Qt rendering or input dispatch.
