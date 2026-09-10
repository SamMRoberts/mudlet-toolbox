# Lifecycle and release

## Initialization and cleanup

Scripts execute during loading and when saved in the editor. Defining functions is safe; unconditionally adding another timer, trigger, event handler, or window is not. Use one explicit start/stop lifecycle and retain ownership of resources.

`sysLoadEvent` occurs after profile loading; a new package installed into an already running profile also needs its installation path handled. `sysInstallPackage` identifies the installed package. `sysUninstallPackage` runs before removal and identifies the package being removed. Filter by exact package identity before starting or stopping. Verify module-specific events separately if supporting Module Manager; a package-only lifecycle adapter is not automatically module-aware.

Capture IDs from temporary objects/anonymous handlers and remove only those owned by the extension. Prefer named registration when the target runtime supports the required API and semantics. Reinitialization must not duplicate registrations. Stop callbacks/timers before deleting their target UI or state. Cleanup should tolerate a second call and partial initialization.

Permanent objects are managed through the package's native object tree. Do not globally remove similarly named objects belonging to another package. Restore shared borders/settings only when ownership and current state permit it; do not overwrite a newer owner's changes.

## User configuration

Store user-editable settings outside the package directory if they must survive replacement or uninstall. Choose persistence according to the existing project. Specify defaults and schema migration only when persistence is actually required. Distinguish a missing settings file from a corrupt file; avoid silently overwriting recoverable user data.

For `table.save`/`table.load`, confirm argument order, accepted contents, and failure behavior on the selected Mudlet version. Use data-only formats for untrusted imported configuration; never evaluate downloaded Lua as a settings parser. Exclude account credentials, connection secrets, and unrelated profile state from exported packages.

## Release preparation

1. Confirm package name, version, description, required dependencies, resources, notices, and supported runtime.
2. Build from source and inspect all native XML entry files, object groups, and assets. Verify dependency presence at runtime before use and provide actionable missing-dependency messages.
3. Test a fresh install, profile restart, reinitialization, upgrade, and uninstall. Compare settings preservation with the requested behavior.
4. Test alongside a second package that uses overlapping events. Uninstalling one must leave the other functioning.
5. Record exactly which artifact was tested; regenerate and recheck if source changed afterward.

The Mudlet package repository supports website submission, a contribution of the package under its `packages/` directory, and a documented trusted-publishing workflow. Consult the current repository instructions when publishing is requested. Prepare metadata and artifacts first; do not infer permission to publish, push commits, or enroll CI from a request to build a package.
