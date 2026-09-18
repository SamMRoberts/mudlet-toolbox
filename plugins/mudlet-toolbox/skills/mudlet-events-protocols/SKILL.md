---
name: mudlet-events-protocols
description: Build or debug Mudlet event handlers and protocol consumers, including handler lifecycle, GMCP partial data, and shared gmod subscriptions.
---

# Mudlet events and protocols

Identify the target Mudlet release, event names, owning component, and the server's protocol contract before changing a consumer. Separate transport delivery, data normalization, and application updates. Preserve the user's game and existing protocol choices.

1. Trace the producer and callback arguments. Subscribe to the narrowest useful event; do not assume callback order or treat a GMCP callback argument as its data table.
2. Assign stable owner/handler names or retain anonymous handler IDs. Make start, stop, reload, and teardown explicit; dispose of the previous instance before replacing its references.
3. Read current protocol data inside the callback. Validate each intermediate table and field; specify how missing, malformed, partial, and stale values affect the application.
4. Manage optional GMCP modules through the component's own `gmod` identity. Establish the server's actual module names and versions; requesting support does not establish server support.
5. When normalized state is intentionally public, raise owner-prefixed custom events with a documented argument contract rather than coupling other packages to handler order or internal tables.
6. Exercise duplicate start, stop/restart, teardown, missing data, partial updates, and reconnect behavior. Report offline logic checks separately from actual protocol negotiation and delivery.

Read [event and protocol contracts](references/event-protocol-contracts.md) for API semantics and reconnect decisions. Adapt [gmcp_listener.lua](examples/gmcp_listener.lua) when a small owned listener is useful; it returns a module and registers nothing until `start()`.

The reference records a Mudlet 5.0.1 compatibility baseline, not a universal version requirement. Inspect the requested runtime before depending on newer helpers. Keep source excerpts and research logs outside the distributed skill.
