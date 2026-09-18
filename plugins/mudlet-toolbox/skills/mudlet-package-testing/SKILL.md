---
name: mudlet-package-testing
description: Inspect and test Mudlet XML, mpackage artifacts, or extension source for packaging errors and runtime lifecycle regressions. Use for installation, reload, upgrade, uninstall, or coexistence verification.
---

# Mudlet package testing

Separate artifact validity, pure Lua behavior, Mudlet engine behavior, visual acceptance, and connected-game acceptance. Report each at the level actually observed.

## Inspect before executing

Identify the exact source revision, artifact, target Mudlet version, dependencies, expected behavior, and allowed profile. Inventory existing package objects/resources before installing a replacement. Do not execute arbitrary `config.lua` as a metadata reader.

Run the bundled read-only inspector with Python 3.10+:

```sh
python3 <this-skill>/scripts/inspect_package.py /absolute/path/extension.mpackage
```

It also accepts plain XML. It produces JSON inventory and diagnostics without extraction or Lua execution. It detects selected malformed/unsafe container conditions; it is not a complete Mudlet schema validator or a malicious-code scanner. Read the report, including unknown elements and limitations, rather than treating exit zero as runtime acceptance. Use `--help` for resource limits.

## Test the changed boundary

Read [acceptance matrix](references/acceptance.md) and select relevant checks. Use project-defined tests first. Test parsing/state logic with Lua 5.1-compatible tooling and run syntax checks on all changed Lua, including code embedded in XML or JSON. Stubs can establish ownership and logical behavior but cannot validate native function signatures or UI rendering.

When available and within scope, run native checks in a disposable offline Mudlet profile. Keep generated profiles and evidence separate from the user's normal profile. Verify that profile selection and connection state are correct before replaying input or installing code. If a launch/automation mechanism cannot provide isolation, report the missing runtime evidence instead of repurposing a live profile.

Review the changed boundary against [Mudlet's best-practices concerns](references/acceptance.md#best-practices-review). Treat them as decision checks, not text-matching rules: confirm why a recommendation applies, or record why the existing design is more appropriate.

For package operations, observe each completion before starting the next. Verify both affected and unaffected packages afterward. Test the actual loaded artifact, not just the source that was intended to produce it.

## Deliver evidence

Record commands, runtime/tool versions, artifact identity, expected versus observed results, and any untested checks with reasons. For UI work include native screenshots/observations of resizing, focus, callbacks, and cleanup. For protocol work distinguish synthetic event injection from an actual server exchange.

Fix defects and rerun the relevant checks. Do not weaken valid tests or remove a requested feature to pass a packaging check. A failure in one independent package need not block inspection of the others; report each outcome.
