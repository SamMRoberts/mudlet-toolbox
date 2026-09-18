# Identity and merge safety

## Separate identity from placement

Mudlet room IDs are local positive integers. A server ID can be a string, repeat between worlds, or identify an instance only temporarily. Preserve it exactly under an explicit source namespace. A room's coordinates and display name are not reliable identity keys.

Use a stable, unambiguous composite key for source/world plus external ID. Mudlet calls these keys hashes; a cryptographic digest is not required. Verify both hash directions and owner metadata before updating a matched room. Establish how server ID reuse, instancing, source revisions, and shared map ownership should behave for this project; none has a universal policy.

## 5.0.1 API distinctions

| API | Relevant semantics |
| --- | --- |
| `createRoomID([minimum])` | Finds an unused positive ID; optional minimum must be positive. Does not create or reserve a room. Repeated calls without adding rooms can return the same ID. Missing map returns `nil, message`. |
| `addRoom(id[, areaID])` | Returns a boolean for ordinary creation/failure. If creation succeeds but area assignment fails, returns `nil, message` after placing the new room in the default area. Treat that result as partial mutation; verify area existence and resulting assignment. |
| `getRoomIDbyHash(hash)` | Returns the linked ID, or `-1` if absent. Zero is not the absent sentinel. Verify room existence because a hash entry alone is insufficient. |
| `getRoomHashByID(id)` | Returns its hash, or `nil, message` if none. |
| `setRoomIDbyHash(id, hash)` | Replaces existing links on both sides; does not validate that the room exists. Returns no values. Check preconditions and read back both directions instead of testing truthiness. |
| `getRoomName(id)` | Returns a string for an existing room, including an empty name; invalid room returns `nil, message`. Use presence, not a nonempty name test. |
| `getRoomUserData(id, key[, fullErrors])` | Default missing key/invalid room yields `""`; with full error reporting enabled those yield `nil, message`. Check room existence separately. |
| `setRoomUserData(id, key, value)` | Stores a string; returns `true` or `nil, message` for an invalid room/map. Namespace keys and write only owned fields. |
| `clearRoomUserDataItem(id, key)` | `true` means removed, `false` means already absent, `nil, message` means error. For idempotent cleanup accept either boolean. Never erase the whole metadata table to remove one owned key. |
| `setExit(from, to, direction)` | Writes a directed standard exit, returning a boolean. A positive destination must exist; a nonpositive destination removes the exit. Validate input so an unknown destination cannot become an accidental deletion. |

Some mapper APIs assume a map object internally; establish map availability before invoking an entire pipeline. `pcall` catches Lua errors, not native crashes. Do not invent a common return-value convention across mapper APIs.

## Topology on sparse grids

A standard exit records graph topology independently from visual distance. For rooms on the same area and floor, a north/south/east/west relationship may span one or more grid cells. Under a straight-axis layout policy, north requires the destination to have the same x coordinate and a greater y coordinate; south uses a smaller y, east the same y and greater x, and west the same y and smaller x. The sign matters, but the magnitude need not be one. Up/down, cross-area links, and special exits need their own project-defined placement rules rather than inheriting this planar rule.

Do not create intermediate rooms, retarget an exit, synthesize a reverse exit, or move an established room merely to fill or remove empty grid cells. A valid long edge can cross unused coordinates. If an existing destination is off the expected axis, keep valid source topology and report a placement conflict separately; visual placement is not evidence that the exit points to a different room.

Before assigning or changing coordinates:

1. Classify each relevant coordinate as source-authoritative, user-edited or foreign, mapper-owned established, or mapper-owned provisional. Treat every class except the last as fixed unless the user explicitly authorizes a broader re-layout.
2. Gather every already positioned incident neighbor and occupied coordinate, not only the room from which the new room was discovered. Test a candidate against all known directional constraints so closing a loop cannot silently invalidate an earlier edge.
3. Evaluate candidates along the permitted directional ray using the mapper's documented spacing policy. Nearest-free placement can be a preference, but it is not proof of adjacency; retain or introduce gaps when occupancy, loop closure, or space for an inner cluster requires them. Do not impose one universal spacing value on every source.
4. If no candidate satisfies the fixed constraints, prepare a reviewable insertion or reflow plan limited to mapper-owned provisional rooms. Revalidate every moved room against occupancy and all incident topology. If no safe provisional-only plan exists, defer the coordinate change and report the layout conflict without discarding or rewriting the exit.
5. Recheck ownership immediately before applying a reflow, journal the moved rooms, and read back their coordinates and ownership afterward. Refresh the map only after the batch is coherent so retries can distinguish completed moves from pending ones.

## Apply a merge in phases

