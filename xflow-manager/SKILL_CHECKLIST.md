# Xpell Flow Manager Checklist

Use this checklist for every Flow Manager, XUI-to-flow, or XVibe flow-binding change.

## Contract Review

- Public module names are exact: `flow`, `flow-client`, `server-xvm`.
- Public ops are exact: `flow.run`; `flow-client.bind`, `flow-client.trigger`, `flow-client.help`; `server-xvm.set_flow`, `server-xvm.get_flow`, `server-xvm.list_flows`.
- Underscore-prefixed methods are treated as implementation details.
- Flow definitions remain data-only JSON.
- Server flow steps execute only through `_x.execute`.
- `server-xvm` persists flows and never executes them.
- `flow-client` bridges client events to server flow execution and never runs server business logic directly.
- XData is treated as runtime state, not persistence.

## UI-to-Flow Binding Review

- The target XUI object is resolved through shared target resolution.
- Binding mutates existing XUI fields only: `_flow`, `_flow_event`, `_flow_auto`, and supported success-view metadata.
- No primitive-specific resolver is introduced.
- No invented `_on.click` flow contract is used when `_flow` is intended.
- No duplicate runtime execution path is introduced.
- No second event bus or flow executor is introduced.
- No client-side primitive execution is added.
- No direct flow file writes are added.

## XVibe Primitive Gate

Before any executable semantic action:

1. Canonicalization.
2. View resolution.
3. Target resolution.
4. Validation.
5. Structured view mutation.
6. Persistence through the existing StructuredViewEdit/ServerXVM path.
7. Runtime execution through XUI and Flow Manager.

Mutation plans must execute only canonical primitives.

## Required Tests

For every UI-to-flow binding feature, report:

- Unit tests.
- Pipeline integration tests.
- Persistence tests.
- Retry tests.
- Composition tests.
- Build.

For any new flow-binding primitive, include:

- XUI field mutation test.
- Persisted view JSON test.
- Reload test.
- Runtime `ui:flow-trigger` test.
- `flow-client.trigger` command-shape test.
- Server `flow.run` test.
- Output-to-XData test.
- Success/error command test.
- At least one real prompt acceptance test that proves prompt-to-runtime behavior.

## Logging Review

- Log flow id, app id, env, module/op, source event, target object id when available, validation failures, persistence writes, retry attempts, and final result status.
- Do not log secrets or raw credentials.
- Preserve existing `[flow]` and `[flow-client]` log prefixes for related paths.

## Regression Prompts

Run or account for these prompts when XVibe flow binding touches structured editing or UI mutation:

- "Change My App to Dashboard"
- "Add footer label"
- "Hide Refresh"
- "Create toolbar"
- "Create toolbar with Save and Cancel"
- "Toolbar + move Refresh"
- "Make Save run the create-project flow"
- "Bind the Submit button to create-vendors and go to vendors-list on success"
