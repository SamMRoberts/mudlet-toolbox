---
name: mudlet-mapper-development
description: Build or debug Mudlet mapper integrations and merge-safe imports, including external room identity, map ownership, topology, and incremental updates.
---

# Mudlet mapper development

Inspect the target runtime, existing map state, source format, and identity contract before proposing writes. Separate server identifiers, Mudlet room IDs, and visual coordinates. Do not infer an Aardwolf schema, numeric server IDs, map format version, or bidirectional movement.

1. Define source identity, owned metadata, and a collision policy. Treat existing rooms and user-edited fields as foreign until ownership is established.
2. Plan additions and conflicts without changing the map. Validate source records, area references, coordinates, exit destinations, and special-exit semantics before application.
3. Allocate Mudlet IDs for new rooms, retaining a source-to-local mapping. Reuse only rooms whose identity and ownership agree. Defer ambiguous or foreign collisions; do not seize their hashes.
4. Apply rooms before exits in bounded batches. Recheck preconditions after yielding, record partial progress and failures, and make reruns safe. Preserve unrelated map state.
5. Check each API's actual return contract and read back identity links. Refresh the display after a coherent batch. Keep map display, current-room synchronization, path planning, and movement execution separate.
6. Keep generic mapper customization triggers outside the managed `generic_mapper` folder so mapper updates do not overwrite them; use a separately owned group/package.
7. Report counts for added, reused, skipped, conflicted, and failed records. Distinguish offline validation from live mapper, pathfinding, persistence, and movement evidence.

Read [identity and merge safety](references/identity-merge-safety.md) before mapper mutations. Use [room_plan.lua](examples/room_plan.lua) for a read-only, single-room planning example. It proposes an ID without reserving or creating it; it is not an importer.

Use `mudlet-geyser-ui` when the request is about constructing, embedding, docking, reparenting, styling, showing, or deleting a `Geyser.Mapper`. Keep room identity, topology, import, persistence, pathfinding, and movement in this skill. A rendered Mapper does not prove map data or server location is correct.

The API baseline is Mudlet 5.0.1. Validate other requested releases and formats directly. Keep source data, raw research, and provenance outside the distributed skill.