1. Normalize and validate the source offline. Reject duplicate composite identities, malformed IDs, dangling references, and unsupported source formats. Retain per-record errors rather than silently dropping features.
2. Inspect existing identities and owned fields; prepare a reviewable plan. Hash collisions, missing linked rooms, inconsistent reverse links, and owner mismatches block that record. Do not repair them by overwriting foreign data.
3. For each new room, obtain and immediately add an unused ID before yielding. Set owned identity metadata and the hash, checking results and reading the links back. A group of planned candidate IDs is not a reservation pool. Track locally reserved IDs when planning a batch, or allocate each ID during application.
4. Populate agreed fields and areas, then resolve exits against the completed source-to-local map. Validate sparse-grid placement separately from exit identity. Do not synthesize reverse exits. Keep special exits, doors, locks, weights, and movement commands distinct; infer none from a directional label. Avoid overwriting user layout or annotations unless their fields are explicitly owned.
5. Journal successful steps and errors across bounded batches. Recheck ownership after a yield. A failure after room creation is partial application, not a transaction rollback. Report it and resume only from verified state; do not delete preexisting rooms during cleanup. Check topology before calling `updateMap()` once per coherent batch.

For a merge, do not use map replacement/clearing APIs as an import shortcut. Saving or loading maps, bulk deletion, and actual travel are separate effects requiring the user's task scope. `centerview` changes displayed position; it is not proof of movement or confirmed server location. A path found in a graph does not establish that doors, special commands, locks, or server movement will succeed.

## Persistence and navigation

Before an authorized map mutation, save a recoverable snapshot with `saveMap(path)` and check its boolean result. The destination directory must exist. In 5.0.1, an explicit binary format uses `saveMap(path, formatVersion)`; the first argument is a path, not a version. Confirm formats supported by both the writer and intended reader instead of hard-coding a universal map version. `updateMap()` refreshes display; it does not save a snapshot.

For full-map JSON interchange, 5.0.1 provides `saveJsonMap(path)` and `loadJsonMap(path)`, returning `true` or `nil, message`; their bindings require an initialized mapper/2D map. Feature-check these functions and format compatibility on other releases. JSON map data is a whole-map format, not an arbitrary room-list import contract. `loadMap(path)` handles native maps and XML through different paths: ordinary results are boolean, while XML failure can return `nil, message`.

Treat `loadMap` and `loadJsonMap` as whole-map restore/import operations, not ownership-aware merges. Use the phased room/exit workflow above for a merge. Verify snapshot round-trips in an authorized disposable profile; a successful write alone does not establish restoration fidelity. Do not load a snapshot into the active profile merely to test it.

When extending Mudlet's generic mapper, place customization triggers and scripts in a separately owned folder or package, not inside `generic_mapper`. The generic mapper owns its folder and may replace it during updates. Record the dependency and test the customization after mapper upgrades without modifying or duplicating the managed objects.

For route preview, call `getPath(fromRoomID, toRoomID)`. In 5.0.1 it returns `true, totalWeight` on success; a disconnected route returns `false, -1, message`, and invalid rooms/map return `nil, message`. It fills shared `speedWalkPath`, `speedWalkDir`, and `speedWalkWeight` tables; copy the needed route immediately before another planner can overwrite them, and never consume them after failure. This computes a route without starting travel.

`gotoRoom(targetRoomID)` plans from the current mapped room and invokes `doSpeedWalk` through the configured speedwalk machinery. Use it only for requested movement, after checking the game's actual movement adapter, special exits, and server-confirmed current room. Stop the adapter's owned timers/queue on cancellation or location mismatch; there is no cancellation behavior implied by `getPath`. Replan from confirmed location rather than assuming completion. Verify these return contracts and adapter behavior for the requested runtime.

## Example contract

`local Planner = dofile(path)` returns a module. `Planner.planRoom(api, owner, source, externalID)` returns a plan table or `nil, reason`; all identity arguments are nonempty strings. It uses length-prefixed identity components to preserve distinctions such as `"007"` versus `"7"`. Owner is part of the hash namespace, intentionally preventing automatic adoption between independent importers.

The returned plan has `action` (`"create"` or `"reuse"`), `roomID`, `hash`, `ownerKey`, `owner`, `sourceKey`, `source`, `externalKey`, and `externalID`. Required read API: `getRoomIDbyHash`, `getRoomHashByID`, `getRoomName`, `getRoomUserData`, and `createRoomID`. A fake API can expose these as ordinary functions; `_G` can be used with an available Mudlet map. The function performs no map writes or display changes.

Existing rooms are reusable only if all three metadata values and the reverse hash agree. New candidate IDs are checked for stale reverse hashes. An allocation failure, stale hash, foreign owner, mismatched identity, or invalid candidate produces an error result. Map availability is a caller precondition because some underlying APIs assume it. The caller must revalidate the proposal immediately before applying it. The example does not discover orphan metadata, repair a previous partial import, reserve IDs, or apply topology.

Offline checks can prove collision decisions and lack of write calls. Native mapper persistence, repainting, pathfinding, and server-confirmed room synchronization remain separate acceptance checks in an authorized disposable profile.
